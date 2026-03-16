"""Squarespace Authentication."""


import datetime
import json
import requests
from typing import Optional

from singer_sdk.authenticators import OAuthAuthenticator, SingletonMeta
from singer_sdk.helpers._util import utc_now
from singer_sdk.streams import Stream as RESTStreamBase



# The SingletonMeta metaclass makes your streams reuse the same authenticator instance.
# If this behaviour interferes with your use-case, you can remove the metaclass.
class SquarespaceAuthenticator(OAuthAuthenticator, metaclass=SingletonMeta):
    """Authenticator class for Squarespace."""

    def __init__(
        self,
        stream: RESTStreamBase,
        auth_endpoint: Optional[str] = None,
        oauth_scopes: Optional[str] = None,
    ) -> None:
        super().__init__(
            stream=stream, auth_endpoint=auth_endpoint, oauth_scopes=oauth_scopes
        )
        self._tap = stream._tap

    @property
    def oauth_request_body(self) -> dict:
        """Define the OAuth request body for the Squarespace API."""
        return {
            "grant_type": "refresh_token",
            "refresh_token": self.config.get("refresh_token"),
        }

    @classmethod
    def create_for_stream(cls, stream) -> "SquarespaceAuthenticator":
        return cls(
            stream=stream,
            auth_endpoint="https://login.squarespace.com/api/1/login/oauth/provider/tokens",
        )
    
    def is_token_valid(self) -> bool:
        access_token = self._config.get("access_token")
        now = round(datetime.datetime.now(datetime.timezone.utc).timestamp())
        expires_in = self.expires_in or self._config.get("expires_in")
        if self.last_refreshed is None:
            return False
        if  expires_in is not None:
            expires_in = int(expires_in)
        if not access_token:
            return False

        if not expires_in:
            return False

        return not ((expires_in - now) < 120)

    def update_access_token(self) -> None:
        """Update `access_token` along with: `last_refreshed` and `expires_in`.

        Raises:
            RuntimeError: When OAuth login fails.
        """
        request_time = utc_now()
        auth_request_payload = self.oauth_request_payload
        token_response = requests.post(self.auth_endpoint, data=auth_request_payload, auth=(self.config.get('client_id'), self.config.get('client_secret')))
        try:
            token_response.raise_for_status()
            self.logger.info("OAuth authorization attempt was successful.")
        except Exception as ex:
            raise RuntimeError(
                f"Failed OAuth login, response was '{token_response.json()}'. {ex}"
            )
        token_json = token_response.json()
        self.access_token = token_json["access_token"]
        self._tap._config["access_token"] = self.access_token
        self.refresh_token = token_json["refresh_token"]
        self._tap._config["refresh_token"] = self.refresh_token
        self.expires_in = round(token_json.get("expires_in", self._default_expiration) + request_time.timestamp())
        if self.expires_in is None:
            self.logger.debug(
                "No expires_in receied in OAuth response and no "
                "default_expiration set. Token will be treated as if it never "
                "expires."
            )
        else:
            self._tap._config["expires_in"] = self.expires_in
        self.last_refreshed = request_time

        with open(self._tap.config_file, "w") as outfile:
            json.dump(self._tap._config, outfile, indent=4)
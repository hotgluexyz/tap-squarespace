"""Squarespace Authentication."""


from hotglue_singer_sdk.authenticators import OAuthAuthenticator, SingletonMeta


TOKEN_URL = "https://login.squarespace.com/api/1/login/oauth/provider/tokens"


# The SingletonMeta metaclass makes your streams reuse the same authenticator instance.
# If this behaviour interferes with your use-case, you can remove the metaclass.
class SquarespaceAuthenticator(OAuthAuthenticator, metaclass=SingletonMeta):
    """Authenticator class for Squarespace."""

    @property
    def oauth_request_body(self) -> dict:
        """Define the OAuth request body for the Squarespace API."""
        return {
            "grant_type": "refresh_token",
            "refresh_token": self.config.get("refresh_token"),
        }

    def request_auth(self):
        """Squarespace expects the client credentials as HTTP Basic auth."""
        return (self.client_id, self.client_secret)

    @classmethod
    def create_for_stream(cls, stream) -> "SquarespaceAuthenticator":
        return cls(stream=stream, auth_endpoint=TOKEN_URL)

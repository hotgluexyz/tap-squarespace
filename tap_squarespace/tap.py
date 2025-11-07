"""squarespace tap class."""

from typing import List

from singer_sdk import Tap, Stream
from singer_sdk import typing as th  # JSON schema typing helpers
# TODO: Import your custom stream types here:
from tap_squarespace.streams import (
    ProductStream,
    OrdersStream,
    SiteInfoStream,
    ProfilesStream

)
# TODO: Compile a list of custom stream types here
#       OR rewrite discover_streams() below with your custom logic.
STREAM_TYPES = [
    ProductStream,
    OrdersStream,
    SiteInfoStream,
    ProfilesStream
]


class Tapsquarespace(Tap):
    """squarespace tap class."""
    name = "tap-squarespace"

    def __init__(
        self,
        config=None,
        catalog=None,
        state=None,
        parse_env_config=False,
        validate_config=True,
    ) -> None:
        self.config_file = config[0]
        super().__init__(config, catalog, state, parse_env_config, validate_config)

    # TODO: Update this section with the actual config values you expect:
    config_jsonschema = th.PropertiesList(
        th.Property(
            "api_key",
            th.StringType,
            description="The token to authenticate against the API service"
        ),
        th.Property(
            "client_id",
            th.StringType,
            description="The client_id to authenticate against the API service"
        ),
        th.Property(
            "client_secret",
            th.StringType,
            description="The client_secret to authenticate against the API service"
        ),
        th.Property(
            "access_token",
            th.StringType,
            description="The access_token to authenticate against the API service"
        ),
        th.Property(
            "refresh_token",
            th.StringType,
            description="The refresh_token to authenticate against the API service"
        ),
        th.Property(
            "start_date",
            th.DateTimeType,
            description="The earliest record date to sync"
        )
    ).to_dict()

    def discover_streams(self) -> List[Stream]:
        """Return a list of discovered streams."""
        return [stream_class(tap=self) for stream_class in STREAM_TYPES]

if __name__ == "__main__":
    Tapsquarespace.cli()
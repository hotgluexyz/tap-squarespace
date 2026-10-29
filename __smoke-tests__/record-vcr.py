"""Record and replay Squarespace smoke tests."""

from hotglue_smoke_test.vcr.tap import VCRTapTestRunner


class SquarespaceTestRunner(VCRTapTestRunner):
    """Run recorded Squarespace smoke cases."""

    FILTER_HEADERS = [*VCRTapTestRunner.FILTER_HEADERS, "cookie"]

    PRESERVE_KEYS = {
        "modifiedOn",
        "hasNextPage",
        "nextPageCursor",
        "expires_in",
    }

    def module(self) -> str:
        """Return the tap CLI module."""
        return "tap_squarespace.tap"

    def launch(self):
        """Launch the Squarespace tap."""
        from tap_squarespace.tap import Tapsquarespace

        Tapsquarespace.cli()


if __name__ == "__main__":
    SquarespaceTestRunner.main()

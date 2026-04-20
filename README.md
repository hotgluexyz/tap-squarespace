# tap-squarespace

`tap-squarespace` is a Singer tap for squarespace.

Built with the [Meltano Tap SDK](https://sdk.meltano.com) for Singer Taps.

## Installation

- [ ] `Developer TODO:` Update the below as needed to correctly describe the install procedure. For instance, if you do not have a PyPi repo, or if you want users to directly install from your git repo, you can modify this step as appropriate.

```bash
pipx install tap-squarespace
```

## Configuration

| Name | Required | Description | Example |
|------|----------|-------------|---------|
| `api_key` | Required (API key auth) | Personal API key for Bearer token authentication | `xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx` |
| `client_id` | Required (OAuth) | OAuth application client ID | `xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx` |
| `client_secret` | Required (OAuth) | OAuth application client secret | `xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx` |
| `access_token` | Required (OAuth) | OAuth access token | `xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx` |
| `refresh_token` | Required (OAuth) | OAuth refresh token used to obtain new access tokens | `xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx` |
| `start_date` | No | Earliest record date to sync (ISO 8601 format) | `2024-01-01T00:00:00Z` |

The tap supports two authentication methods:

- **API key**: Provide only `api_key`. Squarespace personal API keys can be generated from your site's Advanced Settings.
- **OAuth**: Provide `client_id`, `client_secret`, `access_token`, and `refresh_token`. The tap will automatically refresh the access token using the refresh token when it expires.

### API key auth (simplest)

```json
{
  "api_key": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
  "start_date": "2024-01-01T00:00:00Z"
}
```

### OAuth auth

```json
{
  "client_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
  "client_secret": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
  "access_token": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
  "refresh_token": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
  "start_date": "2024-01-01T00:00:00Z"
}
```

## Usage

You can easily run `tap-squarespace` by itself or in a pipeline using [Meltano](https://meltano.com/).

### Executing the Tap Directly

```bash
tap-squarespace --version
tap-squarespace --help
tap-squarespace --config CONFIG --discover > ./catalog.json
```

## Developer Resources

- [ ] `Developer TODO:` As a first step, scan the entire project for the text "`TODO:`" and complete any recommended steps, deleting the "TODO" references once completed.

### Initialize your Development Environment

```bash
pipx install poetry
poetry install
```

### Create and Run Tests

Create tests within the `tap_squarespace/tests` subfolder and
  then run:

```bash
poetry run pytest
```

You can also test the `tap-squarespace` CLI interface directly using `poetry run`:

```bash
poetry run tap-squarespace --help
```

### Testing with [Meltano](https://www.meltano.com)

_**Note:** This tap will work in any Singer environment and does not require Meltano.
Examples here are for convenience and to streamline end-to-end orchestration scenarios._

Your project comes with a custom `meltano.yml` project file already created. Open the `meltano.yml` and follow any _"TODO"_ items listed in
the file.

Next, install Meltano (if you haven't already) and any needed plugins:

```bash
# Install meltano
pipx install meltano
# Initialize meltano within this directory
cd tap-squarespace
meltano install
```

Now you can test and orchestrate using Meltano:

```bash
# Test invocation:
meltano invoke tap-squarespace --version
# OR run a test `elt` pipeline:
meltano elt tap-squarespace target-jsonl
```

### SDK Dev Guide

See the [dev guide](https://sdk.meltano.com/en/latest/dev_guide.html) for more instructions on how to use the SDK to 
develop your own taps and targets.

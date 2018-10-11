"""Mock Abode Claims Response."""

from tests.mock import OAUTH_TOKEN


def get_response_ok(oauth_token=OAUTH_TOKEN):
    """Return the oauth2 claims token."""
    return '''
    {
        "token_type":"Bearer",
        "access_token":"''' + oauth_token + '''",
        "expires_in":3600
    }'''

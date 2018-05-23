"""
Mock responses that mimic actual data from Abode servers.

This file should be updated any time the Abode server responses
change so we can test that abodepy can still communicate.
"""

AUTH_TOKEN = 'web-1eb04ba2236d85f49d4b9b4bb91665f2'
OAUTH_TOKEN = 'eyJ0eXAiOiJKV1Qi'


def response_forbidden():
    """Return the invalid API key response json."""
    return '{"code":403,"message":"Invalid API Key"}'


def generic_response_ok():
    """
    Return the successful generic change response json.

    Used for settings changes.
    """
    return '{"code":200,"message":"OK"}'

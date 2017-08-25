"""
Mock devices that mimic actual data from Abode servers.

This file should be updated any time the Abode server responses
change so we can test that abodepy can still communicate.
"""

EMPTY_DEVICE_RESPONSE = '[]'


def status_put_response_ok(devid, status):
    """Return status change response json."""
    return '{"id": "' + devid + '", "status": "' + str(status) + '"}'


def level_put_response_ok(devid, level):
    """Return level change response json."""
    return '{"id": "' + devid + '", "level": "' + str(level) + '"}'

"""Mock Abode Automation."""

import abodepy.helpers.constants as CONST


def get_response_ok(aid, name, is_active, the_type, sub_type=""):
    """Return automation json."""
    return '''{
        "id": ''' + str(int(aid)) + ''',
        "name": "''' + name + '''",
        "actions": "a=1&m=2;",
        "condition": "HHMM_2300_2300",
        "is_active": "''' + str(int(is_active)) + '''",
        "sub_type": "''' + sub_type + '''",
        "type": "''' + the_type + '''",
        "notify_msg": null
  }'''


def put_response_ok(area='1', mode=CONST.MODE_STANDBY):
    """Return panel mode response json."""
    return '{"area": "' + area + '", "mode": "' + mode + '"}'

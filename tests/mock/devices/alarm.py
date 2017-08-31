"""
Mock Internal Alarm Device.

AbodePy creates an internal device that is a standard panel response that
includes a few required device fields. This is so that we can easily translate
the panel/alarm itself into a Home Assistant device.
"""
import json
import abodepy.helpers.constants as CONST

import tests.mock.panel as PANEL


def device(area='1', panel=PANEL.get_response_ok(mode=CONST.MODE_STANDBY)):
    """Alarm mock device."""
    alarm = json.loads(panel)
    alarm['name'] = CONST.ALARM_NAME
    alarm['id'] = CONST.ALARM_DEVICE_ID + area
    alarm['type'] = CONST.ALARM_TYPE
    alarm['type_tag'] = CONST.DEVICE_ALARM
    alarm['generic_type'] = CONST.TYPE_ALARM

    return alarm

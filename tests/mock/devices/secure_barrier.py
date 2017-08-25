"""Mock Abode Power Switch Sensor Device."""
import abodepy.helpers.constants as CONST

DEVICE_ID = 'ZW:0000000a'
CONTROL_URL = 'api/v1/control/power_switch/' + DEVICE_ID


def device(devid=DEVICE_ID,
           status=CONST.STATUS_OPEN,
           low_battery=False, no_response=False):
    """Secure barrier mock device."""
    return '''
        {
           "id":"''' + devid + '''",
           "type_tag":"device_type.secure_barrier",
           "type":"Secure Barrier",
           "name":"Garage Auto Door",
           "area":"1",
           "zone":"11",
           "sort_order":"0",
           "is_window":"0",
           "bypass":"0",
           "schar_24hr":"0",
           "sresp_mode_0":"0",
           "sresp_entry_0":"0",
           "sresp_exit_0":"0",
           "sresp_mode_1":"0",
           "sresp_entry_1":"0",
           "sresp_exit_1":"0",
           "sresp_mode_2":"0",
           "sresp_entry_2":"0",
           "sresp_exit_2":"0",
           "sresp_mode_3":"0",
           "sresp_entry_3":"0",
           "sresp_exit_3":"0",
           "capture_mode":null,
           "origin":"abode",
           "control_url":"''' + CONTROL_URL + '''",
           "deep_link":null,
           "status_color":"#5cb85c",
           "faults":{
              "low_battery":''' + str(int(low_battery)) + ''',
              "tempered":0,
              "supervision":0,
              "out_of_order":0,
              "no_response":''' + str(int(no_response)) + '''
           },
           "status":"''' + status + '''",
           "statuses":{
              "hvac_mode":null
           },
           "status_ex":"",
           "actions":[
              {
                 "label":"Close",
                 "value":"a=1&z=11&sw=off;"
              },
              {
                 "label":"Open",
                 "value":"a=1&z=11&sw=on;"
              }
           ],
           "status_icons":{
              "Open":"assets/icons/garage-door-red.svg",
              "Closed":"assets/icons/garage-door-green.svg"
           },
           "icon":"assets/icons/garage-door.svg"
        }'''

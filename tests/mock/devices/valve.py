"""Mock Abode Power Switch Sensor Device."""
import abodepy.helpers.constants as CONST

DEVICE_ID = 'ZW:00000113'
CONTROL_URL = 'api/v1/control/power_switch/' + DEVICE_ID


def device(devid=DEVICE_ID, status=CONST.STATUS_OPEN,
           low_battery=False, no_response=False):
    """Valve mock device."""
    return '''
      {
         "actions":[
            {
               "label":"Close",
               "value":"a=1&z=18&sw=off;"
            },
            {
               "label":"Open",
               "value":"a=1&z=18&sw=on;"
            }
         ],
         "area":"1",
         "bypass":"0",
         "control_url":"''' + CONTROL_URL + '''",
         "deep_link":null,
         "default_group_id":"1",
         "faults":{
            "low_battery":''' + str(int(low_battery)) + ''',
            "tempered":0,
            "supervision":0,
            "out_of_order":0,
            "no_response":''' + str(int(no_response)) + '''
         },
         "generic_type":"valve",
         "group_id":"xxxxx",
         "group_name":"Water leak",
         "has_subscription":null,
         "icon":"assets/icons/water-value-shutoff.svg",
         "id":"''' + devid + '''",
         "is_window":"",
         "name":"Water shut-off valve",
         "onboard":"0",
         "origin":"abode",
         "s2_dsk":"",
         "s2_grnt_keys":"",
         "s2_keys_valid":"",
         "s2_propty":"",
         "schar_24hr":"0",
         "sort_id":"6",
         "sort_order":"",
         "sresp_24hr":"0",
         "sresp_entry_0":"0",
         "sresp_entry_1":"0",
         "sresp_entry_2":"0",
         "sresp_entry_3":"0",
         "sresp_entry_4":"0",
         "sresp_exit_0":"0",
         "sresp_exit_1":"0",
         "sresp_exit_2":"0",
         "sresp_exit_3":"0",
         "sresp_exit_4":"0",
         "sresp_mode_0":"0",
         "sresp_mode_1":"0",
         "sresp_mode_2":"0",
         "sresp_mode_3":"0",
         "sresp_mode_4":"0",
         "status":"''' + status + '''",
         "status_color":"#5cb85c",
         "status_display":"Open",
         "status_ex":"",
         "status_icons":[

         ],
         "statuses":{
            "switch":"1"
         },
         "type":"Shutoff Valve",
         "type_tag":"device_type.valve",
         "uuid":"xxxxxxxxxxxxxxxxxxxxxxxxx",
         "version":"021f00030002",
         "zone":"18",
         "zwave_secure_protocol":""
      }'''

"""Mock Abode Door Lock Device."""
import abodepy.helpers.constants as CONST

DEVICE_ID = 'ZW:0000006'
CONTROL_URL = 'api/v1/control/lock/' + DEVICE_ID


def device(devid=DEVICE_ID, status=CONST.STATUS_LOCKCLOSED,
           low_battery=False, no_response=False):
    """Door lock mock device."""
    return '''
        {
          "id":"''' + devid + '''",
          "type_tag":"device_type.door_lock",
          "type":"Door Lock",
          "name":"Back Door Deadbolt",
          "area":"1",
          "zone":"7",
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
          "version":"",
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
                "label":"Lock",
                "value":"a=1&z=7&sw=on;"
             },
             {
                "label":"Unlock",
                "value":"a=1&z=7&sw=off;"
             }
          ],
          "status_icons":{
             "LockOpen":"assets/icons/unlocked-red.svg",
             "LockClosed":"assets/icons/locked-green.svg"
          },
          "automation_settings":null,
          "icon":"assets/icons/automation-lock.svg"
       }'''

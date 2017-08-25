"""Mock Abode Siren Device."""
import abodepy.helpers.constants as CONST

DEVICE_ID = 'ZB:0005674fff'


def device(devid=DEVICE_ID, status=CONST.STATUS_ONLINE,
           low_battery=False, no_response=False):
    """Siren mock device."""
    return '''
        {
          "id":"''' + devid + '''",
          "type_tag":"device_type.siren",
          "type":"Siren",
          "name":"Basement Siren",
          "area":"1",
          "zone":"8",
          "sort_order":null,
          "is_window":"",
          "bypass":"0",
          "schar_24hr":"0",
          "sresp_mode_0":"0",
          "sresp_entry_0":"0",
          "sresp_exit_0":"0",
          "sresp_mode_1":"5",
          "sresp_entry_1":"4",
          "sresp_exit_1":"0",
          "sresp_mode_2":"0",
          "sresp_entry_2":"4",
          "sresp_exit_2":"0",
          "sresp_mode_3":"0",
          "sresp_entry_3":"0",
          "sresp_exit_3":"0",
          "version":"852_00.00.03.05TC",
          "origin":"abode",
          "control_url":"",
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
          "actions":[],
          "status_icons":[
          ],
          "motion_event":"1",
          "wide_angle":"0",
          "icon":"assets/icons/indoor-siren.svg"
       }'''

"""Mock Abode Power Switch Sensor Device."""
import abodepy.helpers.constants as CONST

DEVICE_ID = 'ZW:00000007'
CONTROL_URL = 'api/v1/control/power_switch/' + DEVICE_ID


def device(devid=DEVICE_ID, status=CONST.STATUS_OFF,
           low_battery=False, no_response=False):
    """Power switch mock device."""
    return '''
        {
           "id":"''' + devid + '''",
           "type_tag":"device_type.power_switch_sensor",
           "type":"Power Switch Sensor",
           "name":"Back Porch Light",
           "area":"1",
           "zone":"32",
           "sort_order":null,
           "is_window":"",
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
                 "label":"Switch off",
                 "value":"a=1&z=32&sw=off;"
              },
              {
                 "label":"Switch on",
                 "value":"a=1&z=32&sw=on;"
              },
              {
                 "label":"Toggle",
                 "value":"a=1&z=32&sw=toggle;"
              },
              {
                 "label":"Switch on for 5 min",
                 "value":"a=1&z=32&sw=on&pd=5;"
              },
              {
                 "label":"Switch on for 10 min",
                 "value":"a=1&z=32&sw=on&pd=10;"
              },
              {
                 "label":"Switch on for 15 min",
                 "value":"a=1&z=32&sw=on&pd=15;"
              },
              {
                 "label":"Switch on for 20 min",
                 "value":"a=1&z=32&sw=on&pd=20;"
              },
              {
                 "label":"Switch on for 25 min",
                 "value":"a=1&z=32&sw=on&pd=25;"
              },
              {
                 "label":"Switch on for 30 min",
                 "value":"a=1&z=32&sw=on&pd=30;"
              },
              {
                 "label":"Switch on for 45 min",
                 "value":"a=1&z=32&sw=on&pd=45;"
              },
              {
                 "label":"Switch on for 1 hour",
                 "value":"a=1&z=32&sw=on&pd=60;"
              },
              {
                 "label":"Switch on for 2 hours",
                 "value":"a=1&z=32&sw=on&pd=120;"
              },
              {
                 "label":"Switch on for 5 hours",
                 "value":"a=1&z=32&sw=on&pd=300;"
              },
              {
                 "label":"Switch on for 8 hours",
                 "value":"a=1&z=32&sw=on&pd=480;"
              }
           ],
           "status_icons":[
           ],
           "icon":"assets/icons/plug.svg"
        }'''

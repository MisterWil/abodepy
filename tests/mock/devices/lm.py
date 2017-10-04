"""Mock Abode LM (Light/Temp/Humidity) Device."""
DEVICE_ID = 'ZB:eee888801'

TEMP_F = '72 °F'
TEMP_C = '72 °C'

LUX = '0 lx'

HUMIDITY = '42 %'


def device(devid=DEVICE_ID, status=TEMP_F,
           temp=TEMP_F, lux=LUX, humidity=HUMIDITY,
           low_battery=False, no_response=False):
    """PIR mock device."""
    return '''
        {
          "id":"''' + devid + '''",
          "type_tag":"device_type.lm",
          "type":"LM",
          "name":"Bedroom Temp",
          "area":"1",
          "zone":"15",
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
          "version":"LMHT_00.00.03.03TC",
          "origin":"abode",
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
          "statusEx": "0",
          "statuses":{
             "hvac_mode":null,
             "temperature": "''' + temp + '''",
             "lux": "''' + lux + '''",
             "humidity": "''' + humidity + '''"
          },
          "status_ex":"",
          "actions":[],
          "status_icons":[
          ],
          "icon":"assets/icons/unknown.svg"
       }'''

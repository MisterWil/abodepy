"""Mock Abode IP Camera Device."""
import abodepy.helpers.constants as CONST

DEVICE_ID = 'ZB:00000305'
CONTROL_URL = 'api/v1/cams/' + DEVICE_ID + '/record'
CONTROL_URL_SNAPSHOT = 'api/v1/cams/' + DEVICE_ID + '/capture'


def device(devid=DEVICE_ID, status=CONST.STATUS_ONLINE,
           low_battery=False, no_response=False):
    """IP camera mock device."""
    return '''
        {
          "id":"''' + devid + '''",
          "type_tag": "device_type.ipcam",
          "type": "IP Cam",
          "name": "Living Room Camera",
          "area": "1",
          "zone": "1",
          "sort_order": "",
          "is_window": "",
          "bypass": "0",
          "schar_24hr": "1",
          "sresp_24hr": "5",
          "sresp_mode_0": "0",
          "sresp_entry_0": "0",
          "sresp_exit_0": "0",
          "group_name": "Streaming Camera",
          "group_id": "397974",
          "default_group_id": "1",
          "sort_id": "10000",
          "sresp_mode_1": "0",
          "sresp_entry_1": "0",
          "sresp_exit_1": "0",
          "sresp_mode_2": "0",
          "sresp_entry_2": "0",
          "sresp_exit_2": "0",
          "sresp_mode_3": "0",
          "uuid": "123456789",
          "sresp_entry_3": "0",
          "sresp_exit_3": "0",
          "sresp_mode_4": "0",
          "sresp_entry_4": "0",
          "sresp_exit_4": "0",
          "version": "1.0.2.22G_6.8E_homekit_2.0.9_s2 ABODE oz",
          "origin": "abode",
          "has_subscription": null,
          "onboard": "1",
          "s2_grnt_keys": "",
          "s2_dsk": "",
          "s2_propty": "",
          "s2_keys_valid": "",
          "zwave_secure_protocol": "",
          "control_url":"''' + CONTROL_URL + '''",
          "deep_link": null,
          "status_color": "#5cb85c",
          "faults": {
              "low_battery":''' + str(int(low_battery)) + ''',
              "tempered": 0,
              "supervision": 0,
              "out_of_order": 0,
              "no_response":''' + str(int(no_response)) + ''',
              "jammed": 0,
              "zwave_fault": 0
          },
          "status": "Online",
          "status_display": "Online",
          "statuses": [],
          "status_ex": "",
          "actions": [
              {
                  "label": "Capture Video",
                  "value": "a=1&z=1&req=vid;"
              },
              {
                  "label": "Turn off Live Video",
                  "value": "a=1&z=1&privacy=on;"
              },
              {
                  "label": "Turn on Live Video",
                  "value": "a=1&z=1&privacy=off;"
              }
          ],
          "status_icons": [],
          "icon": "assets\/icons\/streaming-camaera-new.svg",
          "control_url_snapshot":"''' + CONTROL_URL_SNAPSHOT + '''",
          "ptt_supported": true,
          "is_new_camera": 1,
          "stream_quality": 3,
          "camera_mac": "AB:CD:EF:GF:HI",
          "privacy": "1",
          "enable_audio": "1",
          "alarm_video": "25",
          "pre_alarm_video": "5",
          "mic_volume": "75",
          "speaker_volume": "75",
          "mic_default_volume": 40,
          "speaker_default_volume": 46,
          "bandwidth": {
              "slider_labels": [
                  {
                      "name": "High",
                      "value": 3
                  },
                  {
                      "name": "Medium",
                      "value": 2
                  },
                  {
                      "name": "Low",
                      "value": 1
                  }
              ],
              "min": 1,
              "max": 3,
              "step": 1
          },
          "volume": {
              "min": 0,
              "max": 100,
              "step": 1
          },
          "video_flip": "0",
          "hframe": "1080P"
        }'''

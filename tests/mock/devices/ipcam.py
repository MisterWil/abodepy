"""Mock Abode IP Camera Device."""
import abodepy.helpers.constants as CONST

DEVICE_ID = 'ZB:00000305'
CONTROL_URL = 'api/v1/cams/' + DEVICE_ID + '/record'
CONTROL_URL_SNAPSHOT = 'api/v1/cams/' + DEVICE_ID + '/capture'


def device(devid=DEVICE_ID, status=CONST.STATUS_ONLINE,
           low_battery=False, no_response=False, privacy=1):
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
          "status":"''' + status + '''",
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
          "icon": "assets/icons/streaming-camaera-new.svg",
          "control_url_snapshot":"''' + CONTROL_URL_SNAPSHOT + '''",
          "ptt_supported": true,
          "is_new_camera": 1,
          "stream_quality": 3,
          "camera_mac": "AB:CD:EF:GF:HI",
          "privacy":"''' + str(privacy) + '''",
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


def get_capture_timeout():
    """Mock timeout response."""
    return '''
    {
        "code":600,
        "message":"Image Capture request has timed out.",
        "title":"",
        "detail":null
    }'''


FILE_PATH_ID = 'ZB00000305'
FILE_PATH = 'api/storage/' + FILE_PATH_ID + '/2020-01-26/173238/0.jpg'

LOCATION_HEADER = 'https://www.google.com/images/branding/googlelogo/' + \
    '1x/googlelogo_color_272x92dp.png'


def timeline_event(devid=DEVICE_ID, event_code='5001', file_path=FILE_PATH):
    """Camera Timeline Event Mockup."""
    return '''
    {
        "mac": "B0:C5:CZ:54:12:9A",
        "id": "1171272698",
        "xml": null,
        "date": "01/26/2020",
        "time": "05:32 PM",
        "event_utc": "1580088758",
        "event_cid": "",
        "event_code": "''' + event_code + '''",
        "device_id": "''' + devid + '''",
        "device_type_id": "69",
        "device_type": "IP Cam",
        "timeline_ha_device": null,
        "d_name": "Living Room Camera",
        "delete_by_user": null,
        "pin_code_user": " ",
        "file_del_at": "",
        "nest_has_motion": null,
        "nest_has_sound": null,
        "nest_has_person": null,
        "neaz": null,
        "hasFaults": "0",
        "file_path":"''' + file_path + '''",
        "deep_link": null,
        "file_name": "48755_b0c5ca37894b_2020-01-26_173238_0-M2+56431.jpg",
        "file_size": "197207",
        "file_count": "1",
        "file_is_del": "0",
        "event_type": "Image Capture",
        "severity": "6",
        "pos": "l",
        "color": "#40bbea",
        "is_alarm": "0",
        "triggered_by_str": null,
        "ha_type": null,
        "ha_device_name": null,
        "ha_location": null,
        "ha_mobile": null,
        "ha_cond": null,
        "h_location": null,
        "ha_trigger": null,
        "icon": "assets/email/motion-camera.png",
        "user_id": "95244",
        "user_name": "Shred",
        "mobile_name": "",
        "parent_tid": "",
        "app_type": "WebApp",
        "viewed_by_uid": null,
        "verified_by_tid": null,
        "la_applied_by": null,
        "la_event_type": null,
        "la_culprit_mobiles": null,
        "la_executed": null,
        "la_applied_at": null,
        "device_name": "Living Room Camera",
        "event_name": "Living Room Camera Image Capture",
        "event_by": "by Shred using WebApp",
        "file_delete_by": ""
    }'''

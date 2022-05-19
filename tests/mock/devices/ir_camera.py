"""Mock Abode IR Camera Device."""
import abodepy.helpers.constants as CONST

DEVICE_ID = 'ZB:00000005'
CONTROL_URL = 'api/v1/cams/' + DEVICE_ID + '/capture'


def device(devid=DEVICE_ID, status=CONST.STATUS_ONLINE,
           low_battery=False, no_response=False):
    """IR camera mock device."""
    return '''
        {
          "id":"''' + devid + '''",
          "type_tag":"device_type.ir_camera",
          "type":"Motion Camera",
          "name":"Downstairs Motion Camera",
          "area":"1",
          "zone":"3",
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
          "uuid": "1234567890",
          "version":"852_00.00.03.05TC",
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
                "label":"Auto Flash",
                "value":"a=1&z=3&req=img;"
             },
             {
                "label":"Never Flash",
                "value":"a=1&z=3&req=img_nf;"
             }
          ],
          "status_icons":[
          ],
          "motion_event":"1",
          "wide_angle":"0",
          "icon":"assets/icons/motioncamera-b.svg"
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


FILE_PATH_ID = 'ZB00000005'
FILE_PATH = 'api/storage/' + FILE_PATH_ID + '/2017-08-23/195505UTC/001.jpg'

LOCATION_HEADER = 'https://www.google.com/images/branding/googlelogo/' + \
    '1x/googlelogo_color_272x92dp.png'


def timeline_event(devid=DEVICE_ID, event_code='5001', file_path=FILE_PATH):
    """Camera Timeline Event Mockup."""
    return '''
    {
        "id": "71739948",
        "event_utc": "1503518105",
        "nest_activity_zones": null,
        "nest_has_motion": null,
        "nest_has_sound": null,
        "nest_has_person": null,
        "date": "08/23/2017",
        "time": "12:55 PM",
        "is_alarm": "0",
        "event_cid": "",
        "event_code": "''' + event_code + '''",
        "device_id": "''' + devid + '''",
        "device_type_id": "27",
        "device_type": "Motion Camera",
        "device_name": "Downstairs Motion Camera",
        "file_path":"''' + file_path + '''",
        "deep_link": null,
        "app_deep_link": null,
        "file_size": "30852",
        "file_count": "1",
        "file_is_del": "0",
        "event_type": "Image Capture",
        "severity": "6",
        "pos": "l",
        "color": "#40bbea",
        "viewed_by_uid": "",
        "user_id": "1234",
        "user_name": "Wil",
        "mobile_name": "",
        "parent_tid": "",
        "icon": "assets/email/motion-camera.png",
        "app_type": "WebApp",
        "file_del_at": "",
        "event_name": "Downstairs Motion Camera Image Capture",
        "event_by": ""
    }'''

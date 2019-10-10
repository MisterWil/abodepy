"""Mock Abode Panel Response."""

import abodepy.helpers.constants as CONST


def get_response_ok(mode=CONST.MODE_STANDBY, battery=False, is_cellular=False,
                    mac='00:11:22:33:44:55'):
    """Return panel response json."""
    return '''{
       "version":"ABGW 0.0.2.17F ABGW-L1-XA36J 3.1.2.6.1 Z-Wave 3.95",
       "report_account":"5555",
       "online":"1",
       "initialized":"1",
       "net_version":"ABGW 0.0.2.17F",
       "rf_version":"ABGW-L1-XA36J",
       "zigbee_version":"3.1.2.6.1",
       "z_wave_version":"Z-Wave 3.95",
       "timezone":"America/New_York",
       "ac_fail":"0",
       "battery":"''' + str(int(battery)) + '''",
       "ip":"192.168.1.1",
       "jam":"0",
       "rssi":"2",
       "setup_zone_1":"1",
       "setup_zone_2":"1",
       "setup_zone_3":"1",
       "setup_zone_4":"1",
       "setup_zone_5":"1",
       "setup_zone_6":"1",
       "setup_zone_7":"1",
       "setup_zone_8":"1",
       "setup_zone_9":"1",
       "setup_zone_10":"1",
       "setup_gateway":"1",
       "setup_contacts":"1",
       "setup_billing":"1",
       "setup_users":"1",
       "is_cellular":"''' + str(int(is_cellular)) + '''",
       "plan_set_id":"1",
       "dealer_id":"0",
       "tz_diff":"-04:00",
       "is_demo":"0",
       "rf51_version":"ABGW-L1-XA36J",
       "model":"L1",
       "mac":"''' + mac + '''",
       "xml_version":"3",
       "dealer_name":"abode",
       "id":"0",
       "dealer_address":"2625 Middlefield Road #900 Palo Alto CA 94306",
       "dealer_domain":"https://my.goabode.com",
       "domain_alias":"https://test.goabode.com",
       "dealer_support_url":"https://support.goabode.com",
       "app_launch_url":"https://goabode.app.link/abode",
       "has_wifi":"0",
       "mode":{
          "area_1":"''' + mode + '''",
          "area_2":"standby"
       }
    }'''


def put_response_ok(area='1', mode=CONST.MODE_STANDBY):
    """Return panel mode response json."""
    return '{"area": "' + area + '", "mode": "' + mode + '"}'

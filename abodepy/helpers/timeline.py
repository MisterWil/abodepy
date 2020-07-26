"""Timeline event constants."""

# Timeline event groups.

ALARM_GROUP = 'abode_alarm'
ALARM_END_GROUP = 'abode_alarm_end'
PANEL_FAULT_GROUP = 'abode_panel_fault'
PANEL_RESTORE_GROUP = 'abode_panel_restore'
DISARM_GROUP = 'abode_disarm'
ARM_GROUP = 'abode_arm'
ARM_FAULT_GROUP = 'abode_arm_fault'
TEST_GROUP = 'abode_test'
CAPTURE_GROUP = 'abode_capture'
DEVICE_GROUP = 'abode_device'
AUTOMATION_GROUP = 'abode_automation'
AUTOMATION_EDIT_GROUP = 'abode_automation_edited'

ALL_EVENT_GROUPS = [ALARM_GROUP, ALARM_END_GROUP, PANEL_FAULT_GROUP,
                    PANEL_RESTORE_GROUP, DISARM_GROUP, ARM_GROUP,
                    ARM_FAULT_GROUP, TEST_GROUP, CAPTURE_GROUP, DEVICE_GROUP,
                    AUTOMATION_GROUP, AUTOMATION_EDIT_GROUP]


def map_event_code(event_code):
    """Map a specific event_code to an event group."""
    event_code = int(event_code)

    # Honestly, these are just guessing based on the below event list.
    # It could be wrong, I have no idea.
    if 1100 <= event_code <= 1199:
        return ALARM_GROUP

    if 3100 <= event_code <= 3199:
        return ALARM_END_GROUP

    if 1300 <= event_code <= 1399:
        return PANEL_FAULT_GROUP

    if 3300 <= event_code <= 3399:
        return PANEL_RESTORE_GROUP

    if 1400 <= event_code <= 1499:
        return DISARM_GROUP

    if 3400 <= event_code <= 3799:
        return ARM_GROUP

    if 1600 <= event_code <= 1699:
        return TEST_GROUP

    if 5000 <= event_code <= 5099:
        return CAPTURE_GROUP

    if 5100 <= event_code <= 5199:
        return DEVICE_GROUP

    if 5200 <= event_code <= 5299:
        return AUTOMATION_GROUP

    if 6000 <= event_code <= 6100:
        return ARM_FAULT_GROUP

    return None


# Specific timeline events by event code.

ALL = {
    'event_code': '0',
    'event_type': 'All Timeline Events (AbodePy)'
}

MEDICAL = {
    'event_code': '1100',
    'event_type': 'Medical'
}

PERSONAL_EMERGENCY = {
    'event_code': '1101',
    'event_type': 'Personal Emergency'
}

FIRE_ALERT = {
    'event_code': '1110',
    'event_type': 'Fire Alert'
}

SMOKE_DETECTED = {
    'event_code': '1111',
    'event_type': 'Smoke Detected'
}

PANIC_ALERT = {
    'event_code': '1120',
    'event_type': 'Panic Alert'
}

DURESS_ALARM = {
    'event_code': '1121',
    'event_type': 'Duress Alarm'
}

SILENT_PANIC_ALERT = {
    'event_code': '1122',
    'event_type': 'Silent Panic Alert'
}

ALARM_TRIGGERED = {
    'event_code': '1130',
    'event_type': 'Alarm Triggered'
}

PERIMETER_ALARM_TRIGGERED = {
    'event_code': '1131',
    'event_type': 'Perimeter Alarm Triggered'
}

INTERIOR_ALARM_TRIGGERED = {
    'event_code': '1132',
    'event_type': 'Interior Alarm Triggered'
}

BURGLAR_ALARM_TRIGGERED = {
    'event_code': '1133',
    'event_type': 'Burglar Alarm Triggered'
}

OUTDOOR_ALARM_TRIGGERED = {
    'event_code': '1136',
    'event_type': 'Outdoor Alarm Triggered'
}

PANEL_TAMPER_SWITCH_TRIGGERED = {
    'event_code': '1137',
    'event_type': 'Panel Tamper Switch Triggered'
}

NOT_CONNECTED_TO_GATEWAY = {
    'event_code': '1147',
    'event_type': 'Not Connected to Gateway'
}

GAS_DETECTED = {
    'event_code': '1151',
    'event_type': 'Gas Detected'
}

WATER_LEAK_DETECTED = {
    'event_code': '1154',
    'event_type': 'Water Leak Detected'
}

CO_DETECTED = {
    'event_code': '1162',
    'event_type': 'CO Detected'
}

POWER_LOST = {
    'event_code': '1301',
    'event_type': 'Power Lost'
}

BATTERY_LOW = {
    'event_code': '1302',
    'event_type': 'Battery Low'
}

BATTERY_MISSING_DEAD = {
    'event_code': '1311',
    'event_type': 'Battery Missing/Dead'
}

JAM_DETECT = {
    'event_code': '1344',
    'event_type': 'Jam Detect/Signal Interference'
}

GPS_LOCATION_FAIL = {
    'event_code': '1354',
    'event_type': 'GPS Location Fail'
}

POLLING_FAILURE = {
    'event_code': '1355',
    'event_type': 'Polling Failure'
}

ARMED_WITH_FAULT = {
    'event_code': '1374',
    'event_type': 'Armed with Fault'
}

SENSOR_OFFLINE = {
    'event_code': '1380',
    'event_type': 'Sensor Offline'
}

SUPERVISION_FAIL = {
    'event_code': '1381',
    'event_type': 'Supervision Fail'
}

TAMPER_SWITCH_TRIGGERED = {
    'event_code': '1383',
    'event_type': 'Tamper Switch Triggered'
}

BATTERY_LOW = {
    'event_code': '1384',
    'event_type': 'Battery Low'
}

SYSTEM_DISARMED = {
    'event_code': '1400',
    'event_type': 'System Disarmed'
}

SYSTEM_DISARMED = {
    'event_code': '1401',
    'event_type': 'System Disarmed'
}

EVENT_CANCELED = {
    'event_code': '1406',
    'event_type': 'Event Canceled'
}

SYSTEM_DISARMED = {
    'event_code': '1407',
    'event_type': 'System Disarmed'
}

SET_UNSET_DISARM = {
    'event_code': '1408',
    'event_type': 'Set/Unset Disarm'
}

OFFLINE = {
    'event_code': '1447',
    'event_type': 'Offline'
}

FAIL_TO_CLOSE = {
    'event_code': '1454',
    'event_type': 'Fail to Close'
}

PARTIAL_ARM = {
    'event_code': '1456',
    'event_type': 'Partial Arm'
}

USER_ON_PREMISES = {
    'event_code': '1458',
    'event_type': 'User on Premises'
}

RECENT_CLOSE = {
    'event_code': '1459',
    'event_type': 'Recent Close'
}

ZONE_BYPASSED = {
    'event_code': '1570',
    'event_type': 'Zone Bypassed'
}

MANUAL_TEST_REPORT = {
    'event_code': '1601',
    'event_type': 'Manual Test Report'
}

PERIODIC_TEST = {
    'event_code': '1602',
    'event_type': 'Periodic Test'
}

POINT_TESTED_OK = {
    'event_code': '1611',
    'event_type': 'Point Tested OK/Technical Alarm'
}

CALL_REQUEST = {
    'event_code': '1616',
    'event_type': 'Call Request'
}

MOBILITY_ALARM = {
    'event_code': '1641',
    'event_type': 'Mobility Alarm/Sensor Watch Trouble'
}

GPS_LOCATION_HELP = {
    'event_code': '1645',
    'event_type': 'GPS Location Help'
}

GPS_LOCATION_REQUEST = {
    'event_code': '1646',
    'event_type': 'GPS Location Request'
}

GPS_LOCATION_TRACKER = {
    'event_code': '1647',
    'event_type': 'GPS Location Tracker'
}

SCREAM = {
    'event_code': '1648',
    'event_type': 'Scream'
}

MOBILE_UNIT_DISCONNECTED_FROM_BASE = {
    'event_code': '1649',
    'event_type': 'Mobile Unit Disconnected from Base'
}

TEST_REPORT = {
    'event_code': '1655',
    'event_type': 'Test Report'
}

ENTRY = {
    'event_code': '1704',
    'event_type': 'Entry'
}

DC_OPEN_MOBILITY = {
    'event_code': '1750',
    'event_type': 'DC Open - Mobility'
}

IR_ACTIVITY_MOBILITY = {
    'event_code': '1751',
    'event_type': 'IR Activity - Mobility'
}

SIREN_ON = {
    'event_code': '1752',
    'event_type': 'Siren On'
}

MOTION_DETECTED_AREA_2 = {
    'event_code': '1788',
    'event_type': 'Motion Detected Area 2'
}

MOTION_DETECTED_AREA_1 = {
    'event_code': '1789',
    'event_type': 'Motion Detected Area 1'
}

PANEL_TAMPER_SWITCH_RESTORED = {
    'event_code': '3137',
    'event_type': 'Panel Tamper Switch Restored'
}

RECONNECTED_TO_GATEWAY = {
    'event_code': '3147',
    'event_type': 'Re-Connected to Gateway'
}

POWER_RESTORED = {
    'event_code': '3301',
    'event_type': 'Power Restored'
}

BATTERY_NORMAL = {
    'event_code': '3302',
    'event_type': 'Battery Normal/OK'
}

BATTERY_NORMAL = {
    'event_code': '3311',
    'event_type': 'Battery Normal/OK'
}

SIGNAL_RESTORED = {
    'event_code': '3344',
    'event_type': 'No Jam/Signal Restored'
}

NET_DEVICE_FAILURE_RESTORED = {
    'event_code': '3354',
    'event_type': 'NET Device Failure Restored'
}

POLLING_FAILURE_RESTORED = {
    'event_code': '3355',
    'event_type': 'Polling Failure Restored'
}

TAMPER_SWITCH_RESTORED = {
    'event_code': '3383',
    'event_type': 'Tamper Switch Restored'
}

BATTERY_NORMAL = {
    'event_code': '3384',
    'event_type': 'Battery Normal/OK'
}

SYSTEM_ARMED = {
    'event_code': '3400',
    'event_type': 'System Armed'
}

SYSTEM_ARMED_AWAY = {
    'event_code': '3401',
    'event_type': 'System Armed - Away'
}

SYSTEM_ARMED = {
    'event_code': '3407',
    'event_type': 'System Armed'
}

SET_UNSET_ARM = {
    'event_code': '3408',
    'event_type': 'Set/Unset Arm'
}

ONLINE = {
    'event_code': '3447',
    'event_type': 'Online'
}

SYSTEM_ARMED_HOME = {
    'event_code': '3456',
    'event_type': 'System Armed - Home'
}

MOBILE_UNIT_CONNECTED_TO_BASE = {
    'event_code': '3649',
    'event_type': 'Mobile Unit Connected to Base'
}

DC_CLOSE_MOBILITY = {
    'event_code': '3750',
    'event_type': 'DC Close - Mobility'
}

SIREN_OFF = {
    'event_code': '3752',
    'event_type': 'Siren Off'
}

SYSTEM_ARMED_HOME = {
    'event_code': '3758',
    'event_type': 'System Armed - Home'
}

VEVENT_CODEEO = {
    'event_code': '5000',
    'event_type': 'Vevent_codeeo'
}

CAPTURE_IMAGE = {
    'event_code': '5001',
    'event_type': 'Capture Image'
}

BURGLAR_VEVENT_CODEEO = {
    'event_code': '5002',
    'event_type': 'Burglar Vevent_codeeo'
}

BURGLAR_CAPTURE_IMAGE = {
    'event_code': '5003',
    'event_type': 'Burglar Capture Image'
}

OPENED = {
    'event_code': '5100',
    'event_type': 'Opened'
}

CLOSED = {
    'event_code': '5101',
    'event_type': 'Closed'
}

UNLOCKED = {
    'event_code': '5110',
    'event_type': 'Unlocked'
}

LOCKED = {
    'event_code': '5111',
    'event_type': 'Locked'
}

STATUS_AUTOMATION = {
    'event_code': '5201',
    'event_type': 'Status Automation'
}

SCHEDULED_AUTOMATION = {
    'event_code': '5202',
    'event_type': 'Scheduled Automation'
}

LOCATION_AUTOMATION = {
    'event_code': '5203',
    'event_type': 'Location Automation'
}

QUICK_ACTION = {
    'event_code': '5204',
    'event_type': 'Quick Action'
}

AUTOMATION = {
    'event_code': '5206',
    'event_type': 'Automation'
}

ARMING_WITH_FAULT_AWAY = {
    'event_code': '6055',
    'event_type': 'Exit Time Started - Arming w/ Faults - Away'
}

ARMED_WITH_FAULT_AWAY = {
    'event_code': '6071',
    'event_type': 'Armed w/ Faults - Away'
}

ARMED_WITH_FAULT_HOME = {
    'event_code': '6077',
    'event_type': 'Armed w/ Faults - Home'
}

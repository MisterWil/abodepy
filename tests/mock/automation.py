"""Mock Abode Automation."""


def get_response_ok(name, enabled, aid):
    """Return automation json."""
    return '''{
        "name": "''' + name + '''",
        "enabled": "''' + str(enabled) + '''",
        "version": 2,
        "id": "''' + aid + '''",
        "subType": "",
        "actions": [{
            "directive": {
                "trait": "panel.traits.panelMode",
                "name": "panel.directives.arm",
                "state": {
                    "panelMode": "AWAY"
                }
            }
        }],
        "conditions": {},
        "triggers": {
            "operator": "OR",
            "expressions": [{
                "mobileDevices": ["89381", "658"],
                "property": {
                    "trait": "mobile.traits.location",
                    "name": "location",
                    "rule": {
                        "location": "31675",
                        "equalTo": "LAST_OUT"
                    }
                }
            }]
        }
    }'''

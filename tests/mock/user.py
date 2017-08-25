"""Mock Abode User Response."""


def get_response_ok():
    """Return the user response data."""
    return '''{
        "id":"user@email.com",
        "email":"user@email.com",
        "first_name":"John",
        "last_name":"Doe",
        "phone":"5555551212",
        "profile_pic":"https://website.com/default-image.svg",
        "address":"555 None St.",
        "city":"New York City",
        "state":"NY",
        "zip":"10108",
        "country":"US",
        "longitude":"0",
        "latitude":"0",
        "timezone":"America/New_York_City",
        "verified":"1",
        "plan":"Basic",
        "plan_id":"0",
        "plan_active":"1",
        "cms_code":"1111",
        "cms_active":"0",
        "cms_started_at":"",
        "cms_expiry":"",
        "cms_ondemand":"",
        "step":"-1",
        "cms_permit_no":"",
        "opted_plan_id":"",
        "stripe_account":"1",
        "plan_effective_from":"",
        "agreement":"1",
        "associate_users":"1",
        "owner":"1"
        }'''

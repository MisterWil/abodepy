def test_alarm_device(abode):
    device = abode.get_alarm();

    assert device

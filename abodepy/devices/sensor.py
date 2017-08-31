"""Abode sensor device."""

from abodepy.devices.binary_sensor import AbodeBinarySensor
import abodepy.helpers.constants as CONST


class AbodeSensor(AbodeBinarySensor):
    """Class to represent a sensor device."""

    @property
    def motion(self):
        """Motion detected."""
        value = self._json_state.get(CONST.MOTION_STATUS_KEY)
        if value:
            return int(value) == 1
        return None

    @property
    def occupancy(self):
        """Occupancy detected."""
        value = self._json_state.get(CONST.OCCUPANCY_STATUS_KEY)
        if value:
            return int(value) == 1
        return None

    @property
    def temp(self):
        """Get device temp."""
        return self._json_state.get(CONST.TEMP_STATUS_KEY)

    @property
    def temp_unit(self):
        """Get unit of temp."""
        return CONST.UNIT_FAHRENHEIT

    @property
    def humidity(self):
        """Get device humdity."""
        return self._json_state.get(CONST.HUMI_STATUS_KEY)

    @property
    def humidity_unit(self):
        """Get unit of humidity."""
        return CONST.UNIT_PERCENT

    @property
    def lux(self):
        """Get device lux."""
        return self._json_state.get(CONST.LUX_STATUS_KEY)

    @property
    def lux_unit(self):
        """Get unit of lux."""
        # I mean, it's called lux right?
        return CONST.UNIT_LUX

    @property
    def has_temp(self):
        """Device reports temperature."""
        return self.temp is True

    @property
    def has_humidity(self):
        """Device reports humidity level."""
        return self.humidity is True

    @property
    def has_lux(self):
        """Device reports light lux level."""
        return self.lux is True

    @property
    def has_motion(self):
        """Device reports motion."""
        return self.motion is not None

    @property
    def has_occupancy(self):
        """Device reports occupancy."""
        return self.occupancy is not None

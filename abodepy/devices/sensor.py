"""Abode sensor device."""
import re

from abodepy.devices.binary_sensor import AbodeBinarySensor
import abodepy.helpers.constants as CONST


class AbodeSensor(AbodeBinarySensor):
    """Class to represent a sensor device."""

    def _get_status(self, key):
        return self._json_state.get(CONST.STATUSES_KEY, {}).get(key)

    def _get_numeric_status(self, key):
        """Extract the numeric value from the statuses object."""
        value = self._get_status(key)

        if value and any(i.isdigit() for i in value):
            return float(re.sub("[^0-9.]", "", value))
        return None

    @property
    def temp(self):
        """Get device temp."""
        return self._get_numeric_status(CONST.TEMP_STATUS_KEY)

    @property
    def temp_unit(self):
        """Get unit of temp."""
        if CONST.UNIT_FAHRENHEIT in self._get_status(CONST.TEMP_STATUS_KEY):
            return CONST.UNIT_FAHRENHEIT

        if CONST.UNIT_CELSIUS in self._get_status(CONST.TEMP_STATUS_KEY):
            return CONST.UNIT_CELSIUS

        return None

    @property
    def humidity(self):
        """Get device humdity."""
        return self._get_numeric_status(CONST.HUMI_STATUS_KEY)

    @property
    def humidity_unit(self):
        """Get unit of humidity."""
        if CONST.UNIT_PERCENT in self._get_status(CONST.HUMI_STATUS_KEY):
            return CONST.UNIT_PERCENT
        return None

    @property
    def lux(self):
        """Get device lux."""
        return self._get_numeric_status(CONST.LUX_STATUS_KEY)

    @property
    def lux_unit(self):
        """Get unit of lux."""
        if CONST.UNIT_LUX in self._get_status(CONST.LUX_STATUS_KEY):
            return CONST.LUX
        return None

    @property
    def has_temp(self):
        """Device reports temperature."""
        return self.temp is not None

    @property
    def has_humidity(self):
        """Device reports humidity level."""
        return self.humidity is not None

    @property
    def has_lux(self):
        """Device reports light lux level."""
        return self.lux is not None

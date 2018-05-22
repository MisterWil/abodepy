"""Abode switch device."""

from abodepy.devices.switch import AbodeSwitch
import abodepy.helpers.constants as CONST


class AbodeLight(AbodeSwitch):
    """Class for lights (dimmers)."""

    @property
    def brightness(self):
        """Get light brightness."""
        return self._json_state.get(CONST.BRIGHTNESS_KEY)

    @property
    def color_temp(self):
        """Get light color temp."""
        # This value still exist in device JSON even when using color mode
        return self._json_state.get(CONST.STATUSES_KEY)['color_temp']

    @property
    def color(self):
        """Get light color."""
        # These values exist in device JSON even when not using color mode
        return (self._json_state.get(CONST.STATUSES_KEY)['hue'],
                self._json_state.get(CONST.STATUSES_KEY)['saturation'])

    @property
    def has_brightness(self):
        """Device has brightness."""
        return self.brightness

    @property
    def has_color(self):
        """Device is using color mode."""
        # color_mode of 0 means it's on, color_mode of 2 means it's off
        if self._json_state.get(CONST.STATUSES_KEY)['color_mode'] == '0':
            return True

    @property
    def is_color_capable(self):
        """Device is color compatible."""
        return 'RGB' in self._type

    @property
    def is_dimmable(self):
        """Device is dimmable."""
        return 'Dimmer' in self._type

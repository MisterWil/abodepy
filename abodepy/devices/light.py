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
        return self._json_state.get(CONST.STATUSES_KEY)['color_temp']

    @property
    def color(self):
        """Get light color."""
        return (self._json_state.get(CONST.STATUSES_KEY)['hue'],
                self._json_state.get(CONST.STATUSES_KEY)['saturation'])

    @property
    def has_brightness(self):
        """Device has brightness."""
        return self.brightness

    @property
    def has_color(self):
        """Device is using color mode."""
        if (self._json_state.get(CONST.STATUSES_KEY)['color_mode']
                == str(CONST.COLOR_MODE_ON)):
            return True

    @property
    def is_color_capable(self):
        """Device is color compatible."""
        return 'RGB' in self._type

    @property
    def is_dimmable(self):
        """Device is dimmable."""
        return 'Dimmer' in self._type

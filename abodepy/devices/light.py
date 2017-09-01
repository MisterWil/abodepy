"""Abode switch device."""

from abodepy.devices.switch import AbodeSwitch
import abodepy.helpers.constants as CONST


class AbodeLight(AbodeSwitch):
    """Class for lights (dimmers)."""

    def set_color(self, _color):
        """Set the color of the light."""
        # Not implemented
        return self.has_color

    @property
    def brightness(self):
        """Get light brightness."""
        return self._json_state.get(CONST.BRIGHTNESS_KEY)

    @property
    def color(self):
        """Get light color."""
        return self._json_state.get(CONST.COLOR_KEY)

    @property
    def has_brightness(self):
        """Device has brightness."""
        return self.brightness is True

    @property
    def has_color(self):
        """Device has color."""
        return self.color is True

    @property
    def is_dimmable(self):
        """Device is dimmable."""
        return self.has_brightness

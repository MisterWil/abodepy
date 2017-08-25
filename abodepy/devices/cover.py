"""Abode cover device."""

from abodepy.devices.switch import AbodeSwitch
import abodepy.helpers.constants as CONST


class AbodeCover(AbodeSwitch):
    """Class to add cover functionality."""

    def switch_on(self):
        """Turn the switch on."""
        success = self.set_status(CONST.STATUS_OPEN_INT)

        if success:
            self._json_state['status'] = CONST.STATUS_OPEN

        return success

    def switch_off(self):
        """Turn the switch off."""
        success = self.set_status(CONST.STATUS_CLOSED_INT)

        if success:
            self._json_state['status'] = CONST.STATUS_CLOSED

        return success

    def open_cover(self):
        """Open the cover."""
        return self.switch_on()

    def close_cover(self):
        """Close the cover."""
        return self.switch_off()

    @property
    def is_open(self):
        """Get if the cover is open."""
        return self.is_on

    @property
    def is_on(self):
        """
        Get cover state.

        Assume cover is open.
        """
        return self.status not in CONST.STATUS_CLOSED

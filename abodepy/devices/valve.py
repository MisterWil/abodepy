"""Abode valve device."""

from abodepy.devices.switch import AbodeSwitch
import abodepy.helpers.constants as CONST


class AbodeValve(AbodeSwitch):
    """Class to add valve functionality."""

    def switch_on(self):
        """Open the valve."""
        success = self.set_status(CONST.STATUS_ON_INT)

        if success:
            self._json_state['status'] = CONST.STATUS_OPEN

        return success

    def switch_off(self):
        """Close the valve."""
        success = self.set_status(CONST.STATUS_OFF_INT)

        if success:
            self._json_state['status'] = CONST.STATUS_CLOSED

        return success

    @property
    def is_on(self):
        """
        Get switch state.

        Assume switch is on.
        """
        return self.status not in (CONST.STATUS_CLOSED, CONST.STATUS_OFFLINE)

    @property
    def is_dimmable(self):
        """Device dimmable."""
        return False

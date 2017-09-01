"""Abode switch device."""

from abodepy.devices import AbodeDevice
import abodepy.helpers.constants as CONST


class AbodeSwitch(AbodeDevice):
    """Class to add switch functionality."""

    def switch_on(self):
        """Turn the switch on."""
        success = self.set_status(CONST.STATUS_ON_INT)

        if success:
            self._json_state['status'] = CONST.STATUS_ON

        return success

    def switch_off(self):
        """Turn the switch off."""
        success = self.set_status(CONST.STATUS_OFF_INT)

        if success:
            self._json_state['status'] = CONST.STATUS_OFF

        return success

    @property
    def is_on(self):
        """
        Get switch state.

        Assume switch is on.
        """
        return self.status not in (CONST.STATUS_OFF, CONST.STATUS_OFFLINE)

    @property
    def is_dimmable(self):
        """Device dimmable."""
        return False

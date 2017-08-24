"""Abode cover device."""

from abodepy.devices.switch import AbodeDevice
import abodepy.helpers.constants as CONST


class AbodeLock(AbodeDevice):
    """Class to represent a door lock."""

    def lock(self):
        """Lock the device."""
        success = self.set_status('1')

        if success:
            self._json_state['status'] = CONST.STATUS_LOCKCLOSED

        return success

    def unlock(self):
        """Unlock the device."""
        success = self.set_status('0')

        if success:
            self._json_state['status'] = CONST.STATUS_LOCKOPEN

        return success

    @property
    def is_locked(self):
        """Get locked state."""
        # Err on side of caution; assume if lock isn't explicitly
        # 'LockClosed' then it's open
        return self.status in CONST.STATUS_LOCKCLOSED

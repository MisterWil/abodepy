"""Abode binary sensor device."""

from abodepy.devices import AbodeDevice
import abodepy.helpers.constants as CONST


class AbodeBinarySensor(AbodeDevice):
    """Class to represent an on / off, online/offline sensor."""

    @property
    def is_on(self):
        """
        Get sensor state.

        Assume offline or open (worst case).
        """
        return self.status not in (CONST.STATUS_OFF, CONST.STATUS_OFFLINE,
                                   CONST.STATUS_CLOSED)

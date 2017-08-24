"""Abode cover device."""

from abodepy.devices.switch import AbodeSwitch
import abodepy.helpers.constants as CONST


class AbodeCover(AbodeSwitch):
    """Class to add cover functionality."""

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

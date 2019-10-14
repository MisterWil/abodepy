"""Abodepy utility methods."""
import logging
import pickle
import uuid

_LOGGER = logging.getLogger(__name__)


def save_cache(data, filename):
    """Save cookies to a file."""
    with open(filename, 'wb') as handle:
        pickle.dump(data, handle)


def load_cache(filename):
    """Load cookies from a file."""
    with open(filename, 'rb') as handle:
        try:
            return pickle.load(handle)
        except EOFError:
            _LOGGER.warning("Empty pickle file: %s", filename)
        except (pickle.UnpicklingError, ValueError):
            _LOGGER.warning("Corrupted pickle file: %s", filename)

        return None


def gen_uuid():
    """Generate a new Abode UUID."""
    return str(uuid.uuid1())


def update(dct, dct_merge):
    """Recursively merge dicts."""
    for key, value in dct_merge.items():
        if key in dct and isinstance(dct[key], dict):
            dct[key] = update(dct[key], value)
        else:
            dct[key] = value
    return dct

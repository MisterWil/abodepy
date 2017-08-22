Changelog
-----------

A list of changes between each release.

0.8.0 (2017-08-22)
^^^^^^^^^^^^^^^^^^
- Refactored almost the entire package layout
- Command line is now called with the 'abodepy' command directly
- Cleaned up command line help
- Changed --setting to --set, --switchOn to --on, and --switchOff to --off
- Modified get_devices() to update existing devices instead of creating new ones every time
- Added additional property methods
- Added support for more device types

0.7.2 (2017-08-21)
^^^^^^^^^^^^^^^^^^
- Small bug fix release regarding event callbacks for HASS testing

0.7.1 (2017-08-21)
^^^^^^^^^^^^^^^^^^
- Added siren settings for Issue #1

0.7.0 (2017-08-21)
^^^^^^^^^^^^^^^^^^
- Wrote tests for setting changes
- Upgraded to correct version of socketio_client3, fixing Issue #4
- Added switchOn, switchOff, lock, and unlock command line arguments
- Now including abodecl with package for Issue #2
- Modified abodepy to also execute abodecl as part of its main method.

0.6.0 (2017-08-20)
^^^^^^^^^^^^^^^^^^
- Added settings changes for Issue #1
- Merge pull request #4 from amelchio/origin-slash

0.5.1 (2017-06-11)
^^^^^^^^^^^^^^^^^^
- Now referencing forked socketIO_client3.

0.5.0 (2017-06-11)
^^^^^^^^^^^^^^^^^^
- Fixed socketio errors.
  Apparently Abode updated to Socket IO 2.0 which was broken with socketio_client 0.7.2. Someone luckily fixed it in their own git repo so I am now referencing their git repo in which they released 0.7.3.

0.4.0 (2017-06-05)
^^^^^^^^^^^^^^^^^^
- Rewrote a lot of the SocketIO code to better handle connection errors.
- Now manages to recover from connection errors cleanly and shutdown is smoother.
- Added additional logging statements throughout.
- Added --verbose command line argument to output info-level abodepy logs.

0.3.0 (2017-06-03)
^^^^^^^^^^^^^^^^^^
- More tests
- Cleaner code (thanks pylint)
- Likely ready to start implementing in HASS

0.2.0 (2017-06-01)
^^^^^^^^^^^^^^^^^^
- Added tests for the alarm device
- Added mock responses for several other devices for tests that will be written
- Reworked a significant chunk of the code to be more python-y.
- Fixed a hand-full of bugs found while writing tests.

0.1.0 (2017-05-27)
^^^^^^^^^^^^^^^^^^
- Initial release of abodepy
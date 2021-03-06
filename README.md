[![Travis CI][Travis-badge]](https://travis-ci.org/kcjengr/qtpyvcp)
[![LinuxCNC 2.8][linuxcnc-badge]](https://github.com/LinuxCNC/linuxcnc)
[![Chat on IRC ][irc-badge]](https://kiwiirc.com/client/irc.kiwiirc.com/hazzy)

[Travis-badge]: https://img.shields.io/travis/kcjengr/qtpyvcp/master.svg?label=docs
[linuxcnc-badge]: https://img.shields.io/badge/LinuxCNC-%202.8-blue.svg
[irc-badge]: https://img.shields.io/badge/Chat%20on%20IRC-%23hazzy-green.svg


# QtPyVCP: A VCP toolkit for LinuxCNC

QtPyVCP is a Virtual Control Panel toolkit for LinuxCNC based on PyQt5
and coded in Python. It leverages QtDesigner and it's custom widget
support to make develop of no-code custom VCPs easy and advanced
VCPs possible.


## Installation and Usage

See the [documentation](https://kcjengr.github.io/qtpyvcp/).


## Resources

* [Development](https://github.com/kcjengr/qtpyvcp/)
* [Documentation](https://kcjengr.github.io/qtpyvcp/)
* [Freenode IRC](http://webchat.freenode.net/?channels=%23hazzy) (#hazzy)
* [Issue Tracker](https://github.com/kcjengr/qtpyvcp/issues)


## Dependancies

* LinuxCNC master (2.8~pre)
* Python 2.7
* PyQt5

QtPyVCP is developed and tested using the LinuxCNC Debian 9 (stretch)
[Live ISO](http://www.linuxcnc.org/testing-stretch-rtpreempt/). It should run
on any system that can have PyQt5 installed, but Debian 9 is the only OS
that is officially supported.


## DISCLAIMER

THE AUTHORS OF THIS SOFTWARE ACCEPT ABSOLUTELY NO LIABILITY FOR
ANY HARM OR LOSS RESULTING FROM ITS USE.  IT IS _EXTREMELY_ UNWISE
TO RELY ON SOFTWARE ALONE FOR SAFETY.  Any machinery capable of
harming persons must have provisions for completely removing power
from all motors, etc, before persons enter any danger area.  All
machinery must be designed to comply with local and national safety
codes, and the authors of this software can not, and do not, take
any responsibility for such compliance.

This software is released under the GPLv2.

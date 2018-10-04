"""
{vcp_name} - A QtPyVCP based Virtual Control Panel for LinuxCNC.

Usage:
  {vcp_cmd} --ini=INI [--log-level=LEVEL] [--log-file=FILE] [--perfmon]
            [--theme=THEME] [--stylesheet=SYTLESHEET] [--pref-file=FILE]
            [--size=WIDTHxHEIGHT] [--position=XPOSxYPOS]
            [--fullscreen] [--maximize] [--hide-menu-bar] [--hide-status-bar]
  {vcp_cmd} (-h | --help)
  {vcp_cmd} (-v | --version)

Required Arguments:
  --ini INI          Path to INI file, relative to ~/linuxcnc/configs.

Display  Options:
  --theme=THEME      The Qt theme to use, defaults to system theme.
  --stylesheet=STYLESHEET
                     Path to QSS file containing styles to be applied
                     to specific Qt and/or QtPyVCP widget classes.
  --size=WIDTHxHEIGHT
                     Initial size of the window in pixels.
  --position=XPOSxYPOS
                     Initial position of the window, specified as the
                     coordinates of the top left corner of the window
                     relative to the top left corner of the screen.
  -f --fullscreen    Flag to start with window fullscreen.
  -m --maximize      Flag to start with window maximized.
  --hide-menu-bar    Hides the menu bar, if present.
  --hide-status-bar  Hides the status bar, if present.

Application Options:
  --log-level=(DEBUG | INFO | WARN | ERROR | CRITICAL)
                     Sets the log level. [default: INFO]
  --log-file=FILE    Specifies the log file. Overrides INI setting.
  --pref-file=FILE   Specifies the preference file. Overrides INI setting.
  --perfmon          Monitor and log system performance.
  --command_line_args <args>...

General Options:
  -h --help          Show this help and exit.
  -v --version       Show version.

Note:
  When specifying {vcp_name} in the INI using [DISPLAY]DISPLAY={vcp_cmd} [...]
  the --ini parameter will be passed by the linuxcnc startup script so does
  not need to be specified.

"""
import os
import sys
from linuxcnc import ini
from docopt import docopt

from QtPyVCP import __version__
from QtPyVCP.utilities.misc import normalizePath

def parse_opts(doc=__doc__, vcp_name='NotSpecified', vcp_cmd='notspecified', vcp_version=None):
    # LinuxCNC passes the INI file as `-ini=inifile` which docopt sees as a
    # short argument which does not support an equals sign, so we loop thru
    # and add another dash to the ini argument if needed.
    for index, item in enumerate(sys.argv):
        if item.startswith('-ini'):
            sys.argv[index] = '-' + item
            break

    version_str = 'QtPyVCP v{}'.format(__version__)
    if vcp_version is not None:
        version_str += ', {} v{}'.format(vcp_name, vcp_version)

    doc = doc.format(vcp_name=vcp_name, vcp_cmd=vcp_cmd)

    raw_args = docopt(doc, version=version_str)

    # convert raw argument dict keys to valid python attribute names
    opts = OptDict({arg.strip('-<>').replace('-', '_') : value for arg, value in raw_args.items()})

    # read options from INI file and merge with cmd line options
    ini_file = ini(normalizePath(opts.ini, os.path.expanduser('~/linuxcnc/configs')))
    for k, v in opts.iteritems():
        ini_val = ini_file.find('DISPLAY', k.upper())
        if ini_val is None:
            continue

        # convert str values to bool
        if type(v) == bool:
            # TODO: Find a way to prefer cmd line values over INI values
            ini_val = ini_val.lower() in ['true', '1', 'on']

        # if its a non bool value and it was specified on the cmd line
        # then prefer the cmd line value
        elif v is not None:
            continue

        opts[k] = ini_val

    # Check if LinuxCNC is running
    if not os.path.isfile('/tmp/linuxcnc.lock'):
        # LinuxCNC is running, but in a different environment.
        # TODO: find some way to get the INI file LCNC was launched with
        print 'LinuxCNC must be running to launch a VCP'
        sys.exit()

    # setup the environment variables
    ini_file = os.environ.get('INI_FILE_NAME') or opts.ini
    if ini_file is None:
        # LinuxCNC is not running
        # TODO: Maybe launch LinuxCNC using subprocess
        print 'LinuxCNC is not running, no INI file specified on command line'
        sys.exit()

    if not os.getenv('INI_FILE_NAME'):
        base_path = os.path.expanduser('~/linuxcnc/configs')
        ini_file = os.path.realpath(normalizePath(ini_file, base_path))
        if not os.path.exists(ini_file):
            print 'Specifed INI file does not exist: {}'.format(ini_file)
            sys.exit()
        os.environ['INI_FILE_NAME'] = ini_file
        os.environ['CONFIG_DIR'] = os.path.dirname(ini_file)

    # show the chooser if the --chooser flag was specified
    if opts.chooser or not opts.get('vcp', True):
        from vcp_launcher.vcp_chooser import VCPChooser
        from PyQt5.QtWidgets import QApplication
        app = QApplication([])
        result = VCPChooser(opts).exec_()
        if result == VCPChooser.Rejected:
            sys.exit()
        del(app)

    # init the logger
    from QtPyVCP.utilities import logger
    LOG = logger.initBaseLogger('QtPyVCP',
                                log_file=opts.log_file,
                                log_level=opts.log_level)

    return opts

class OptDict(dict):
    """Simple dot.notation access for opt dictionary values"""
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

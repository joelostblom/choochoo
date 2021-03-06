
from argparse import ArgumentParser
from genericpath import exists
from logging import getLogger
from os import makedirs
from os.path import dirname, expanduser, realpath, normpath
from re import sub
from typing import Mapping

from ..lib.date import to_date, to_time

log = getLogger(__name__)

# this can be modified during development.  it will be reset from setup.py on release.
CH2_VERSION = '0.27.5'
# new database on minor releases.  not sure this will always be a good idea.  we will see.
DB_VERSION = '-'.join(CH2_VERSION.split('.')[:2])

PROGNAME = 'ch2'
COMMAND = 'command'
TOPIC = 'topic'

ACTIVITIES = 'activities'
CONFIG = 'config'
CONSTANTS = 'constants'
DIARY = 'diary'
DUMP = 'dump'
FIT = 'fit'
FIX_FIT = 'fix-fit'
GARMIN = 'garmin'
H, HELP = 'h', 'help'
NO_OP = 'no-op'
PACKAGE_FIT_PROFILE = 'package-fit-profile'
STATISTICS = 'statistics'
TEST_SCHEDULE = 'test-schedule'

ACTIVITY = 'activity'
ACTIVITY_GROUP = 'activity-group'
ACTIVITY_GROUPS = 'activity-groups'
ACTIVITY_JOURNALS = 'activity-journals'
ACTIVITY_JOURNAL_ID = 'activity-journal-id'
ADD = 'add'
ADD_HEADER = 'add-header'
AFTER = 'after'
AFTER_BYTES = 'after-bytes'
AFTER_RECORDS = 'after-records'
ALL = 'all'
ALL_MESSAGES = 'all-messages'
ALL_FIELDS = 'all-fields'
ARG = 'arg'
BORDER = 'border'
CHANGE = 'change'
CHECK = 'check'
COMPACT = 'compact'
COMPONENT = 'component'
CONSTRAINT = 'constraint'
CONSTANT = 'constant'
CONTEXT = 'context'
CSV = 'csv'
D = 'd'
DATA = 'data'
DATABASE = 'database'
DATE = 'date'
DEFAULT = 'default'
DELETE = 'delete'
DESCRIBE = 'describe'
DESCRIPTION = 'description'
DEV = 'dev'
DIR = 'dir'
DISCARD = 'discard'
DROP = 'drop'
EMPTY = 'empty'
F = 'f'
FAST = 'fast'
FIELD = 'field'
FIELDS = 'fields'
FINISH = 'finish'
FIX_CHECKSUM = 'fix-checksum'
FIX_HEADER = 'fix-header'
FORMAT = 'format'
FORCE = 'force'
FTHR = 'fthr'
GREP = 'grep'
GROUP = 'group'
HEADER_SIZE = 'header-size'
HEIGHT = 'height'
INTERNAL = 'internal'
ITEM = 'item'
JUPYTER = 'jupyter'
K = 'k'
KARG = 'karg'
KIT = 'kit'
LABEL = 'label'
LATITUDE = 'latitude'
LIKE = 'like'
LIMIT_BYTES = 'limit-bytes'
LIMIT_RECORDS = 'limit-records'
LOG = 'log'
LOGS = 'logs'
LONGITUDE = 'longitude'
LIST = 'list'
M, MESSAGE = 'm', 'message'
MATCH = 'match'
MAX_BACK_CNT = 'max-back-cnt'
MAX_COLUMNS = 'max-columns'
MAX_COLWIDTH = 'max-colwidth'
MAX_DROP_CNT = 'max-drop-cnt'
MAX_DELTA_T = 'max-delta-t'
MAX_FWD_LEN = 'max-fwd-len'
MAX_ROWS = 'max-rows'
MAX_RECORD_LEN = 'max-record-len'
MIN_SYNC_CNT = 'min-sync-cnt'
MODEL = 'model'
MONITOR = 'monitor'
MONITOR_JOURNALS = 'monitor-journals'
MONTH = 'month'
MONTHS = 'months'
NAME = 'name'
NAME_BAD = 'name-bad'
NAME_GOOD = 'name-good'
NAMES = 'names'
NEW = 'new'
NOT = 'not'
NOTEBOOKS = 'notebooks'
O, OUTPUT = 'o', 'output'
OWNER = 'owner'
PASS = 'pass'
PATH = 'path'
P, PATTERN = 'p', 'pattern'
PLAN = 'plan'
PRINT = 'print'
PROFILE_VERSION = 'profile-version'
PROTOCOL_VERSION = 'protocol-version'
PWD = 'pwd'
RAW = 'raw'
REBUILD = 'rebuild'
RECORDS = 'records'
REMOVE = 'remove'
RETIRE = 'retire'
ROOT = 'root'
RUN = 'run'
SEGMENT_JOURNALS = 'segment-journals'
SEGMENTS = 'segments'
SERVICE = 'service'
SET = 'set'
SCHEDULE = 'schedule'
SHOW = 'show'
SINGLE = 'single'
SLICES = 'slices'
SOURCE_ID = 'source-id'
START = 'start'
STATISTIC_NAMES = 'statistic-names'
STATISTIC_JOURNALS = 'statistic-journals'
STATISTIC_QUARTILES = 'statistic-quartiles'
STATUS = 'status'
STOP = 'stop'
SUB_COMMAND = 'sub-command'
TABLE = 'table'
TABLES = 'tables'
TOKENS = 'tokens'
TUI = 'tui'
UNDO = 'undo'
UNLOCK = 'unlock'
USER = 'user'
VALIDATE = 'validate'
V, VERBOSITY = 'v', 'verbosity'
VALUE = 'value'
VERSION = 'version'
W, WARN = 'w', 'warn'
WAYPOINTS = 'waypoints'
WIDTH = 'width'
WORKER = 'worker'
YEAR = 'year'
Y = 'y'


def mm(name): return '--' + name
def m(name): return '-' + name
def no(name): return 'no-%s' % name


MEMORY = ':memory:'


class NamespaceWithVariables(Mapping):

    def __init__(self, ns):
        self._dict = vars(ns)

    def __getitem__(self, name):
        try:
            value = self._dict[name]
        except KeyError:
            value = self._dict[sub('-', '_', name)]
        return value

    def path(self, name, index=None):
        # special case sqlite3 in-memory database
        if self[name] == MEMORY: return self[name]
        path = self[name]
        if index is not None: path = path[index]
        path = expanduser(path)
        return realpath(normpath(path))

    def file(self, name, index=None):
        file = self.path(name, index=index)
        # special case sqlite3 in-memory database
        if file == MEMORY: return file
        path = dirname(file)
        if not exists(path):
            makedirs(path)
        return file

    def dir(self, name, index=None):
        path = self.path(name, index=index)
        if not exists(path):
            makedirs(path)
        return path

    def __iter__(self):
        return iter(self._dict)

    def __len__(self):
        return len(self.__dict__)


def make_parser():

    parser = ArgumentParser(prog=PROGNAME)

    parser.add_argument(m(V), mm(VERBOSITY), action='store', default=4, type=int, metavar='VERBOSITY',
                        help='output level for stderr (0: silent; 5:noisy)')
    parser.add_argument(mm(TUI), action='store_true',
                        help='text user interface (no log to stdout)')
    parser.add_argument(m(F), mm(DATABASE), action='store', default=f'~/.ch2/database-{DB_VERSION}.sql', metavar='FILE',
                        help='the file containing the database')
    parser.add_argument(mm(LOGS), action='store', default='~/.ch2/logs', metavar='DIR',
                        help='the directory for logs')
    parser.add_argument(mm(NOTEBOOKS), action='store', default='~/.ch2/notebooks', metavar='DIR',
                        help='the directory for notebooks (when jupyter starts)')
    parser.add_argument(mm(LOG), action='store', metavar='FILE',
                        help='the filename for the log (command name by default)')
    parser.add_argument(mm(DEV), action='store_true', help='show stack trace on error')
    parser.add_argument(m(V.upper()), mm(VERSION), action='version', version=CH2_VERSION,
                        help='display version and exit')

    subparsers = parser.add_subparsers(title='commands', dest=COMMAND)

    activities = subparsers.add_parser(ACTIVITIES, help='read activity data')
    activities.add_argument(mm(FORCE), action='store_true', help='re-read file and delete existing data')
    activities.add_argument(mm(FAST), action='store_true', help='do not calculate statistics')
    activities.add_argument(PATH, action='store', metavar='PATH', nargs='+',
                            help='path to fit file(s)')
    activities.add_argument(m(D.upper()), mm(CONSTANT), action='append', metavar='NAME=VALUE', dest=CONSTANT,
                            help='constant to be stored with the activities (can be repeated)')
    activities.add_argument(m(K.upper()), mm(KARG), action='append', metavar='NAME=VALUE', dest=KARG,
                            help='keyword argument to be passed to the pipelines (can be repeated)')
    activities.add_argument(mm(WORKER), action='store', metavar='ID', type=int,
                            help='internal use only (identifies sub-process workers)')

    config = subparsers.add_parser(CONFIG,
                                   help='configure the default database ' +
                                        '(see docs for full configuration instructions)')
    config_cmds = config.add_subparsers(title='sub-commands', dest=SUB_COMMAND, required=True)
    config_default = config_cmds.add_parser(DEFAULT, help="create default config")
    config_default.add_argument(mm(no(DIARY)), action='store_true', help='skip diary creation (for migration)')
    config_check = config_cmds.add_parser(CHECK, help="check config")
    config_check.add_argument(mm(no(DATA)), action='store_true', help='check database has no data loaded')
    config_check.add_argument(mm(no(CONFIG)), action='store_true', help='check database has no configuration')
    config_check.add_argument(mm(no(ACTIVITY_GROUPS)), action='store_true',
                              help='check database has no activity groups defined')

    constant = subparsers.add_parser(CONSTANTS, help='set and examine constants')
    constant_cmds = constant.add_subparsers(title='sub-commands', dest=SUB_COMMAND, required=True)
    constant_show = constant_cmds.add_parser(SHOW, help='show a value (or all values)')
    constant_show.add_argument(NAME, action='store', nargs='?', metavar='NAME', help='name (omit for all)')
    constant_show.add_argument(DATE, action='store', nargs='?', metavar='DATE',
                               help='date of value to show (omit for all)')
    constant_add = constant_cmds.add_parser(ADD, help='add a new constant')
    constant_add.add_argument(NAME, action='store', metavar='NAME', help='name')
    constant_add.add_argument(CONSTRAINT, action='store', nargs='?', metavar='CONSTRAINT',
                              help='constraint (eg activity group)')
    constant_add.add_argument(mm(SINGLE), action='store_true', help='allow only a single (constant) value')
    constant_add.add_argument(mm(DESCRIPTION), help='optional description')
    constant_add.add_argument(mm(VALIDATE), help='optional validation class')
    constant_set = constant_cmds.add_parser(SET, help='set or modify a value')
    constant_set.add_argument(NAME, action='store', metavar='NAME', help='name')
    constant_set.add_argument(VALUE, action='store', metavar='VALUE', help='value')
    constant_set.add_argument(DATE, action='store', nargs='?', metavar='DATE',
                              help='date when measured (omit for all time)')
    constant_set.add_argument(mm(FORCE), action='store_true', help='allow over-writing existing values')
    constant_delete = constant_cmds.add_parser(DELETE, help='delete a value (or all values)')
    constant_delete.add_argument(NAME, action='store', metavar='NAME', help='name')
    constant_delete.add_argument(DATE, action='store', nargs='?', metavar='DATE',
                                 help='date of value to delete (omit for all)')
    constant_delete.add_argument(mm(FORCE), action='store_true', help='allow deletion of all values')
    constant_remove = constant_cmds.add_parser(REMOVE, help='remove a constant (after deleting all values)')
    constant_remove.add_argument(NAME, action='store', metavar='NAME', help='name')
    constant_remove.add_argument(mm(FORCE), action='store_true', help='allow remove of multiple constants')

    diary = subparsers.add_parser(DIARY, help='daily diary and summary')
    diary.add_argument(DATE, action='store', metavar='DATE', nargs='?',
                       help='an optional date to display (default is today)')
    diary.add_argument(mm(FAST), action='store_true',
                       help='skip update of statistics on exit')
    diary_summary = diary.add_mutually_exclusive_group()
    diary_summary.add_argument(m(M), mm(MONTH), action='store_const', dest=SCHEDULE, const='m',
                               help='show monthly summary')
    diary_summary.add_argument(m(Y), mm(YEAR), action='store_const', dest=SCHEDULE, const='y',
                               help='show yearly summary')
    diary_summary.add_argument(mm(SCHEDULE), metavar='SCHEDULE',
                               help='show summary for given schedule')

    dump = subparsers.add_parser(DUMP, help='display database contents')  # todo - this one needs tests!
    dump_format = dump.add_mutually_exclusive_group()
    dump_format.add_argument(mm(PRINT), action='store_const', dest=FORMAT, const=PRINT, help='default format')
    dump_format.add_argument(mm(CSV), action='store_const', dest=FORMAT, const=CSV, help='CVS format')
    dump_format.add_argument(mm(DESCRIBE), action='store_const', dest=FORMAT, const=DESCRIBE, help='summary format')
    dump.add_argument(mm(MAX_COLUMNS), action='store', metavar='N', type=int, help='pandas max_columns attribute')
    dump.add_argument(mm(MAX_COLWIDTH), action='store', metavar='N', type=int, help='pandas max_colwidth attribute')
    dump.add_argument(mm(MAX_ROWS), action='store', metavar='N', type=int, help='pandas max_rows attribute')
    dump.add_argument(mm(WIDTH), action='store', metavar='N', type=int, help='pandas width attribute')
    dump_sub = dump.add_subparsers(dest=SUB_COMMAND)
    dump_statistics = dump_sub.add_parser(STATISTICS)
    dump_statistics.add_argument(NAMES, action='store', nargs='*', metavar='NAME', help='statistic names')
    dump_statistics.add_argument(mm(START), action='store', metavar='TIME', help='start time')
    dump_statistics.add_argument(mm(FINISH), action='store', metavar='TIME', help='finish time')
    dump_statistics.add_argument(mm(OWNER), action='store', metavar='OWNER',
                                 help='typically the class that created the data')
    dump_statistics.add_argument(mm(CONSTRAINT), action='store', metavar='CONSTRAINT',
                                 help='a value that makes the name unique (eg activity group)')
    dump_statistics.add_argument(mm(SCHEDULE), action='store', metavar='SCHEDULE',
                                 help='the schedule on which some statistics are calculated')
    dump_statistics.add_argument(mm(SOURCE_ID), action='append', metavar='ID', type=int,
                                 help='the source ID for the statistic (can be repeated)')
    dump_statistic_quartiles = dump_sub.add_parser(STATISTIC_QUARTILES)
    dump_statistic_quartiles.add_argument(NAMES, action='store', nargs='*', metavar='NAME', help='statistic names')
    dump_statistic_quartiles.add_argument(mm(START), action='store', metavar='TIME', help='start time')
    dump_statistic_quartiles.add_argument(mm(FINISH), action='store', metavar='TIME', help='finish time')
    dump_statistic_quartiles.add_argument(mm(OWNER), action='store', metavar='OWNER',
                                          help='typically the class that created the data')
    dump_statistic_quartiles.add_argument(mm(CONSTRAINT), action='store', metavar='CONSTRAINT',
                                          help='a value that makes the name unique (eg activity group)')
    dump_statistic_quartiles.add_argument(mm(SCHEDULE), action='store', metavar='SCHEDULE',
                                          help='the schedule on which some statistics are calculated')
    dump_statistic_quartiles.add_argument(mm(SOURCE_ID), action='append', metavar='ID', type=int,
                                          help='the source ID for the statistic (can be repeated)')
    dump_table = dump_sub.add_parser(TABLE)
    dump_table.add_argument(NAME, action='store', metavar='NAME', help='table name')
    dump.set_defaults(format=PRINT)

    fit = subparsers.add_parser(FIT, help='display contents of fit file')
    fit_cmds = fit.add_subparsers(title='sub-commands', dest=SUB_COMMAND, required=True)
    fit_grep = fit_cmds.add_parser(GREP, help='show matching entries')
    fit_records = fit_cmds.add_parser(RECORDS, help='show high-level structure (ordered by time)')
    fit_tables = fit_cmds.add_parser(TABLES, help='show high-level structure (grouped in tables)')
    fit_csv = fit_cmds.add_parser(CSV, help='show high-level structure (in CSV format)')
    fit_tokens = fit_cmds.add_parser(TOKENS, help='show low-level tokens')
    fit_fields = fit_cmds.add_parser(FIELDS, help='show low-level fields (within tokens)')

    def add_fit_general(cmd):
        cmd.add_argument(mm(AFTER_RECORDS), action='store', type=int, metavar='N', default=None,
                         help='skip initial records')
        cmd.add_argument(mm(LIMIT_RECORDS), action='store', type=int, metavar='N', default=-1,
                         help='limit number of records displayed')
        cmd.add_argument(mm(AFTER_BYTES), action='store', type=int, metavar='N', default=None,
                         help='skip initial bytes')
        cmd.add_argument(mm(LIMIT_BYTES), action='store', type=int, metavar='N', default=-1,
                         help='limit number of bytes displayed')
        cmd.add_argument(m(W), mm(WARN), action='store_true',
                         help='log additional warnings')
        cmd.add_argument(mm(no(VALIDATE)), action='store_true',
                         help='do not validate checksum, length')
        cmd.add_argument(mm(MAX_DELTA_T), action='store', type=float, metavar='S',
                         help='validate seconds between timestamps (and non-decreasing)')
        cmd.add_argument(mm(NAME), action='store_true',
                         help='print file name')
        cmd.add_argument(PATH, action='store', metavar='PATH', nargs='+',
                         help='path to fit file')

    def add_fit_grep(cmd):
        cmd.add_argument(mm(NOT), action='store_true',
                         help='print file names that don\'t match (with --name)')
        cmd.add_argument(mm(MATCH), action='store', type=int, default=-1,
                         help='max number of matches (default -1 for all)')
        cmd.add_argument(mm(COMPACT), action='store_true',
                         help='no space between records')
        cmd.add_argument(mm(CONTEXT), action='store_true',
                         help='display entire record')
        cmd.add_argument(m(P), mm(PATTERN), action='store', nargs='+', metavar='MSG:FLD[=VAL]', required=True,
                         help='pattern to match (separate from PATH with --)')

    def add_fit_high_level(cmd):
        cmd.add_argument(m(M), mm(MESSAGE), action='store', nargs='+', metavar='MSG',
                         help='display named messages')
        cmd.add_argument(m(F), mm(FIELD), action='store', nargs='+', metavar='FLD',
                         help='display named fields')
        cmd.add_argument(mm(INTERNAL), action='store_true',
                         help='display internal messages')

    def add_fit_very_high_level(cmd):
        cmd.add_argument(mm(ALL_MESSAGES), action='store_true',
                         help='display undocumented messages')
        cmd.add_argument(mm(ALL_FIELDS), action='store_true',
                         help='display undocumented fields')

    for cmd in fit_grep, fit_records, fit_tables, fit_csv, fit_tokens, fit_fields:
        add_fit_general(cmd)

    for cmd in fit_records, fit_tables, fit_csv:
        add_fit_high_level(cmd)

    for cmd in fit_records, fit_tables:
        add_fit_very_high_level(cmd)

    add_fit_grep(fit_grep)

    for cmd in fit_grep, fit_records, fit_tables:
        cmd.add_argument(mm(WIDTH), action='store', type=int,
                         help='display width')

    fix_fit = subparsers.add_parser(FIX_FIT, help='fix a corrupted fit file')
    fix_fit.add_argument(PATH, action='store', metavar='PATH', nargs='+',
                         help='path to fit file')
    fix_fit.add_argument(m(W), mm(WARN), action='store_true',
                         help='additional warning messages')
    fix_fit_output = fix_fit.add_argument_group(title='output (default hex to stdout)').add_mutually_exclusive_group()
    fix_fit_output.add_argument(m(O), mm(OUTPUT), action='store',
                                help='output file for fixed data (otherwise, stdout)')
    fix_fit_output.add_argument(mm(DISCARD), action='store_true',
                                help='discard output (otherwise, stdout)')
    fix_fit_output.add_argument(mm(RAW), action='store_true',
                                help='raw binary to stdout (otherwise, hex encoded)')
    fix_fit_output.add_argument(mm(NAME_BAD), action='store_false', dest=NAME, default=None,
                                help='print file name if bad')
    fix_fit_output.add_argument(mm(NAME_GOOD), action='store_true', dest=NAME, default=None,
                                help='print file name if good')
    fix_fit_process = fix_fit.add_argument_group(title='processing (default disabled)')
    fix_fit_process.add_argument(mm(ADD_HEADER), action='store_true',
                                 help='preprend a new header')
    fix_fit_stage = fix_fit_process.add_mutually_exclusive_group()
    fix_fit_stage.add_argument(mm(DROP), action='store_true',
                               help='search for data that can be dropped to give a successful parse')
    fix_fit_stage.add_argument(mm(SLICES), action='store', metavar='A:B,C:D,...',
                               help='data slices to pick')
    fix_fit_stage.add_argument(mm(START), action='store', type=to_time, metavar='TIME',
                               help='change start time')
    fix_fit_process.add_argument(mm(FIX_HEADER), action='store_true',
                                 help='modify the header')
    fix_fit_process.add_argument(mm(FIX_CHECKSUM), action='store_true',
                                 help='modify the checksum')
    fix_fit_process.add_argument(mm(no(FORCE)), action='store_false', dest=FORCE,
                                 help='don\'t parse record contents')
    fix_fit_process.add_argument(mm(no(VALIDATE)), action='store_false', dest=VALIDATE,
                                 help='don\'t validate the final data')
    fix_fit_params = fix_fit.add_argument_group(title='parameters')
    fix_fit_params.add_argument(mm(HEADER_SIZE), action='store', type=int, metavar='N',
                                help='header size (validation and/or new header)')
    fix_fit_params.add_argument(mm(PROTOCOL_VERSION), action='store', type=int, metavar='N',
                                help='protocol version (validation and/or new header)')
    fix_fit_params.add_argument(mm(PROFILE_VERSION), action='store', type=int, metavar='N',
                                help='profile version (validation and/or new header)')
    fix_fit_params.add_argument(mm(MIN_SYNC_CNT), action='store', type=int, metavar='N', default=3,
                                help='minimum number of records to read for synchronization')
    fix_fit_params.add_argument(mm(MAX_RECORD_LEN), action='store', type=int, metavar='N', default=None,
                                help='maximum record length')
    fix_fit_params.add_argument(mm(MAX_DROP_CNT), action='store', type=int, metavar='N', default=1,
                                help='maximum number of gaps to drop')
    fix_fit_params.add_argument(mm(MAX_BACK_CNT), action='store', type=int, metavar='N', default=3,
                                help='maximum number of readable records to discard in a single gap')
    fix_fit_params.add_argument(mm(MAX_FWD_LEN), action='store', type=int, metavar='N', default=200,
                                help='maximum number of bytes to drop in a single gap')
    fix_fit_params.add_argument(mm(MAX_DELTA_T), action='store', type=float, metavar='S',
                                help='max number of seconds between timestamps')

    garmin = subparsers.add_parser(GARMIN, help='download monitor data from garmin connect')
    garmin.add_argument(DIR, action='store', metavar='DIR',
                        help='the directory where FIT files are stored')
    garmin.add_argument(mm(USER), action='store', metavar='USER', required=True,
                        help='garmin connect username')
    garmin.add_argument(mm(PASS), action='store', metavar='PASSWORD', required=True,
                        help='garmin connect password')
    garmin.add_argument(mm(DATE), action='store', metavar='DATE', type=to_date,
                        help='date to download')
    garmin.add_argument(mm(FORCE), action='store_true', help='allow longer date range')

    help = subparsers.add_parser(HELP, help='display help')
    help.add_argument(TOPIC, action='store', nargs='?', metavar=TOPIC,
                      help='the subject for help')

    jupyter = subparsers.add_parser(JUPYTER, help='access jupyter')
    jupyter_cmds = jupyter.add_subparsers(title='sub-commands', dest=SUB_COMMAND, required=True)
    jupyter_cmds.add_parser(LIST, help='list available templates')
    jupyter_show = jupyter_cmds.add_parser(SHOW, help='display a template (starting server if needed)')
    jupyter_show.add_argument(NAME, action='store', help='the template name')
    jupyter_show.add_argument(ARG, action='store', nargs='*', help='template arguments')
    jupyter_cmds.add_parser(START, help='start a background service')
    jupyter_cmds.add_parser(STOP, help='stop the background service')
    jupyter_cmds.add_parser(STATUS, help='display status of background service')
    jupyter_cmds.add_parser(SERVICE, help='internal use only - use start/stop')

    kit = subparsers.add_parser(KIT, help='manage kit')
    kit_cmds = kit.add_subparsers(title='sub-commands', dest=SUB_COMMAND, required=True)
    kit_start = kit_cmds.add_parser(START, help='define a new item (new bike, new shoe)')
    kit_start.add_argument(GROUP, action='store', help='item group (bike, shoe, etc)')
    kit_start.add_argument(ITEM, action='store', help='item name (cotic, adidas, etc)')
    kit_start.add_argument(DATE, action='store', nargs='?', help='when created (default now)')
    kit_start.add_argument(mm(FORCE), action='store_true', help='confirm creation of a new group')
    kit_finish = kit_cmds.add_parser(FINISH, help='retire an item')
    kit_finish.add_argument(ITEM, action='store', help='item name')
    kit_finish.add_argument(DATE, action='store', nargs='?', help='when to retire (default now)')
    kit_finish.add_argument(mm(FORCE), action='store_true', help='confirm change of existing date')
    kit_delete = kit_cmds.add_parser(DELETE, help='remove all entries for an item or group')
    kit_delete.add_argument(NAME, action='store', help='item or group to delete')
    kit_delete.add_argument(mm(FORCE), action='store_true', help='confirm group deletion')
    kit_change = kit_cmds.add_parser(CHANGE, help='replace (or add) a part (wheel, innersole, etc)')
    kit_change.add_argument(ITEM, action='store', help='item name (cotic, adidas, etc)')
    kit_change.add_argument(COMPONENT, action='store', help='component type (chain, laces, etc)')
    kit_change.add_argument(MODEL, action='store', help='model description')
    kit_change.add_argument(DATE, action='store', nargs='?', help='when changed (default now)')
    kit_change.add_argument(mm(FORCE), action='store_true', help='confirm creation of a new component')
    kit_change.add_argument(mm(START), action='store_true', help='set default date to start of item')
    kit_undo = kit_cmds.add_parser(UNDO, help='remove a change')
    kit_undo.add_argument(ITEM, action='store', help='item name')
    kit_undo.add_argument(COMPONENT, action='store', help='component type')
    kit_undo.add_argument(MODEL, action='store', help='model description')
    kit_undo.add_argument(DATE, action='store', nargs='?', help='active date (to disambiguate models; default now)')
    kit_undo.add_argument(mm(ALL), action='store_true', help='remove all models (rather than single date)')
    kit_show = kit_cmds.add_parser(SHOW, help='display kit data')
    kit_show.add_argument(NAME, action='store', nargs='?', help='group or item to display (default all)')
    kit_show.add_argument(DATE, action='store', nargs='?', help='when to display (default now)')
    kit_show.add_argument(mm(CSV), action='store_true', help='CSV format')
    kit_statistics = kit_cmds.add_parser(STATISTICS, help='display statistics')
    kit_statistics.add_argument(NAME, action='store', nargs='?', help='group, item, component or model')
    kit_statistics.add_argument(mm(CSV), action='store_true', help='CSV format')
    kit_rebuild = kit_cmds.add_parser(REBUILD, help='rebuild database entries')

    monitor = subparsers.add_parser(MONITOR, help='read monitor data')
    monitor.add_argument(mm(FORCE), action='store_true', help='re-read file and delete existing data')
    monitor.add_argument(mm(FAST), action='store_true', help='do not calculate statistics')
    monitor.add_argument(PATH, action='store', metavar='PATH', nargs='+',
                         help='path to fit file(s)')
    monitor.add_argument(m(K.upper()), mm(KARG), action='append', metavar='NAME=VALUE', dest=KARG,
                         help='keyword argument to be passed to the pipelines (can be repeated)')
    monitor.add_argument(mm(WORKER), action='store', metavar='ID', type=int,
                         help='internal use only (identifies sub-process workers)')

    noop = subparsers.add_parser(NO_OP,
                                 help='used within jupyter (no-op from cmd line)')

    package_fit_profile = subparsers.add_parser(PACKAGE_FIT_PROFILE,
                                                help='parse and save the global fit profile (dev only)')
    package_fit_profile.add_argument(PATH, action='store', metavar='PROFILE',
                                     help='the path to the profile (Profile.xlsx)')
    package_fit_profile.add_argument(m(W), mm(WARN), action='store_true',
                                     help='additional warning messages')

    statistics = subparsers.add_parser(STATISTICS, help='(re-)generate statistics')
    statistics.add_argument(mm(FORCE), action='store_true',
                            help='delete existing statistics')
    statistics.add_argument(mm(LIKE), action='store', metavar='PATTERN',
                            help='run only matching pipeline classes')
    statistics.add_argument(START, action='store', metavar='START', nargs='?',
                            help='optional start date')
    statistics.add_argument(FINISH, action='store', metavar='FINISH', nargs='?',
                            help='optional finish date (if start also given)')
    statistics.add_argument(m(K.upper()), mm(KARG), action='append', metavar='NAME=VALUE', dest=KARG,
                            help='keyword argument to be passed to the pipelines (can be repeated)')
    statistics.add_argument(mm(WORKER), action='store', metavar='ID', type=int,
                            help='internal use only (identifies sub-process workers)')

    test_schedule = subparsers.add_parser(TEST_SCHEDULE, help='print schedule locations in a calendar')
    test_schedule.add_argument(SCHEDULE, action='store', metavar='SCHEDULE',
                               help='the schedule to test')
    test_schedule.add_argument(mm(START), action='store', metavar='DATE',
                               help='the date to start displaying data')
    test_schedule.add_argument(mm(MONTHS), action='store', metavar='N', type=int,
                               help='the number of months to display')

    unlock = subparsers.add_parser(UNLOCK, help='remove database locking')

    return parser


def bootstrap_file(file, *args, configurator=None, post_config=None):

    from ..lib.log import make_log
    from ..config.database import config
    from ..squeal.database import Database

    args = [mm(DATABASE), file.name] + list(args)
    if configurator:
        db = config(*args)
        configurator(db)
    args += post_config if post_config else []
    args = NamespaceWithVariables(make_parser().parse_args(args))
    make_log(args)
    db = Database(args)

    return args, db


def parse_pairs(pairs):
    # simple name, value pairs.  owner and constraint supplied by command.
    d = {}
    if pairs is not None:
        for pair in pairs:
            name, value = pair.split('=', 1)
            for type in (int, float, to_time):
                try:
                    value = type(value)
                    break
                except ValueError:
                    pass
            d[name] = value
    return d

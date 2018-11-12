
from ..squeal.database import connect
from ..squeal.tables.activity import ActivityGroup
from ..squeal.tables.constant import Constant, intern
from ..squeal.tables.pipeline import Pipeline, PipelineType
from ..squeal.tables.statistic import StatisticName, StatisticJournalType
from ..squeal.tables.topic import Topic, TopicField
from ..uweird.fields.topic import Integer


def config(*args):
    '''
    Start here to configure the system.  Create an instance on the command line:

        log, db = config('-v', '4')
        print(c...)  todo
        ...
    '''
    ns, log, db = connect(args)
    return log, db


class Counter:

    def __init__(self, start=10, delta=10):
        self.__start = start
        self.__delta = delta
        self.__previous = None

    def __call__(self, reset=None, delta=None):
        if delta is not None:
            if delta < 1:
                raise Exception('Negative increment')
            self.__delta = delta
        if reset is None:
            if self.__previous is None:
                self.__previous = self.__start
            else:
                self.__previous += self.__delta
        else:
            if reset <= self.__previous:
                raise Exception('Sort not increasing with reset')
            else:
                self.__previous = reset
        return self.__previous


def add(s, instance):
    '''
    Add an instance to the session (and so to the database), returning the instance.
    You likely don't need this - see the more specific helpers below.

    The instance can of any class that subclasses the Field class from SQLAlchemy.
    In practice, that means most classes in the ch2.squeal.tables mdoule.
    However, only some classes make sense in the context of a configuration, and
    more specific helpers probably already exist for those.
    '''
    s.add(instance)
    return instance


def add_statistics(s, cls, sort, **kargs):
    '''
    Add a class to the statistics pipeline.

    The pipeline classes are invoked when the diary is modified and when activities are added.
    They detect new data and calculate appropriate statistics.
    See the ch2.stoats module for examples.

    The sort argument fixes the order in which the classes are instantiated and called and can
    be an integer or a callable (that returns an integer) like Counter above.

    The kargs are passed to the constructor and so can be used to customize the processing.
    '''
    return add(s, Pipeline(cls=cls, type=PipelineType.STATISTIC, sort=sort, kargs=kargs))


def add_diary(s, cls, sort, **kargs):
    '''
    Add a class to the diary pipeline.

    The pipeline classes are invoked when the diary is displyed.
    They generate display classes for activity statistics (and similar)
    See the ch2.stoats module for examples.

    The sort argument fixes the order in which the classes are instantiated and called and can
    be an integer or a callable (that returns an integer) like Counter above.

    The kargs are passed to the constructor and so can be used to customize the processing.
    '''
    return add(s, Pipeline(cls=cls, type=PipelineType.DIARY, sort=sort, kargs=kargs))


def add_monitor(s, cls, sort, **kargs):
    '''
    Add a class to the monitor pipeline.

    The pipeline classes are invoked when activities are imported from FIT files.
    They read the files and create MonitorJournal entries and associated statistics.

    The sort argument fixes the order in which the classes are instantiated and called and can
    be an integer or a callable (that returns an integer) like Counter above.

    The kargs are passed to the constructor and so can be used to customize the processing.
    '''
    return add(s, Pipeline(cls=cls, type=PipelineType.MONITOR, sort=sort, kargs=kargs))


def add_activity_group(s, name, sort, description=None):
    '''
    Add an activity type to the configuration.

    These are used to group activities (and related statistics).
    So typical entries might be for cycling, running, etc.
    '''
    return add(s, ActivityGroup(name=name, sort=sort, description=description))


def add_activities(s, cls, sort, **kargs):
    '''
    Add a class to the activities pipeline.

    The pipeline classes are invoked when activities are imported from FIT files.
    They read the files and create ActivityJournal entries and associated statistics.

    The sort argument fixes the order in which the classes are instantiated and called and can
    be an integer or a callable (that returns an integer) like Counter above.

    The kargs are passed to the constructor and so can be used to customize the processing.
    '''
    return add(s, Pipeline(cls=cls, type=PipelineType.ACTIVITY, sort=sort, kargs=kargs))


def add_activity_constant(s, activity_group, name, description=None, units=None,
                          statistic_journal_type=StatisticJournalType.INTEGER):
    '''
    Add a constant associated with an activity.

    Configuring a constant allows the user to supply a value later, using the `ch2 constant` command.
    This can be useful for values that don't vary often, and so aren't worth adding to the diary.
    An example is FTHR, which you will only measure occasionally, but which is needed when calculating
    activity statistics (also, FTHR can vary by activity, which is why we add a constant per activity).
    '''
    if activity_group.id is None:
        s.flush()
    statistic_name = add(s, StatisticName(name=name, owner=intern(s, Constant),
                                          constraint=activity_group.id, constraint_hint='ActivityGroup',
                                          units=units, description=description))
    constant = add(s, Constant(statistic_journal_type=statistic_journal_type, statistic_name=statistic_name,
                               name='%s.%s' % (name, activity_group.name)))


def add_topic(s, name, sort, description=None, schedule=None):
    '''
    Add a root topic.

    Topics are displayed in the diary.
    They can be permanent, or associated with some schedule.
    They can also be associated with fields (and so with statistics).

    A root topic is usually used as a header to group related children.
    For example, 'DailyDiary' to group diary entries (notes, weight, sleep etc), or 'Plan' to group training plans.
    '''
    return add(s, Topic(name=name, sort=sort, description=description, schedule=schedule))


def add_child_topic(s, parent, name, sort, description=None, schedule=None):
    '''
    Add a child topic.

    Topics are displayed in the diary.
    They can be permanent, or associated with some schedule.
    They can also be associated with fields (and so with statistics).

    A child topic is used to add additional structrure to an existing topic.
    For example, the parent topic might be "injuries" and permanent, while children are defined for
    specific injuries with a schedule that gives start and end dates.
    '''
    return add(s, Topic(parent=parent, name=name, sort=sort, description=description, schedule=schedule))


def add_topic_field(s, topic, name, sort, description=None, units=None, summary=None,
                    display_cls=Integer, **display_kargs):
    '''
    Add a field and associated statistic to a topic entry.

    This is how the user can enter values into the diary.
    The field describes how the values are displayed in the diary.
    The statistic describes how the values are stored in the database.
    '''
    if topic.id is None:
        s.flush()
    statistic_name = add(s, StatisticName(name=name, owner=intern(s, topic),
                                          constraint=topic.id, constraint_hint='Topic',
                                          description=description, units=units, summary=summary))
    field = add(s, TopicField(topic=topic, sort=sort, type=display_cls.statistic_journal_type,
                              display_cls=display_cls, display_kargs=display_kargs,
                              statistic_name=statistic_name))

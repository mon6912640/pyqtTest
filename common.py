EVENT_SHOW_LOG = 'event_show_log'
EVENT_MAIN_INIT = 'event_main_init'
EVENT_FILE_COMPLETE = 'event_file_complete'

from monkey_event import *

app = None

LOG_TYPE_MAIN = 'type_main'
LOG_TYPE_CLEAN = 'type_clean'


# EventCenterAsync.setup(False)


def show_log(p_str: str, p_type=LOG_TYPE_MAIN):
    EventCenterSync.send_event(EVENT_SHOW_LOG, {'str': p_str, 'type': p_type})


def send_file_complete():
    EventCenterSync.send_event(EVENT_FILE_COMPLETE)

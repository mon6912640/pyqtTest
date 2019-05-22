EVENT_SHOW_LOG = 'event_show_log'
EVENT_MAIN_INIT = 'event_main_init'

from monkey_event import *

app = None

# EventCenterAsync.setup(False)


def show_log(p_str):
    EventCenterSync.send_event(EVENT_SHOW_LOG, p_str)

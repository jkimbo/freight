from __future__ import absolute_import

from .base import Notifier, NotifierEvent  # NOQA
from .dummy import DummyNotifier
from .manager import NotifierManager
from .sentry import SentryNotifier
from .slack import SlackNotifier
from .hipchat import HipChatNotifier
from .queue import NotificationQueue

queue = NotificationQueue()

manager = NotifierManager()
manager.add('dummy', DummyNotifier)
manager.add('sentry', SentryNotifier)
manager.add('slack', SlackNotifier)
manager.add('hipchat', HipChatNotifier)

get = manager.get

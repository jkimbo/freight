from __future__ import absolute_import

import json
import responses

from freight import notifiers
from freight.notifiers import NotifierEvent
from freight.models import TaskStatus
from freight.testutils import TestCase


class HipChatNotifierBase(TestCase):
    def setUp(self):
        self.notifier = notifiers.get('hipchat')
        self.user = self.create_user()
        self.repo = self.create_repo()
        self.app = self.create_app(repository=self.repo)
        self.task = self.create_task(
            app=self.app,
            user=self.user,
            status=TaskStatus.finished,
        )


class HipChatNotifierTest(HipChatNotifierBase):
    @responses.activate
    def test_send_finished_task(self):
        responses.add(responses.POST, 'http://example.com/')

        config = {'webhook_url': 'http://example.com/'}

        self.notifier.send(self.task, config, NotifierEvent.TASK_FINISHED)

        call = responses.calls[0]
        assert len(responses.calls) == 1
        assert call.request.url == 'http://example.com/'
        body = call.request.body
        payload = json.loads(body)
        # TODO(dcramer): we probably shouldnt hardcode this, but it'll do for now
        assert payload
        assert payload['color'] == 'green'

    @responses.activate
    def test_send_started_task(self):
        responses.add(responses.POST, 'http://example.com/')

        config = {'webhook_url': 'http://example.com/'}

        self.notifier.send(self.task, config, NotifierEvent.TASK_STARTED)

        call = responses.calls[0]
        assert len(responses.calls) == 1
        assert call.request.url == 'http://example.com/'
        body = call.request.body
        payload = json.loads(body)
        # TODO(dcramer): we probably shouldnt hardcode this, but it'll do for now
        assert payload
        assert payload['color'] == 'yellow'

    @responses.activate
    def test_notify_option(self):
        responses.add(responses.POST, 'http://example.com/')

        config = {'webhook_url': 'http://example.com/', 'notify': 'true'}

        self.notifier.send(self.task, config, NotifierEvent.TASK_FINISHED)

        call = responses.calls[0]
        assert len(responses.calls) == 1
        assert call.request.url == 'http://example.com/'
        body = call.request.body
        payload = json.loads(body)
        # TODO(dcramer): we probably shouldnt hardcode this, but it'll do for now
        assert payload
        assert payload['notify'] == 'true'

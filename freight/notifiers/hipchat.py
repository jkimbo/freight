from __future__ import absolute_import

__all__ = ['HipChatNotifier']

from freight import http
from freight.models import App, TaskStatus

from .base import Notifier, NotifierEvent


class HipChatNotifier(Notifier):
    def get_options(self):
        return {
            'webhook_url': {'required': True},
            'notify': {'required': False},
        }

    def send(self, task, config, event):
        webhook_url = config['webhook_url']
        notify = config.get('notify', False)

        app = App.query.get(task.app_id)

        params = {
            'number': task.number,
            'app_name': app.name,
            'env': task.environment,
            'ref': task.ref,
            'sha': task.sha[:7] if task.sha else task.ref,
            'status_label': task.status_label,
            'duration': task.duration,
            'link': http.absolute_uri('/tasks/{}/{}/{}/'.format(app.name, task.environment, task.number)),
        }

        if event == NotifierEvent.TASK_QUEUED:
            message = "[{app_name}/{env}] Queued deploy <{link}|#{number}> ({sha})".format(**params)
            color = 'yellow'
        elif event == NotifierEvent.TASK_STARTED:
            message = "[{app_name}/{env}] Starting deploy <{link}|#{number}> ({sha})".format(**params)
            color = 'yellow'
        elif task.status == TaskStatus.failed:
            message = "[{app_name}/{env}] Failed to deploy <{link}|#{number}> ({sha}) after {duration}s".format(**params)
            color = 'red'
        elif task.status == TaskStatus.cancelled:
            message = "[{app_name}/{env}] Deploy <{link}|#{number}> ({sha}) was cancelled after {duration}s".format(**params)
            color = 'red'
        elif task.status == TaskStatus.finished:
            message = "[{app_name}/{env}] Successfully deployed <{link}|#{number}> ({sha}) after {duration}s".format(**params)
            color = 'green'
        else:
            raise NotImplementedError(task.status)

        payload = {
            'message_format': 'text',
            'message': message,
            'color': color,
            'notify': notify,
        }

        http.post(webhook_url, json=payload)

# coding=utf-8
from __future__ import absolute_import

import octoprint.plugin
import os
import json
import requests

class StackStormPlugin(octoprint.plugin.SettingsPlugin,
                       octoprint.plugin.TemplatePlugin,
                       octoprint.plugin.EventHandlerPlugin):

    ## SettingsPlugin

    def get_settings_defaults(self):
        return dict(webhook_url="", api_key="")

    def get_settings_version(self):
        return 1

    ## TemplatePlugin

    def get_template_configs(self):
        return [dict(type="settings", name="StackStorm", custom_bindings=False)]

    ## EventPlugin

    def on_event(self, event, payload):
        webhook_url = self._settings.get(['webhook_url'])
        api_key = self._settings.get(['api_key'])

        if webhook_url == "":
            self._logger.exception("StackStorm Webhook URL not set!")
            return

        if api_key == "":
            self._logger.exception("StackStorm API Key not set!")
            return

        headers = {
            'St2-Api-Key': api_key,
        }
        payload = {
            'event': event,
            'payload': payload,
        }

        self._logger.debug("Attempting post of StackStorm message: {}".format(payload))

        try:
            res = requests.post(webhook_url, headers=headers, json=payload)
        except Exception, e:
            self._logger.exception("An error occurred connecting to StackStorm:\n {}".format(e.message))
            return

        if not res.ok:
            self._logger.exception("An error occurred posting to StackStorm:\n {}".format(res.text))
            return

        self._logger.debug("Posted event successfully to StackStorm!")

__plugin_name__ = "StackStorm"
__plugin_implementation__ = StackStormPlugin()

# coding=utf-8
from __future__ import absolute_import

import octoprint.plugin
import os
import json
import requests

class StackStormPlugin(octoprint.plugin.SettingsPlugin,
                       octoprint.plugin.TemplatePlugin,
                       octoprint.plugin.StartupPlugin,
                       octoprint.plugin.EventHandlerPlugin):

    ## SettingsPlugin

    def get_settings_defaults(self):
        return dict(
            webhook_url="",
            api_key=""
        )

    def on_settings_save(self, data):
        old_webhook_url = self._settings.get(['webhook_url'])
        old_api_key = self._settings.get(['api_key'])

        octoprint.plugin.SettingsPlugin.on_settings_save(self, data)
        new_webhook_url = self._settings.get(['webhook_url'])
        new_api_key = self._settings.get(['api_key'])

        if old_webhook_url != new_webhook_url:
            self._logger.info("StackStorm Webhook URL changed from {old_webhook_url} to {new_webhook_url}".format(**locals()))

        if old_api_key != new_api_key:
            self._logger.info("StackStorm API Key changed")

    def get_settings_version(self):
        return 1

    ## TemplatePlugin
    def get_template_configs(self):
        return [dict(type="settings", name="StackStorm", custom_bindings=False)]

    ## StartupPlugin
    def on_after_startup(self):
        webhook_url = self._settings.get(['webhook_url'])
        api_key = self._settings.get(['api_key'])

    ## EventPlugin

    def on_event(self, event, payload):
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

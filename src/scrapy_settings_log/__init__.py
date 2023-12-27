import logging
import inspect
import json
import re

import scrapy
from scrapy import signals
from scrapy.settings import BaseSettings

logger = logging.getLogger(__name__)


class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, BaseSettings):
            return CustomEncoder.clean_settings_dict(dict(obj))
        if isinstance(obj, set):
            return str(obj)
        return json.JSONEncoder.default(self, obj)

    @classmethod
    def clean_settings_dict(cls, settings_dict):
        parsed_settings = {}
        for key in settings_dict:
            if (
                isinstance(key, str) or
                isinstance(key, int) or
                isinstance(key, float) or
                isinstance(key, bool) or
                key is None
            ):
                parsed_settings[key] = CustomEncoder.clean_settings_value(settings_dict[key])
            elif inspect.isclass(key):
                parsed_settings[key.__name__] = CustomEncoder.clean_settings_value(settings_dict[key])
            elif isinstance(key, tuple):
                parsed_settings[str(key)] = CustomEncoder.clean_settings_value(settings_dict[key])
            else:
                # Warn that key is of unexpected type. ex: a class object.
                parsed_settings[str(key)] = CustomEncoder.clean_settings_value(settings_dict[key])
                logger.warn(f"Using __str__ for {key} as it cannot be encoded as JSON.")
        return parsed_settings

    @classmethod
    def clean_settings_value(cls, value):
        if isinstance(value, BaseSettings) or isinstance(value, dict):
            return CustomEncoder.clean_settings_dict(value)
        return value


class SpiderSettingsLogging:
    custom_encoder = CustomEncoder

    @classmethod
    def from_crawler(cls, crawler):
        ext = cls()
        crawler.signals.connect(ext.spider_closed, signal=signals.spider_closed)
        return ext

    def spider_closed(self, spider):
        settings = spider.settings
        if not settings.getbool("SETTINGS_LOGGING_ENABLED"):
            return

        regex = settings.get("SETTINGS_LOGGING_REGEX")
        if regex is not None:
            settings = {k: v for k, v in settings.items() if re.search(regex, k)}

        self.output_settings(settings, spider)

    def output_settings(self, settings: dict, spider: scrapy.Spider):
        # this can be overwritten in a subclass if you want to send this data elsewhere
        indent = spider.settings.get("SETTINGS_LOGGING_INDENT")
        clean_settings = self.custom_encoder.clean_settings_dict(settings)
        logger.info(json.dumps(clean_settings, indent=indent, cls=self.custom_encoder))

import inspect
import json
import logging
import re
from collections.abc import Iterable, Mapping

import scrapy
from scrapy import signals

logger = logging.getLogger(__name__)


def prepare_for_json_serialization(obj):
    """Prepare the obj recursively for JSON serialization.

    Args:
        obj: The obj.

    Returns:
        object suitable for JSON serialization.

    """
    if isinstance(obj, (str, int, float, bool)) or obj is None:
        return obj
    elif isinstance(obj, Mapping):
        return {
            str(prepare_for_json_serialization(k)): prepare_for_json_serialization(v)
            for k, v in obj.items()
        }
    elif isinstance(obj, Iterable):
        return [prepare_for_json_serialization(v) for v in obj]
    elif inspect.isclass(obj):
        return str(obj.__name__)
    else:
        logger.warn(f"Using __str__ for {obj} as it cannot be encoded as JSON.")
        return str(obj)


class SpiderSettingsLogging:
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
        # convert settings obj into something representable in JSON
        json_serializable_settings = prepare_for_json_serialization(settings)
        logger.info(json.dumps(json_serializable_settings, indent=indent))

import logging
import json
import re
from scrapy import signals
from scrapy.settings import BaseSettings

logger = logging.getLogger(__name__)


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
        indent = settings.get("SETTINGS_LOGGING_INDENT")
        if regex is not None:
            settings = {k: v for k, v in settings.items() if re.search(regex, k)}

        # nested settings will be BaseSettings objects that are not JSON seriable
        settings = {
            k: dict(v) if type(v) is BaseSettings else v for k, v in settings.items()
        }

        logger.debug(json.dumps(settings, indent=indent))

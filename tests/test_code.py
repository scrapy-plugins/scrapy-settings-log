from scrapy import Spider
from scrapy.crawler import Crawler
from src.scrapy_settings_log import SpiderSettingsLogging
import logging

LOGGER = logging.getLogger(__name__)


def MockSpider(settings):
    crawler = Crawler(Spider, settings=settings)
    return Spider.from_crawler(crawler, name="dummy")


def test_disabled(caplog):
    spider = MockSpider({})
    logger = SpiderSettingsLogging()
    logger.spider_closed(spider)

    with caplog.at_level(logging.INFO):
        logger.spider_closed(spider)

    assert not caplog.text


def test_log_all(caplog):
    settings = {
        "SETTINGS_LOGGING_ENABLED": True,
    }

    spider = MockSpider(settings)
    logger = SpiderSettingsLogging()
    with caplog.at_level(logging.INFO):
        logger.spider_closed(spider)

    # won't check specifics here as the default settings
    # can vary with scrapy versions - presence is enough
    assert caplog.text


def test_log_filtered(caplog):
    settings = {
        "SETTINGS_LOGGING_ENABLED": True,
        "DUMMY_INT": 4,
        "DUMMY_STR": "foo",
        "SETTINGS_LOGGING_REGEX": "DUMMY",
    }

    spider = MockSpider(settings)
    logger = SpiderSettingsLogging()
    with caplog.at_level(logging.INFO):
        logger.spider_closed(spider)

    assert '{"DUMMY_INT": 4, "DUMMY_STR": "foo"}' in caplog.text


def test_log_indented(caplog):
    settings = {
        "SETTINGS_LOGGING_ENABLED": True,
        "DUMMY_INT": 4,
        "DUMMY_STR": "foo",
        "SETTINGS_LOGGING_REGEX": "DUMMY",
        "SETTINGS_LOGGING_INDENT": 4,
    }

    spider = MockSpider(settings)
    logger = SpiderSettingsLogging()
    with caplog.at_level(logging.INFO):
        logger.spider_closed(spider)

    assert '{\n    "DUMMY_INT": 4,\n    "DUMMY_STR": "foo"\n}' in caplog.text


def test_log_set(caplog):
    settings = {
        "SETTINGS_LOGGING_ENABLED": True,
        "DUMMY_SET": {1, 2, 3},
        "SETTINGS_LOGGING_REGEX": "DUMMY",
    }

    spider = MockSpider(settings)
    logger = SpiderSettingsLogging()
    with caplog.at_level(logging.INFO):
        logger.spider_closed(spider)

    assert '{"DUMMY_SET": "{1, 2, 3}"}' in caplog.text

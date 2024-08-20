import logging

from scrapy import Spider
from scrapy.crawler import Crawler

from src.scrapy_settings_log import SpiderSettingsLogging

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

    assert '{"DUMMY_SET": [1, 2, 3]}' in caplog.text


def test_log_custom_class(caplog):

    class CustomClass:
        pass

    settings = {
        "SETTINGS_LOGGING_ENABLED": True,
        "SETTINGS_LOGGING_REGEX": "DUMMY",
        "DUMMY_CUSTOM_CLASS": {CustomClass: "/foo/bar"},
    }
    spider = MockSpider(settings)
    logger = SpiderSettingsLogging()
    with caplog.at_level(logging.INFO):
        logger.spider_closed(spider)

    assert '{"DUMMY_CUSTOM_CLASS": {"CustomClass": "/foo/bar"}}' in caplog.text


def test_log_all_should_not_return_apikey_value_by_default(caplog):
    settings = {
        "SETTINGS_LOGGING_ENABLED": True,
        "SHUB_APIKEY": "apikey_value1",
        "shub_apikey": "apikey_value2",
        "api_key": "apikey_value3",
    }

    spider = MockSpider(settings)
    logger = SpiderSettingsLogging()
    with caplog.at_level(logging.INFO):
        logger.spider_closed(spider)

    assert '"SHUB_APIKEY": "**********"' in caplog.text
    assert '"shub_apikey": "**********"' in caplog.text
    assert '"api_key": "**********"' in caplog.text
    assert "apikey_value" not in caplog.text


def test_log_all_should_return_apikey_value_if_MASKED_SENSITIVE_SETTINGS_ENABLED_is_false(
    caplog,
):
    settings = {
        "SETTINGS_LOGGING_ENABLED": True,
        "APIKEY": "apikey_value",
        "MASKED_SENSITIVE_SETTINGS_ENABLED": False,
    }

    spider = MockSpider(settings)
    logger = SpiderSettingsLogging()
    with caplog.at_level(logging.INFO):
        logger.spider_closed(spider)

    assert '"APIKEY": "apikey_value"' in caplog.text


def test_log_all_should_not_return_aws_secret_key_value_by_default(caplog):
    settings = {
        "SETTINGS_LOGGING_ENABLED": True,
        "AWS_SECRET_ACCESS_KEY": "secret_value1",
        "aws_secret_access_key": "secret_value2",
        "aws_access_key": "secret_value2",
        "AWS_SECRET_KEY": "secret_value2",
        "aws_secret_key": "secret_value2",
    }

    spider = MockSpider(settings)
    logger = SpiderSettingsLogging()
    with caplog.at_level(logging.INFO):
        logger.spider_closed(spider)

    assert '"AWS_SECRET_ACCESS_KEY": "**********"' in caplog.text
    assert '"aws_secret_access_key": "**********"' in caplog.text
    assert '"aws_access_key": "**********"' in caplog.text
    assert '"AWS_SECRET_KEY": "**********"' in caplog.text
    assert '"aws_secret_key": "**********"' in caplog.text
    assert "secret_value" not in caplog.text


def test_log_all_should_not_return_password_value_by_default(caplog):
    settings = {
        "SETTINGS_LOGGING_ENABLED": True,
        "test_password": "secret_value1",
        "PASSWORD_TEST": "secret_value2",
    }

    spider = MockSpider(settings)
    logger = SpiderSettingsLogging()
    with caplog.at_level(logging.INFO):
        logger.spider_closed(spider)

    assert '"test_password": "**********"' in caplog.text
    assert '"PASSWORD_TEST": "**********"' in caplog.text
    assert "secret_value" not in caplog.text


def test_log_all_should_return_only_the_custom_regex_data_masked_if_MASKED_SENSITIVE_SETTINGS_REGEX_LIST_configured(
    caplog,
):
    settings = {
        "SETTINGS_LOGGING_ENABLED": True,
        "MASKED_SENSITIVE_SETTINGS_REGEX_LIST": ["apppppppikey"],
        "APIKEY": "apikey_value1",
        "apppppppikey": "some_random_value",
    }

    spider = MockSpider(settings)
    logger = SpiderSettingsLogging()
    with caplog.at_level(logging.INFO):
        logger.spider_closed(spider)

    assert "apikey_value1" in caplog.text
    assert '"apppppppikey": "**********"' in caplog.text
    assert "some_random_value" not in caplog.text

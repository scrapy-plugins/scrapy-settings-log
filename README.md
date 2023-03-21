# Scrapy Settings Log
An extension that allows a user to display all or some of their scrapy spider settings at runtime. 
It will add a logline with some or all settings for your spider in JSON compatible format.


## Install

`pip install scrapy-settings-log`

## Quick-Start

Add the following to your settings:

```python
EXTENSIONS = {
    'scrapy_settings_log.SpiderSettingsLogging': 999,
}

SETTINGS_LOGGING_ENABLED = True
```

When you run your spider you will see a debug log like below when spider is closing:

`[scrapy_settings_log] INFO: {"SETTINGS_LOGGING_ENABLED": true, ...}`

## Additional Options

* `SETTINGS_LOGGING_REGEX` - Add a regular expression to only show some settings - for example `SETTINGS_LOGGING_REGEX = "SPIDERMON"` will show settings with SPIDERMON in their name.
* `SETTINGS_LOGGING_INDENT` - Add indentation to make log more human-readable.

import os
from datetime import datetime, timezone
from scrapy.crawler import CrawlerProcess
from yugioh_scraper.spiders.db_yugioh_card import DBYugiohCardSpider

UTC_DATETIME = datetime.now(timezone.utc)
UTC_FILE_FORMATTED = UTC_DATETIME.strftime("%Y-%m-%d")


def main():
    """Entry point for the application script"""
    print("Call your main code here")


def db_yugioghcard():
    # os.makedirs() method will raise
    # an OSError if the directory
    # to be created already exists
    # But It can be suppressed by
    # setting the value of a parameter
    # exist_ok as True

    # directory
    directory = "db_yugioghcard"

    # parent job directory path
    parent_directory = "jobs"

    # path
    path = os.path.join(parent_directory, directory)
    print(path)

    # create the directory
    try:
        os.makedirs(path, exist_ok=True)
        print("Directory '%s' created successfully" % directory)
    except OSError as error:
        print("Directory '%s' can not be created" % directory)

    # By setting exist_ok as True
    # error caused due already
    # existing directory can be suppressed
    # but other OSError may be raised
    # due to other error like
    # invalid path name

    """Entry point for the db_yugioghcard spider"""
    process = CrawlerProcess(
        settings={
            "FEEDS": {
                f"{path}/{UTC_FILE_FORMATTED}.json": {"format": "json"},
            },
        }
    )
    process.crawl(DBYugiohCardSpider)
    process.start()

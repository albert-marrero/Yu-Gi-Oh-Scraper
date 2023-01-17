# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem


class DbYugiohCardPipeline:
    def process_item(self, item, spider):
        return item


class DuplicatesPipeline:
    def __init__(self):
        self.product_name_seen = set()
        self.card_name_seen = set()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        data_type = adapter["data_type"]

        if data_type == "product":
            if adapter["product_name"] in self.product_name_seen:
                raise DropItem(f"Duplicate product name found: {item!r}")

            self.product_name_seen.add(adapter["product_name"])

        if data_type == "product_card":
            if adapter["card_name"] in self.card_name_seen:
                raise DropItem(f"Duplicate card name found: {item!r}")

            self.card_name_seen.add(adapter["card_name"])

        return item


class CardDetailsPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        if "card_details" in adapter:
            adapter["card_details"] = [
                i.strip() for i in adapter["card_details"] if i.strip()
            ]

        return item

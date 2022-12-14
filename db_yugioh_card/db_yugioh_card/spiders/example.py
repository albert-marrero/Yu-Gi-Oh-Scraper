import scrapy


class DBYugiohCardSpider(scrapy.Spider):
    name = "db_yugioghcard"
    allowed_domains = ["yugioh-card.com"]
    start_urls = ["https://www.db.yugioh-card.com/yugiohdb/card_list.action"]

    def parse(self, response):
        product_lists = response.xpath(
            '//div[contains(@id, "card_list")]//div[contains(@class, "pac_set")]'
        )

        for product_list in product_lists:
            product_type = product_list.xpath(
                'div[contains(@class, "list_title")]//span//text()'
            ).extract_first()
            products = product_list.xpath(
                'div[contains(@class, "list_body")]//div[contains(@class, "toggle")]//div[contains(@class, "pack")]'
            )

            for product in products:
                product_name = product.xpath("p//strong//text()").extract_first()
                product_link = product.xpath("input//@value").extract_first()

                yield {
                    "product_type": product_type,
                    "product_name": product_name,
                    "data_type": "product",
                }

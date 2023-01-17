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

                yield response.follow(product_link, self.parse_product)

    def parse_product(self, response):
        cards = response.xpath(
            '//div[contains(@id, "card_list")]//div[contains(@class, "t_row")]'
        )

        for card in cards:
            card_name = card.xpath(
                'input[contains(@class, "cnm")]//@value'
            ).extract_first()
            card_link = card.xpath(
                'input[contains(@class, "link_value")]//@value'
            ).extract_first()

            yield {
                "card_name": card_name,
                "data_type": "product_card",
            }

            yield response.follow(card_link, self.parse_card)

    def parse_card(self, response):
        card_name = (
            response.xpath(
                '//div[contains(@id, "CardSet")]//div[contains(@id, "cardname")]//h1//text()'
            )
            .extract_first()
            .strip()
        )
        card_details = response.xpath(
            '//div[contains(@id, "CardSet")]//div[contains(@class, "top")]//div[contains(@id, "CardTextSet")]//div[contains(@class, "CardText")]//text()'
        ).extract()
        set_list = response.xpath(
            '//div[contains(@id, "update_list")]//div[contains(@class, "t_body")]//div[contains(@class, "t_row")]'
        )

        for set_item in set_list:
            product_release_date = (
                set_item.xpath(
                    'div[contains(@class, "inside")]//div[contains(@class, "time")]//text()'
                )
                .extract_first()
                .strip()
            )
            product_name = (
                set_item.xpath(
                    'div[contains(@class, "inside")]//div[contains(@class, "contents")]//div[contains(@class, "pack_name")]//text()'
                )
                .extract_first()
                .strip()
            )
            card_rarity = (
                set_item.xpath(
                    'div[contains(@class, "inside")]//div[contains(@class, "icon")]//div//span//text()'
                )
                .extract_first()
                .strip()
            )

            yield {
                "card_name": card_name,
                "card_rarity": card_rarity,
                "card_details": card_details,
                "product_name": product_name,
                "product_release_date": product_release_date,
                "data_type": "card",
            }

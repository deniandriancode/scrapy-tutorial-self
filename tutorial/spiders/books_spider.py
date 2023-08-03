from pathlib import Path
import scrapy

class BookSpider(scrapy.Spider):
    name = "books"
    start_urls = ["https://books.toscrape.com/"]

    def parse(self, response):
        for book in response.css("section ol li"):
            title = book.css("h3 a::attr(title)").get()
            rating = book.css("p")[0].attrib["class"].split(" ")[-1]
            rating = self.get_rating(rating)
            price = book.css("div.product_price p.price_color::text").get()
            in_stock = book.css("div.product_price p.instock.availability::text").getall()
            in_stock = "".join(in_stock).strip().replace("\n", "")
            in_stock = True if in_stock.lower() == "in stock" else False
            yield {
                "title": title,
                "rating": rating,
                "price": price,
                "in_stock": in_stock
            }

        next_page = response.css("ul.pager li.next a::attr(href)").get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

    def get_rating(self, rate: str) -> int:
        rate_arr = ["one", "two", "three", "four", "five"]
        for score, r in enumerate(rate_arr, start=1):
            if rate.lower() == r:
                return score

        return -1

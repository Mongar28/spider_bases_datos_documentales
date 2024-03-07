import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = [
        "https://quotes.toscrape.com/page/1/",
        "https://quotes.toscrape.com/page/2/",
    ]

    def parse(self, response):
        for quote in response.xpath('//div[@class="quote"]'):
            print(quote.xpath('.//small[@class="author"]/text()').get())
            print("--------------------------------------------------------")
            yield {
                "text": quote.css("span.text::text").get(),
                "author": quote.xpath('.//small[@class="author"]/text()').get(),
                "tags": quote.css("div.tags a.tag::text").getall(),
            }
            print('________________________________________________________')

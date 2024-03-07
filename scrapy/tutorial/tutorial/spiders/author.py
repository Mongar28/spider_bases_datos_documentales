import scrapy

class AuthorSpider(scrapy.Spider):
    name = "author"
    start_urls = ["https://quotes.toscrape.com/"]

    def parse(self, response):
        # Con esta expresion xpath se buscan todos los links que tengan la palabra author
        author_page_links = response.xpath("//a[contains(@href, 'author')]")
        # con response.follow_all lleva todos los links a la funcion que los parseará (self.parse_author)
        yield from response.follow_all(author_page_links, self.parse_author)
        
        # Una vez se llevan los links de los autores a la funcion que las parse, se pasa de pagina, y se le pasa el link de nuevo al funcion parse.
        pagination_links = response.xpath("//li[@class='next']/a/@href")
        yield from response.follow_all(pagination_links, self.parse)

    def parse_author(self, response):
        def extract_with_css(query):
            # El argumento default="" en el método get()se utiliza para especificar un valor 
            return response.xpath(query).get(default="").strip()

        yield {
            "name": extract_with_css("//h3[@class='author-title']/text()"),
            "birthdate": extract_with_css("//p/span[@class='author-born-date']/text()"),
            "bio": extract_with_css("//div/div[@class='author-description']/text()"),
        }

import json
import scrapy
import os

class AllMovie_Scrapper(scrapy.Spider):
    name = 'allmovie'
    seen_url = set()

    async def start(self):
        self.seen_url = set()
        try:
            path = os.path.join('..', '..', 'data.jsonl')
            with open(path, 'r') as lines:
                for line in lines:
                    data = json.loads(line)
                    self.seen_url.add(data['url'])
        except FileNotFoundError:
            pass
            

        urls = [
            "https://www.allmovie.com/genre/action-adventure-ag100",
            # "https://www.allmovie.com/genre/animation-ag102",
            # "https://www.allmovie.com/genre/anime-ag103",
            # "https://www.allmovie.com/genre/avant-garde-experimental-ag104",
            # "https://www.allmovie.com/genre/biography-ag105",
            # "https://www.allmovie.com/genre/childrens-ag106",
            # "https://www.allmovie.com/genre/comedy-ag107",
            # "https://www.allmovie.com/genre/comedy-drama-ag108",
            # "https://www.allmovie.com/genre/crime-ag109",
            # "https://www.allmovie.com/genre/documentary-ag110",
            # "https://www.allmovie.com/genre/drama-ag111",
            # "https://www.allmovie.com/genre/epic-ag112",
            # "https://www.allmovie.com/genre/family-ag113",
            # "https://www.allmovie.com/genre/fantasy-ag114",
            # "https://www.allmovie.com/genre/history-ag115",
            # "https://www.allmovie.com/genre/horror-ag116",
            # "https://www.allmovie.com/genre/mature-ag101",
            # "https://www.allmovie.com/genre/music-ag117",
            # "https://www.allmovie.com/genre/mystery-suspense-ag118",
            # "https://www.allmovie.com/genre/romance-ag120",
            # "https://www.allmovie.com/genre/science-fiction-ag121",
            # "https://www.allmovie.com/genre/silent-film-ag122",
            # "https://www.allmovie.com/genre/sports-ag123",
            # "https://www.allmovie.com/genre/spy-film-ag124",
            # "https://www.allmovie.com/genre/thriller-ag125",
            # "https://www.allmovie.com/genre/war-ag126",
            # "https://www.allmovie.com/genre/western-ag127",
        ]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
    
    def parse(self, response):
        mh = response.css('.movie-highlights')
        hrefs = mh.css('.title a::attr(href)').getall()
        urls = ['https://www.allmovie.com' + href for href in hrefs]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.movie_parse)


    def movie_parse(self, response):
        url = response.url
        title = response.css('.movie-title::text').get().strip()
        links = response.css('.movie-director a::attr(href)').getall()
        names = response.css('.movie-director a::text').getall()
        directors = [{'name': name.strip(), 'url': response.urljoin(link)} for name, link in zip(names,links)]
        yield {
            'url': url,
            'title': title,
            'directors': directors
        }
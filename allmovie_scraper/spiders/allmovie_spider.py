import json
import scrapy


class AllMovie_Scrapper(scrapy.Spider):
    name = 'allmovie'
    seen_url = set()
    mpaa = set(['G', 'PG', 'PG-13', 'R', 'NC-17', 'NR', 'TV-Y', 'TV-Y7', 'TV-G', 'TV-PG', 'TV-14', 'TV-MA'])

    async def start(self):
        try:
            with open('data.jsonl', 'r') as lines:
                for line in lines:
                    data = json.loads(line)
                    url = data.get('url')
                    if url:
                        self.seen_url.add(url)
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
            if url not in self.seen_url:
                self.seen_url.add(url)
                yield scrapy.Request(url=url, callback=self.movie_parse)
        
        next_href = response.css('.next a::attr(href)').get()
        page_count = response.meta.get('page_count', 1)
        if next_href and page_count < 1:
            next_url = 'https://www.allmovie.com' + next_href
            yield scrapy.Request(
                url=next_url,
                callback=self.parse,
                meta={'page_count': page_count + 1}
            )
            


    def movie_parse(self, response):
        try:
            url = response.url
            title = response.css('.movie-title::text').get().strip()
            poster = response.css('.poster.desktopOnly img::attr(src)').get()
            links = response.css('.movie-director a::attr(href)').getall()
            names = response.css('.movie-director a::text').getall()
            directors = [{'name': name.strip(), 'url': response.urljoin(link)} for name, link in zip(names,links)] if len(names) > 0 else None
            genres = response.css('.details .header-movie-genres a::text').getall()
            subgenres = response.css('.details .header-movie-subgenres a::text').getall()
            subgenres = subgenres if len(subgenres) > 0 else None
            details = response.css('.details span > span::text').getall()
            release = None
            runtime = None
            country = None
            mpaa_rating = None
            for i, detail in enumerate(details):
                if i == 0:
                    release = detail
                elif i == 1:
                    runtime = int(detail.split()[0])
                elif i == 2:
                    if detail in self.mpaa:
                        mpaa_rating = detail
                    else:
                        country = detail
                else:
                    mpaa_rating = detail
            budget = response.css('.budget .charactList::text').get()
            if budget:
                budget = int(budget.strip().replace("$", "").replace(",", ""))
            box_office = response.css('.box-office .charactList::text').get()
            if box_office:
                box_office = int(box_office.strip().replace("$", "").replace(",", ""))
            themes = response.css('.themes .charactList a::text').getall()
            yield {
                'url': url,
                'title': title,
                'poster': poster,
                'image_urls': [poster] if poster else [],
                'directors': directors,
                'genres': genres,
                'subgenres': subgenres,
                'release': release,
                'runtime': runtime,
                'country': country,
                'mpaa_rating': mpaa_rating,
                'budget': budget,
                'box_office': box_office,
                'themes': themes
            }
        except Exception as e:
            yield {'error': e}
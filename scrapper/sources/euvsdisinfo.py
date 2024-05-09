from urllib.request import Request, urlopen
from datetime import datetime
import json

from bs4 import BeautifulSoup

from core.base_source import BaseSource
from db.reviews import reviews_collection
from model.model import Fake, FakeEntry, Author, Review, Location


class ArticleInfo(object):
    def __init__(self, title, summary, media_links, claim_urls, outlet, country, fake_language, review_language,
                 location, fake_date, review_date, review_text, review_summary, url, description, keywords, domain,
                 links):
        self.title = title
        self.summary = summary
        self.media_links = media_links
        self.claim_urls = claim_urls
        self.outlet = outlet
        self.country = country
        self.fake_language = fake_language
        self.review_language = review_language
        self.location = location
        self.fake_date = fake_date
        self.review_date = review_date
        self.review_text = review_text
        self.review_summary = review_summary
        self.url = url
        self.description = description
        self.keywords = keywords
        self.domain = domain
        self.links = links


class EuVSDisInfo(BaseSource):
    def __init__(self):
        self.main_page = 'https://euvsdisinfo.eu/disinformation-cases/'
        self.headers = {'User-Agent': 'FakesRadar', 'organization': 'FakesRadar.org',
                        'domain': 'https://FakesRadar.org', 'email':
                            'dp@fakesradar.org'}

    def open_page(self, href):
        page = urlopen(Request(href, headers=self.headers)).read().decode('utf-8')
        soup = BeautifulSoup(page, 'lxml')

        return soup

    def get_new_article(self):
        new_articles = []
        soup = self.open_page(self.main_page).select('.disinfo-db-posts')[0]
        articles = soup.find_all('div', {'class': 'disinfo-db-post '})

        for article in articles:
            new_articles.append(article.find('a').get('href'))

        return new_articles

    def get_articles_urls(self):
        soup = self.open_page(self.main_page).select('.disinfo-db-current-paging')
        page_count = int(soup[0].contents[19].attrs.get('href')[8:])

        all_articles = []

        while page_count >= 0:
            link = 'https://euvsdisinfo.eu/disinformation-cases/?offset=' + str(page_count)
            articles = self.open_page(link).select('.disinfo-db-cell.cell-title')[1:]

            for article in reversed(articles):
                all_articles.append(article.contents[1].get('href'))

            page_count -= 10

        # print('All urls to articles done')
        return all_articles

    def get_location(self, url):
        # print('get_location start')
        domain = urlopen(url).url.split('/')[2]
        json_url = 'http://api.ipapi.com/api/' + domain + '?access_key=98ede21e1079d805bd1519e983f1e30a'
        open_json = json.load(urlopen(json_url))

        # print('get_location done')
        return open_json['latitude'], open_json['longitude']

    def get_information_from_article(self, article_url):
        date = outlet = country = summary = disproof = language = keywords = location = ''

        # print('get_information_from_article done')

        try:
            soup = self.open_page(article_url).select('.report-content.container')
            parth_one = soup[0].contents[7].contents[1::2]
            parth_two = soup[0].contents[5].contents[1].contents[1::2]

            for cont in parth_one:
                try:
                    value = cont.get_text().lstrip()
                    if value.startswith('Date'):
                        data = value.split(':')[1].strip()
                        date = datetime.strptime(data, '%d.%m.%Y')
                        date = str(datetime.strftime(date, '%Y.%m.%d'))
                    elif value.startswith('Country'):
                        country = value.split(':')[1].strip()
                    elif value.startswith('Language'):
                        language = value.split(':')[1].strip()
                    elif value.startswith('Outlet'):
                        outlet = value.split(':')[1].strip()
                    elif value.startswith('Keywords'):
                        keywords = value.split(':')[1].strip()
                    else:
                        continue
                except:
                    # print(cont)
                    print()

            for count in parth_two:
                try:
                    value = count.get_text().lstrip()

                    if value.startswith('Summary'):
                        summary = value.strip()[27:-73]
                    elif value.startswith('Disproof'):
                        disproof = value[10:-2]
                    else:
                        continue
                except:
                    # print(count)
                    print()

            fake_ulrs = []
            try:
                url = parth_two[0].find('div', {'class': 'report-disinfo-link'}).find('a').get('href')
                # print('get url for location')

                try:
                    location = self.get_location(url)

                except:
                    location = (None, None)

                    # print('Error in location')

                if url.startswith('https://'):
                    url = url[8:]

                elif url.startswith('http://'):
                    url = url[7:]

                fake_ulrs = [url.rstrip('/')]

            except:

                part_fake_ulrs = parth_two[0].contents
                # print('part_fake_ulrs')

                for fake_ulr in part_fake_ulrs:
                    try:
                        url = fake_ulr.get('href')

                        if url is not None and 'web.archive.org/web/' not in url:
                            # print('get url for location')

                            try:
                                location = self.get_location(url)

                            except:
                                location = (None, None)

                            if url.startswith('https://'):
                                url = url[8:]

                            elif url.startswith('http://'):
                                url = url[7:]

                            fake_ulrs.append(url.rstrip('/'))

                    except:
                        # print('except in part_fake_ulrs')
                        continue

            title = 'Fake:' + str(soup[0].find('h2', {'class': 'report-title section_title'}).get_text()).strip()

            try:
                for_media_links = parth_two[1].find_all('a')
                media_links = [media_link.get('href') for media_link in for_media_links]
            except:
                media_links = []

            domain = 'euvsdisinfo.eu'

#             print(title, summary, media_links, fake_ulrs, outlet, country, language, 'english', location, '', date,
#                   disproof, '', article_url, '', keywords, domain, '')

            return ArticleInfo(title=title, summary=summary, media_links=media_links, claim_urls=fake_ulrs,
                               outlet=outlet,
                               country=country, fake_language=language, review_language='english', location=location,
                               fake_date='', review_date=date, review_text=disproof, review_summary='', url=article_url,
                               description='', keywords=keywords, domain=domain, links='')

        except:
            print('Error in ', article_url)

    def upsert_article_by_url(self, url, should_send_message):
        information = self.get_information_from_article(article_url=url)
        print('Information ok')

        try:

            entries = [FakeEntry(type='CreativeWork',
                                 url=url,
                                 location_created=Location(latitude=information.location[0],
                                                           longitude=information.location[1]),
                                 content_location=None,
                                 language=None,
                                 similar=None)
                       for url in information.claim_urls]
            print('entries')

            fake = Fake(author=Author(type='Organization', name=information.outlet, url=None),
                        date=information.fake_date,
                        # source=information.claim_urls,
                        entries=entries)

            # print('fake')

            review = Review(author=Author(type='Organization', name='Euvsdisinfo', url=information.domain),
                            header=information.title,
                            date=information.review_date,
                            url=information.url,
                            fake=fake,
                            rating=None,
                            publisher=Author.fakes_radar(),
                            disproof_urls=information.media_links)

            # print('review')

            reviews_collection.update_one(filter={'claimReviewed': review.header},
                                          update={'$set': review.to_document()},
                                          upsert=True)

            # print('did upsert review with header = ', review.header)

        except:
            print('Error in information: ', information)

    def initial_parse(self):
        print('initial_parse in EUvsDisinfo start')

        articles_urls = self.get_articles_urls()

        for url in articles_urls:
            self.upsert_article_by_url(url=url, should_send_message=False)

        print('initial_parse done')

    def parse(self):
        print('EUvsDisinfo parse start')

        articles_urls = self.get_new_article()

        for url in articles_urls:
            self.upsert_article_by_url(url=url, should_send_message=False)

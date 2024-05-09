import json
from urllib.request import urlopen

from core.base_source import BaseSource
from db.reviews import reviews_collection
from model.model import Fake, FakeEntry, Author, Review, Location, Rating
from datetime import datetime


class ArticleInfo(object):
    def __init__(self, title, summary, media_links, claim_urls, outlet, outlet_type, country, fake_language,
                 review_language, location, fake_date, review_date, review_text, review_summary, url, description,
                 keywords, domain, links, author_type, author_name, claim_type, rating_type, rating_alternate_name,
                 rating_best_rating, rating_value, rating_worst_rating):

        self.title = title
        self.summary = summary
        self.media_links = media_links
        self.claim_urls = claim_urls
        self.outlet = outlet
        self.outlet_type = outlet_type
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
        self.author_type = author_type
        self.author_name = author_name
        self.claim_type = claim_type
        self.rating_type = rating_type
        self.rating_alternate_name = rating_alternate_name
        self.rating_best_rating = rating_best_rating
        self.rating_value = rating_value
        self.rating_worst_rating = rating_worst_rating


class DataCommons(BaseSource):
    def __init__(self):
        self.main_page = 'https://storage.googleapis.com/datacommons-feeds/claimreview/latest/data.json'
        self.headers = {'User-Agent': 'FakesRadar', 'organization': 'FakesRadar.org',
                        'domain': 'https://FakesRadar.org', 'email':
                            'dp@fakesradar.org'}

    def get_location(self, url):
        domain = urlopen(url).url.split('/')[2]
        json_url = 'http://api.ipapi.com/api/' + domain + '?access_key=98ede21e1079d805bd1519e983f1e30a'
        open_json = json.load(urlopen(json_url))

        return open_json['latitude'], open_json['longitude']

    def claim_reviewed_valid(self, item):
        try:
            return item['claimReviewed']
        except:
            return None

    def date_published_valid(self, item):
        try:
            return item['datePublished']    # str(datetime.strftime(datetime.strptime(item['datePublished'], '%Y-%m-%d'), '%Y.%m.%d'))
        except:
            return None

    def url_valid(self, item):
        try:
            return item['url']
        except:
            return None

    def author_type_valid(self, author):
        try:
            return author['@type']
        except:
            return None

    def author_name_valid(self, author):
        try:
            return author['name']
        except:
            return None

    def author_url_valid(self, author):
        try:
            return author['url']
        except:
            return None

    def item_reviewed_date_published_valid(self, item):
        try:
            return item['datePublished']
        except:
            return None

    def item_reviewed_author_valid(self, item):
        try:
            return item['author']
        except:
            return None

    def item_reviewed_author_type_valid(self, author):
        try:
            return author['@type']
        except:
            return None

    def item_reviewed_author_name_valid(self, author):
        try:
            return author['name']
        except:
            return None

    def item_reviewed_appearance_type_valid(self, appearance):
        try:
            return appearance['@type']
        except:
            return None

    def item_reviewed_appearance_url_valid(self, appearance):
        try:
            return appearance['url']
        except:
            return None

    def review_rating_type_valid(self, rating):
        try:
            return rating['@type']
        except:
            return None

    def review_rating_alternate_name_valid(self, rating):
        try:
            return rating['alternateName']
        except:
            return None

    def review_rating_best_rating_valid(self, rating):
        try:
            return rating['bestRating']
        except:
            return None

    def review_rating_rating_value_valid(self, rating):
        try:
            return rating['ratingValue']
        except:
            return None

    def review_rating_worst_rating_valid(self, rating):
        try:
            return rating['worstRating']
        except:
            return None

    def get_information(self, element):
        item_reviewed_appearance_url = item_reviewed_author_name = item_reviewed_author_type = \
            item_reviewed_date_published = item_reviewed_appearance_type = review_rating_type = \
            review_rating_alternate_name = review_rating_best_rating = review_rating_rating_value = \
            review_rating_worst_rating = None

        try:
            item = element['item'][0]

            claim_reviewed = self.claim_reviewed_valid(item)
            date_published = self.date_published_valid(item)
            url = self.url_valid(item)

            author = item['author']
            author_type = self.author_type_valid(author)
            author_name = self.author_name_valid(author)
            author_url = self.author_url_valid(author)

            try:
                item_reviewed = item['itemReviewed']
                item_reviewed_date_published = self.item_reviewed_date_published_valid(item_reviewed)

                item_reviewed_author = self.item_reviewed_author_valid(item_reviewed)
                item_reviewed_author_type = self.item_reviewed_author_valid(item_reviewed_author)
                item_reviewed_author_name = self.item_reviewed_author_name_valid(item_reviewed_author)

                try:
                    item_reviewed_appearance = item_reviewed['firstAppearance']
                    item_reviewed_appearance_type = self.item_reviewed_appearance_type_valid(item_reviewed_appearance)
                    item_reviewed_appearance_url = self.item_reviewed_appearance_url_valid(item_reviewed_appearance)

                except:
                    item_reviewed_appearance = None

            except:
                item_reviewed = None

            try:
                review_rating = item['reviewRating']
                review_rating_type = self.review_rating_type_valid(review_rating)
                review_rating_alternate_name = self.review_rating_alternate_name_valid(review_rating)
                review_rating_best_rating = self.review_rating_best_rating_valid(review_rating)
                review_rating_rating_value = self.review_rating_rating_value_valid(review_rating)
                review_rating_worst_rating = self.review_rating_worst_rating_valid(review_rating)

            except:
                review_rating = None

            return ArticleInfo(title=claim_reviewed, summary=None, media_links=None,
                               claim_urls=item_reviewed_appearance_url, outlet=item_reviewed_author_name,
                               outlet_type=item_reviewed_author_type, country=None, fake_language=None,
                               review_language=None, location=None, fake_date=item_reviewed_date_published,
                               review_date=date_published, review_text=None, review_summary=None, url=url,
                               description=None, keywords=None, domain=author_url, links=None, author_type=author_type,
                               author_name=author_name, claim_type=item_reviewed_appearance_type,
                               rating_type=review_rating_type, rating_alternate_name=review_rating_alternate_name,
                               rating_best_rating=review_rating_best_rating, rating_value=review_rating_rating_value,
                               rating_worst_rating=review_rating_worst_rating)

        except:
            print('Error: ', element)

    def upsert_article_by_url(self, data_feed_element):
        information = self.get_information(data_feed_element)

        try:
            entries = FakeEntry(type=information.claim_type, url=information.claim_urls,
                                location_created=Location(latitude=None,
                                                          longitude=None),
                                content_location=None, language=None, similar=None)

            fake = Fake(author=Author(type=information.outlet_type, name=information.outlet, url=None),
                        date=information.fake_date,
                        entries=entries)

            rating = Rating(type=information.rating_type,
                            alternate=information.rating_alternate_name,
                            best_mark=information.rating_best_rating,
                            worst_mark=information.rating_worst_rating,
                            mark=information.rating_value)

            review = Review(author=Author(type=information.author_type, name=information.author_name, url=None),
                            header=information.title,
                            date=information.review_date,
                            url=information.url,
                            fake=fake,
                            rating=rating,
                            publisher=Author.fakes_radar(),
                            disproof_urls=None)

            reviews_collection.update_one(filter={'claimReviewed': review.header},
                                          update={'$set': review.to_document()},
                                          upsert=True)

        except:
            print('Error in article ', data_feed_element)


    def initial_parse(self):
        print('initial_parse start')
        data = urlopen(self.main_page)
        result = json.load(data)

        data_feed_elements = result['dataFeedElement']

        for data_feed_element in data_feed_elements:
            self.upsert_article_by_url(data_feed_element)


    def parse(self):
        data = urlopen(self.main_page)
        result = json.load(data)

        data_feed_elements = result['dataFeedElement']

        for data_feed_element in data_feed_elements:
            try:
                date_created = data_feed_element['dateCreated'].split('T')[0]
                if date_created == datetime.now().strftime('%Y-%m-%d'):
                    self.upsert_article_by_url(data_feed_element)

            except:
                date_created = data_feed_element['dateModified'].split('T')[0]
                if date_created == datetime.now().strftime('%Y-%m-%d'):
                    self.upsert_article_by_url(data_feed_element)



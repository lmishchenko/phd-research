import csv
from datetime import datetime

from core.base_source import BaseSource
from db.reviews import reviews_collection
from model.model import Fake, FakeEntry, Author, Review, Location


class ArticleInfo(object):
    def __init__(self, title, disproof_links, claim_urls, outlet, outlet_type, country, fake_language,
                 review_language, fake_date, review_date, review_summary, url, claim_type):

        self.title = title
        self.disproof_links = disproof_links
        self.claim_urls = claim_urls
        self.outlet = outlet
        self.outlet_type = outlet_type
        self.country = country
        self.fake_language = fake_language
        self.review_language = review_language
        self.fake_date = fake_date
        self.review_date = review_date
        self.review_summary = review_summary
        self.url = url
        self.claim_type = claim_type


class Nepravda(BaseSource):

    def get_information_from_file(self, row):
        faker = row[1]
        claim_public_data = row[3]
        review_public_data = row[4]
        date = datetime.strptime(review_public_data, '%d.%m.%Y')
        review_date = str(datetime.strftime(date, '%Y.%m.%d'))
        claim = row[5]
        review = row[7]
        link_to_claim = [row[9]]
        link_to_review = row[8]
        claim_type = row[6]

        return ArticleInfo(title=claim, disproof_links=link_to_review, claim_urls=link_to_claim, outlet=faker,
                           outlet_type='Person', country='Ukraine', fake_language='Ukrainian',
                           review_language='Ukrainian', fake_date=claim_public_data, review_date=review_date,
                           review_summary=review, url=link_to_review, claim_type=claim_type)

    def upsert_article_by_url(self, row):
        information = self.get_information_from_file(row=row)

        try:
            entries = [FakeEntry(type='CreativeWork',
                                 url=url,
                                 location_created=Location(latitude=None,
                                                           longitude=None),
                                 content_location=None,
                                 language=None,
                                 similar=None)
                       for url in information.claim_urls]

            fake = Fake(author=Author(type=information.outlet_type, name=information.outlet, url=None),
                        date=information.fake_date,
                        entries=entries)

            review = Review(author=Author(type='Organization', name='Voxukraine', url='voxukraine.org'),
                            header=information.title,
                            date=information.review_date,
                            url=information.url,
                            fake=fake,
                            rating=None,
                            publisher=Author.fakes_radar(),
                            disproof_urls=information.disproof_links)

            reviews_collection.update_one(filter={'claimReviewed': review.header},
                                          update={'$set': review.to_document()},
                                          upsert=True)

        except:
            print('Error in information: ', information)

    def initial_parse(self):
        print('initial_parse nepravda_file start')
        with open('/code/data/nepravda_false.csv', newline='') as f:
            reader = csv.reader(f)
            for row in reader:
                self.upsert_article_by_url(row)

        with open('/code/data/nepravda_manipulation.csv', newline='') as f:
            reader = csv.reader(f)
            for row in reader:
                self.upsert_article_by_url(row)

    def parse(self):
        pass

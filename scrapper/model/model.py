class Review(object):
    def __init__(self, author, header, date, url, fake, rating, publisher, disproof_urls):
        self.author = author
        self.header = header
        self.date = date
        self.url = url
        self.fake = fake
        self.rating = rating
        self.publisher = publisher
        self.disproof_urls = disproof_urls

    def to_document(self):
        return {
            '@type': 'ClaimReview',
            'author': self.author.to_document(),
            'claimReviewed': self.header,
            'datePublished': self.date,
            'itemReviewed': self.fake.to_document(),
            'reviewRating': '' if self.rating is None else self.rating.to_document(),
            'sdPublisher': self.publisher.to_document(),
            'url': self.url,
            'disproof_urls': self.disproof_urls
        }


class Author(object):

    @staticmethod
    def fakes_radar():
        return Author(type='Organization', name='FakesRadar', url='https://fakesradar.org')

    def __init__(self, type, name, url):
        self.type = type
        self.name = name
        self.url = url

    def to_document(self):
        return {
            '@type': self.type,
            'name': self.name,
            'url': self.url
        }


class Location(object):
    def __init__(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude

    def to_document(self):
        return {
            'latitude': self.latitude,
            'longitude': self.longitude
        }


class Fake(object):
    def __init__(self, author, date, entries):      # source,
        self.author = author
        self.date = date
        # self.source = source
        self.entries = entries

    def to_document(self):
        return {
            '@type': 'Claim',
            'author': self.author.to_document(),
            'datePublished': self.date,
            # 'urls': self.source,
            'appearance': [x.to_document() for x in self.entries]
        }


class FakeEntry(object):
    def __init__(self, type, url, location_created, content_location, language, similar):
        self.type = type
        self.url = url
        self.location_created = location_created
        self.content_location = content_location
        self.language = language
        self.similar = similar

    def to_document(self):
        return {
            '@type': self.type,
            'url': self.url,
            'locationCreated': self.location_created.to_document(),
            'contentLocation': self.content_location,
            'inLanguage': self.language,
            'sameAs': self.similar
        }


class Rating(object):
    def __init__(self, type, best_mark, worst_mark, mark, alternate):
        self.type = type
        self.best_mark = best_mark
        self.worst_mark = worst_mark
        self.mark = mark
        self.alternate = alternate

    def to_document(self):
        return {
            '@type': 'Rating',
            'alternateName': self.type,

            'bestRating': self.best_mark,
            'ratingValue': self.mark,
            'worstRating': self.worst_mark
        }

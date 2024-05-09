from configuration.base import BaseConfiguration


class DevelopmentConfiguration(BaseConfiguration):
    def needs_initial_parse(self):
        return True

    def mongo_host(self):
        return 'localhost'

    def mongo_port(self):
        return 27017

    def needs_auth(self):
        return False

    def mongo_user(self):
        pass

    def mongo_password(self):
        pass

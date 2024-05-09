from configuration.base import BaseConfiguration


class ProductionConfiguration(BaseConfiguration):
    def needs_initial_parse(self):
        return True

    def mongo_host(self):
        return '10.166.0.4'

    def mongo_port(self):
        return 27017

    def needs_auth(self):
        return True

    def mongo_user(self):
        return 'fakes_radar_write_user'

    def mongo_password(self):
        return 'Gm6w9aeVxgB2zsTSkFXW4LmppQE992wN'

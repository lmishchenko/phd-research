class BaseConfiguration(object):
    def needs_initial_parse(self):
        pass

    def mongo_host(self):
        pass

    def mongo_port(self):
        pass

    def needs_auth(self):
        pass

    def mongo_user(self):
        pass

    def mongo_password(self):
        pass
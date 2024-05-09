class SourceRunner(object):
    def __init__(self, source, configuration):
        self.source = source
        self.configuration = configuration

    def run(self):
        if self.configuration.needs_initial_parse():
            self.source.initial_parse()
            
        self.source.parse()

import sys

from configuration.development import DevelopmentConfiguration
from configuration.production import ProductionConfiguration

configuration = ProductionConfiguration() if 'configuration=prod' in sys.argv else DevelopmentConfiguration()

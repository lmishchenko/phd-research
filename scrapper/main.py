import time

from core.source_runner import SourceRunner
from sources.euvsdisinfo import EuVSDisInfo
from model.common import DataCommons
from sources.nepravda import Nepravda
from configuration.resolver import configuration


if __name__ == '__main__':
    while True:
        source_dc = DataCommons()
        source_eu = EuVSDisInfo()
        source_nf = Nepravda()
        runner_dc = SourceRunner(source_dc, configuration)
        runner_eu = SourceRunner(source_eu, configuration)
        runner_nf = SourceRunner(source_nf, configuration)
        runner_nf.run()
        runner_dc.run()
        runner_eu.run()
        
        time.sleep(18000)

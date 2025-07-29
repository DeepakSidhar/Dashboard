import subprocess
import os
from logger import logger

RUN_VULNERABILITY_SCAN = os.environ.get('RUN_VULNERABILITY_SCAN', 'True').lower() =='true' # checking if the prod env server if the files are there

def run_pip_audit():
    if RUN_VULNERABILITY_SCAN:
        logger.info("Running vulnerability scan ")
        result = subprocess.run("pip-audit", capture_output=True, text=True)
        if result.returncode != 0:
            logger.warn("Vulnerabilities in the system")
            logger.warn(result.stdout)
        else:
            logger.info('No known vulnerabilities found')



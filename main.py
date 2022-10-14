"""
This script spins up the docker containers for the java and the python environments.
It sets the test parameters and then runs the python and java containers one at the time.
Each such execution is and observation that will be kept in the mounted directory, and at the end, the reports are to be analyzed by the jupyter notebook environment 
"""

import os
import time
NUMBER_OF_OBSERVATIONS = 50

HOW_MANY_THREADS = 500
RAMP_UP = 10
DURATION = 600


for i in range(NUMBER_OF_OBSERVATIONS):
    # python:
    os.system(
        f"docker run -v C:\\benchmark\\py_outs:/usr/src/app/output -e HOW_MANY_THREADS={HOW_MANY_THREADS} -e RAMP_UP={RAMP_UP} -e DURATION={DURATION} py-jmeter-benchmark"
    )
    time.sleep(5)

    # java:
    os.system(
        f"docker run -v C:\\benchmark\\java_outs:/usr/src/app/output -e HOW_MANY_THREADS={HOW_MANY_THREADS} -e RAMP_UP={RAMP_UP} -e DURATION={DURATION} java-jmeter-benchmark"
    )
    
    time.sleep(5)


import os

NUMBER_OF_OBSERVATIONS = 10

HOW_MANY_THREADS = 500
RAMP_UP = 10
DURATION = 600


for i in range(NUMBER_OF_OBSERVATIONS):
    # python:
    os.system(
        f"docker run -v C:\\benchmark\\py_outs:/usr/src/app/output -e HOW_MANY_THREADS={HOW_MANY_THREADS} -e RAMP_UP={RAMP_UP} -e DURATION={DURATION} py-jmeter-benchmark"
    )

    # java:
    os.system(
        f"docker run -v C:\\benchmark\\java_outs:/usr/src/app/output -e HOW_MANY_THREADS={HOW_MANY_THREADS} -e RAMP_UP={RAMP_UP} -e DURATION={DURATION} java-jmeter-benchmark"
    )


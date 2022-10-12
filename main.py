import os

NUMBER_OF_OBSERVATIONS = 2

HOW_MANY_THREADS = 100
RAMP_UP = 1
DURATION = 600


# python:
for i in range(NUMBER_OF_OBSERVATIONS):
    os.system(
        f"docker run -v C:\\benchmark\\py_outs:/usr/src/app/output -e HOW_MANY_THREADS={HOW_MANY_THREADS} -e RAMP_UP={RAMP_UP} -e DURATION={DURATION} py-jmeter-benchmark"
    )

# java:
for i in range(NUMBER_OF_OBSERVATIONS):
    os.system(
        "docker run -v C:\\benchmark\\java_outs:/usr/src/app/output -e HOW_MANY_THREADS={HOW_MANY_THREADS} -e RAMP_UP={RAMP_UP} -e DURATION={DURATION} java-jmeter-benchmark"
    )

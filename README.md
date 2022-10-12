# pymeter-benchmark
benchmarking JMeter's java-dsl with python dsl

## python

'''
docker build -t py-jmeter-benchmark python-dsl-environment
docker run py-jmeter-benchmark
'''

## JAVA
'''
docker build -t java-jmeter-benchmark java-dsl-environment
docker run java-jmeter-benchmark
'''
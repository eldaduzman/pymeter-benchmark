# pymeter-benchmark
benchmarking JMeter's java-dsl with python dsl

## python

'''
docker build -t py-jmeter-benchmark python-dsl-environment
docker run -v C:\benchmark\py_outs:/usr/src/app/output py-jmeter-benchmark
'''

## JAVA
'''
docker build -t java-jmeter-benchmark java-dsl-environment
docker run -v C:\benchmark\java_outs:/usr/src/app/output java-jmeter-benchmark
'''
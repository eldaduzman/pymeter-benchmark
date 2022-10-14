# pymeter-benchmark
[![Generic badge](https://img.shields.io/badge/revision-1.0-blue.svg)](https://shields.io/)

## File structure

```
Folder PATH listing
Volume serial number is 1084-BED0
C:.
|   .gitignore
|   .pre-commit-config.yaml
|   LICENSE
|   main.py
|   README.md
+---java-dsl-environment
|   |   Dockerfile
|   |   pom.xml
|   |   
|   +---src
|   |   +---main
|   |   |   \---java
|   |   |       \---com
|   |   |           \---java
|   |   |               \---dsl
|   |   |                   \---environment
|   |   |                           App.java
|   |   |                           
|   |   \---test
|   |       \---java
|   |           \---com
|   |               \---java
|   |                   \---dsl
|   |                       \---environment
|   |                               AppTest.java                         
+---notebooks
|       requirements.in
|       statistical-analysis.ipynb
|       
+---python-dsl-environment
|       Dockerfile
|       main.py
|       requirements.in
|       requirements.txt
|

```

## Abstract

The main goal of this project is to validate the performance of [pymeter](https://github.com/eldaduzman/pymeter).
More spesifically, it answers the question whether there is any significant performance difference between pymeter and [JMeter-DSL](https://abstracta.github.io/jmeter-java-dsl/)


For that purpose, I conducted an experiment, in which 2 identical tests cases, one written in JMeter-DSL and the other written in pymeter had been executed repeatedly.
After they were executed, I analyzed their result to check for any outcome difference.

I've found statistically insignificant differences and it overall appears that there are no performance differences.

## Introduction

**JMeter** is one of the most popular and long standing load testing tools.
The original implementation is a gui based tool to script load test scenarios in a hierarchical structure, however this came with limitations and short comings.

For once, upgrading JMeter versions is painful, as it involved manually downloading and deploying executable files.
This became very clear when [log4j](https://en.wikipedia.org/wiki/Log4Shell) vulnerability was discovered, and software developers needed to instantly upgrade their log4j versions.
With JMeter, this was even more painful without a proper package management system such as maven or gradel.

Other limitations include difficulty to share code between different projects, using source control management tools such as git or svn.
It is quite difficult to extend JMeter and it requires a GUI editor which means to use additional development environment instead of using a single IDE for all needs.

The awesome folks at [abstracta](https://abstracta.us/) have put up an amazing amount of work to deliver [JMeter-DSL](https://abstracta.github.io/jmeter-java-dsl/), which allows developers to use plain Java to script their load test scenarios, and pretty much solve all the pain mentioned above.

An example for a JMeter-DSL test script would be:

```
import org.junit.Test;

import static us.abstracta.jmeter.javadsl.JmeterDsl.*;
import java.time.Instant;
import java.io.IOException;
import java.time.Duration;
import java.nio.file.Paths;

public class AppTest {

        @Test
        public void shouldAnswerWithTrue() throws IOException {

                String reportPath = Paths.get("output", "html-report-" + Instant.now().toString().replace(":", "-")).toString();
                testPlan(
                                threadGroup()
                                                .rampToAndHold(100, Duration.ofSeconds(1), Duration.ofSeconds(60))
                                                .children(httpSampler("echo_get_request", "https://postman-echo.com/get?var=1")
                                                .children(uniformRandomTimer(2000, 5000)))

                                ,
                                htmlReporter(reportPath)).run();
        }
}
```

To capitalize on the success of JMeter-DSL, I created the [pymeter](https://github.com/eldaduzman/pymeter) project which aimed to enable developers to write their JMeter scripts using python.

Since JMeter requires a JAVA runtime to run on, I've decided to use JMeter-DSL as my engine, and to bridge between the JAVA and python runtimes by using [pyjnius](https://github.com/kivy/pyjnius)

Pyjnius offers an easy bridge between python and JAVA using the [Java Native Interface (JNI)](https://en.wikipedia.org/wiki/Java_Native_Interface), this allows using the java classes directly from the python code without spinning up the entire java runtime and rely on heavy inter-process communication.

An example for a pymeter script would be:
```
from pymeter.api.config import TestPlan, ThreadGroupWithRampUpAndHold
from pymeter.api.samplers import HttpSampler
from pymeter.api.reporters import HtmlReporter
from pymeter.api.timers import UniformRandomTimer


HOW_MANY_THREADS = int(os.environ.get("HOW_MANY_THREADS", 10))
RAMP_UP = int(os.environ.get("RAMP_UP", 1))
DURATION = int(os.environ.get("DURATION", 60))

timer = UniformRandomTimer(2000, 5000)
html_reporter = HtmlReporter()

http_sampler = HttpSampler(
    "echo_get_request", "https://postman-echo.com/get?var=1", timer
)

thread_group = ThreadGroupWithRampUpAndHold(100, 1, 60, http_sampler)

test_plan = TestPlan(thread_group, html_reporter)
stats = test_plan.run()

```

Pymeter successfully defines and runs the JMeter tests with it's API, however, the bridging implementation raises a legitimate concern regarding performance.
For once, python doesn't allow multi core threading with the implementation of the [Global Interpreter Lock (GIL)](https://realpython.com/python-gil/) and since JMeter's architecture is thread base, this might lead to problems.

Another concern is pythons slowness compared to java that could be **orders of magnitude** slower! [link](https://programming-language-benchmarks.vercel.app/python-vs-java)


Theoretically, these concern, while being legit, are nullified, as the actual JMeter test runs as JAVA code, which means that the GIL doesn't apply to it and it is statically typed which should make it as fast as java.

This benchmark aimed to take the theoretical argument and put it to empirical test.

I conducted an experiment in which 2 identical test scripts, one written in JAVA and one written in python were executed repeatedly.
And then these results would be analyzed for statistical significance.

## Experimental materials.

### Java environment:

The java test code is powered by junit and maven, the script can be found [here](https://github.com/eldaduzman/pymeter-benchmark/blob/main/java-dsl-environment/src/test/java/com/java/dsl/environment/AppTest.java) and the docker file is [here](https://github.com/eldaduzman/pymeter-benchmark/blob/main/java-dsl-environment/Dockerfile)

### Python environment:

to avoid any possible optimizations, I used a flat script with no main definition.
Test script can be found [here](https://github.com/eldaduzman/pymeter-benchmark/blob/main/python-dsl-environment/main.py) and the docker file is [here](https://github.com/eldaduzman/pymeter-benchmark/blob/main/python-dsl-environment/Dockerfile)

### Execution:

To run the experiments periodically, I created the two docker images:
1. image for python environment
```docker build -t py-jmeter-benchmark python-dsl-environment```

2. image for java environment
```docker build -t java-jmeter-benchmark java-dsl-environment```

having the two iamges created, I can run them with the ```docker run``` command.

Both test scripts expect 3 environment variables:
- HOW_MANY_THREADS - the number of threads to spin up in JMeter
- RAMP_UP - thread rampup period in seconds
- DURATION - the duration of the test in seconds

Both scripts save the results in HTML format in a new folder named by the date of the execution.
To keep the results after the docker execution, I mounted the directory  `c:\benchmark` to the outputs directory


The final execution flow is to run a python test and then a java test periodically, in total **27** test of each had been executed with the following configurations:
- HOW_MANY_THREADS=500
- RAMP_UP=10
- DURATION=600

Each virtual user in the test scripts send a get request to the [postman-echo](https://postman-echo.com/) server every 2000-5000 milliseconds using the [uniform random timer](https://www.blazemeter.com/blog/jmeter-timer)

### Measurements:

In each result folder, there's the file ```statistics.json``` which contains summary information of the test execution.
An example of such file would be:

```
{
  "Total" : {
    "transaction" : "Total",
    "sampleCount" : 82080,
    "errorCount" : 0,
    "errorPct" : 0.0,
    "meanResTime" : 178.09485867446304,
    "medianResTime" : 150.0,
    "minResTime" : 137.0,
    "maxResTime" : 1259.0,
    "pct1ResTime" : 166.0,
    "pct2ResTime" : 557.9000000000015,
    "pct3ResTime" : 613.9900000000016,
    "throughput" : 135.01798759374194,
    "receivedKBytesPerSec" : 80.38196957571651,
    "sentKBytesPerSec" : 17.009101952727256
  },
  "echo_get_request" : {
    "transaction" : "echo_get_request",
    "sampleCount" : 82080,
    "errorCount" : 0,
    "errorPct" : 0.0,
    "meanResTime" : 178.09485867446304,
    "medianResTime" : 150.0,
    "minResTime" : 137.0,
    "maxResTime" : 1259.0,
    "pct1ResTime" : 166.0,
    "pct2ResTime" : 557.9000000000015,
    "pct3ResTime" : 613.9900000000016,
    "throughput" : 135.01798759374194,
    "receivedKBytesPerSec" : 80.38196957571651,
    "sentKBytesPerSec" : 17.009101952727256
  }
}
```

I took the `total` portion and extracted out of it the following fields:

1. sampleCount - total number of requests sent
2. throughput - rate of requests per seconds
3. errorPct - percentage of requests resulted in error
4. meanResTime - the average of response time.

### Statistical analysis:

Statistical analysis was conducted in a [jupyter notebook](https://jupyter.org/), visualizations were powered by [plotly](https://plotly.com/), data processing with [pandas](https://pandas.pydata.org/) and the statistical computation were done with [scipy](https://scipy.org/).

For each of the measurements, the effect size was calculated using [Cohen's d](https://statisticsbyjim.com/basics/cohens-d/), statistical significance was calculated using [T test](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.ttest_ind.html) with confidence interval of 5%.

### Results:

#### sampleCount:
<!-- 
<div style="text-align:center">
        <img src="images\sampleCount-table.histogram" width="50%" />
        <img src="images\sampleCount-table.box" width="50%" />
</div>

<br/>
<br/>
<br/>
<br/> -->


![](images\sampleCount-table.png)
>>>> sample count table
>>>>>> p-value > 0.05 indicates statistical insignificance

<br/>
<br/>
<br/>
<br/>

![](images\sampleCount-histogram.png)
>>>> sample count histogram

<br/>
<br/>
<br/>
<br/>


![](images\sampleCount-box.png)
>>>> sample count box-plot

<br/>
<br/>
<br/>
<br/>

#### throughput:

![](images\throughput-table.png)
>>>> throughput count table
>>>>>> p-value > 0.05 indicates statistical insignificance


<br/>
<br/>
<br/>
<br/>


![](images\throughput-histogram.png)
>>>> throughput count histogram


<br/>
<br/>
<br/>
<br/>


![](images\throughput-box.png)
>>>> throughput count box-plot

<br/>
<br/>
<br/>
<br/>

#### errorPct:

![](images\errorPct-table.png)
>>>> errorPct count table
>>>>>> p-value > 0.05 indicates statistical insignificance


<br/>
<br/>
<br/>
<br/>


![](images\errorPct-histogram.png)
>>>> errorPct count histogram


<br/>
<br/>
<br/>
<br/>


![](images\errorPct-box.png)
>>>> errorPct count box-plot

<br/>
<br/>
<br/>
<br/>

#### meanResTime:

![](images\meanResTime-table.png)
>>>> meanResTime count table
>>>>>> p-value > 0.05 indicates statistical insignificance


<br/>
<br/>
<br/>
<br/>


![](images\meanResTime-histogram.png)
>>>> meanResTime count histogram

<br/>
<br/>
<br/>
<br/>


![](images\meanResTime-box.png)
>>>> meanResTime count box-plot

<br/>
<br/>
<br/>
<br/>


## Conclusion

In all 4 measurements: sampleCount, throughput, errPct and meanResTime, differences between java runtime and python runtime were statistically insignificant.

This supports the theoretical argument that the JNI bridging provides sound performance and do not hinder pymeters capacity to generate load.

package com.java.dsl.environment;

import org.junit.Test;

import static us.abstracta.jmeter.javadsl.JmeterDsl.*;
import java.time.Instant;
import java.io.IOException;
import java.time.Duration;

public class AppTest {

        @Test
        public void shouldAnswerWithTrue() throws IOException {
                String report = "html-report-" + Instant.now().toString().replace(":", "-");
                testPlan(
                                threadGroup()
                                                .rampToAndHold(10, Duration.ofSeconds(1), Duration.ofSeconds(60))
                                                .children(
                                                                httpSampler("echo_get_request",
                                                                                "https://postman-echo.com/get?var=1")
                                                                                .children(uniformRandomTimer(2000,
                                                                                                5000)))

                                ,
                                htmlReporter(report) + ".html").run();
        }
}
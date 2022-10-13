package com.java.dsl.environment;

import org.junit.Test;

import static us.abstracta.jmeter.javadsl.JmeterDsl.*;
import java.time.Instant;
import java.io.IOException;
import java.time.Duration;
import java.nio.file.Paths;

public class AppTest {

        @Test
        public void shouldAnswerWithTrue() throws IOException {
                int HOW_MANY_THREADS = Integer.parseInt(System.getenv("HOW_MANY_THREADS"));
                int RAMP_UP = Integer.parseInt(System.getenv("RAMP_UP"));
                int DURATION = Integer.parseInt(System.getenv("DURATION"));
                String reportPath = Paths.get("output", "html-report-" + Instant.now().toString().replace(":", "-")).toString();
                testPlan(
                                threadGroup()
                                                .rampToAndHold(HOW_MANY_THREADS, Duration.ofSeconds(RAMP_UP), Duration.ofSeconds(DURATION))
                                                .children(
                                                                httpSampler("echo_get_request",
                                                                                "https://postman-echo.com/get?var=1")
                                                                                .children(uniformRandomTimer(2000,
                                                                                                5000)))

                                ,
                                htmlReporter(reportPath)).run();
        }
}

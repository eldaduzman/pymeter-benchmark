import os
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

thread_group = ThreadGroupWithRampUpAndHold(HOW_MANY_THREADS, RAMP_UP, DURATION, http_sampler)

test_plan = TestPlan(thread_group, html_reporter)
stats = test_plan.run()

from pymeter.api.config import TestPlan, ThreadGroupWithRampUpAndHold
from pymeter.api.samplers import HttpSampler
from pymeter.api.reporters import HtmlReporter
from pymeter.api.timers import UniformRandomTimer

timer = UniformRandomTimer(2000, 5000)
html_reporter = HtmlReporter()

http_sampler = HttpSampler(
    "echo_get_request", "https://postman-echo.com/get?var=1", timer
)

thread_group = ThreadGroupWithRampUpAndHold(10, 1, 60, http_sampler)

test_plan = TestPlan(thread_group, html_reporter)
stats = test_plan.run()

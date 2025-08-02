import os
import sys

from django.test.runner import DiscoverRunner

try:
    import xmlrunner
except ImportError:
    xmlrunner = None


class JUnitXMLTestRunner(DiscoverRunner):
    """
    A Django test runner that extends DiscoverRunner
    to provide JUnit XML output.
    """

    def __init__(self, junit_output_dir=None, **kwargs):
        # Extract junit_output_dir from kwargs if present
        if "junit_output_dir" in kwargs:
            junit_output_dir = kwargs.pop("junit_output_dir")
        super().__init__(**kwargs)
        self.junit_output_dir = junit_output_dir or os.environ.get(
            "JUNIT_OUTPUT_DIR", "test-results"
        )

    @classmethod
    def add_arguments(cls, parser):
        super().add_arguments(parser)
        parser.add_argument(
            "--junit-output-dir",
            default=os.environ.get("JUNIT_OUTPUT_DIR", "test-results"),
            help="Directory to store JUnit XML test results (default: test-results)",
        )

    def get_test_runner_kwargs(self):
        """Return kwargs for the test runner."""
        kwargs = super().get_test_runner_kwargs()

        if xmlrunner is not None:
            # Ensure the output directory exists
            os.makedirs(self.junit_output_dir, exist_ok=True)

            # Replace the default test runner with XMLTestRunner
            kwargs["stream"] = sys.stdout
            kwargs["verbosity"] = self.verbosity
            kwargs["failfast"] = self.failfast
            kwargs["buffer"] = self.buffer

            # Return a custom runner factory that creates XMLTestRunner
            return kwargs
        else:
            # Fall back to default behavior if xmlrunner is not available
            return kwargs

    def get_resultclass(self):
        """Return the result class to use."""
        if xmlrunner is not None:
            return xmlrunner.result.XMLTestResult
        else:
            return super().get_resultclass()

    def run_suite(self, suite, **kwargs):
        """Run the test suite with JUnit XML output if available."""
        if xmlrunner is not None:
            # Create XMLTestRunner with JUnit XML output
            runner = xmlrunner.XMLTestRunner(
                output=self.junit_output_dir,
                verbosity=self.verbosity,
                failfast=self.failfast,
                buffer=self.buffer,
                stream=kwargs.get("stream", sys.stdout),
            )
            return runner.run(suite)
        else:
            # Fall back to default behavior
            return super().run_suite(suite, **kwargs)

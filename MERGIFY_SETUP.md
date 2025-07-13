# Mergify CI Insights Setup

This document explains how to set up Mergify CI Insights integration for Django's test suite.

## Prerequisites

1. A Mergify account with CI Insights enabled
2. A Mergify API token

## Setup Steps

### 1. Get Your Mergify Token

1. Log into your Mergify dashboard
2. Navigate to your CI Insights settings
3. Generate or copy your API token

### 2. Add Token to GitHub Repository

1. Go to your repository's **Settings** → **Secrets and variables** → **Actions**
2. Click **New repository secret**
3. Name: `MERGIFY_TOKEN`
4. Value: Your Mergify API token
5. Click **Add secret**

### 3. Verify Integration

Once the token is set up, your GitHub Actions workflows will automatically:

- Generate JUnit XML test reports
- Upload test results to Mergify CI Insights
- Provide enhanced test analytics and insights

## What's Included

The integration has been added to the following workflows:

- **tests.yml** - Windows SQLite tests
- **python_matrix.yml** - Python version matrix tests
- **schedule_tests.yml** - Scheduled tests (Windows, PostgreSQL, Selenium)
- **selenium.yml** - Selenium tests
- **postgis.yml** - PostGIS/GeoDjango tests
- **screenshots.yml** - Visual regression tests

## Test Results Location

- **Local**: `tests/test-results/*.xml`
- **CI Artifacts**: Available as GitHub Actions artifacts
- **Mergify**: Automatically uploaded to CI Insights dashboard

## Troubleshooting

If you encounter issues:

1. Verify the `MERGIFY_TOKEN` secret is properly set
2. Check that the token has the correct permissions
3. Ensure the `unittest-xml-reporting` package is installed in your test environment
4. Review the GitHub Actions logs for any upload errors

For more information, see the [Mergify CI Insights documentation](https://docs.mergify.com/ci-insights/). 
#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `pywhip` package."""

import pytest

from click.testing import CliRunner

from pywhip import cli


@pytest.fixture
def response():
    """Sample pytest fixture.

    See more at: http://doc.pytest.org/en/latest/fixture.html
    """
    # import requests
    # return requests.get('https://github.com/audreyr/cookiecutter-pypackage')


def test_command_line_interface():
    """Test the CLI."""
    runner = CliRunner()
    result = runner.invoke(cli.main)
    assert result.exit_code == 2 # provide error on missing input
    help_result = runner.invoke(cli.main, ['--help'])
    assert help_result.exit_code == 0
    assert '--help            Show this message and exit.' in \
           help_result.output

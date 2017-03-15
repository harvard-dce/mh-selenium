
## pytest-splinter UI test scripts

The tests in this directory use [splinter](http://splinter.readthedocs.io), a selenium abstraction layer, and [pytest](http://docs.pytest.org/), a python testing framework, to test the DCE Matterhorn Opencast admin and paella player UI.

### Running the tests

From the base `mh-ui-testing` directory you can execute the test scripts individually using `pytest`:

    pytest tests/test_something.py [options]

or all at once:

    pytest tests/ [options]
    

### Creating new tests

All tests should use standard **pytest** structure and syntax, and make use of fixtures defined in `tests/conftest.py`.

from pytest_reqs import check_requirements


def pytest_collection_modifyitems(config, session, items):
    check_requirements(config, session, items)

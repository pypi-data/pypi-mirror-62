"""Pytest configuration."""

import pytest

from xoinvader import application
from xoinvader import state


@pytest.fixture
def mock_application(request):

    def inner():
        return MockedApplication()

    request.addfinalizer(MockedApplication._finalize)
    return inner


@pytest.fixture
def mock_state(request, mock_application):

    def inner(mock_app=False):
        if mock_app:
            mock_application()
        application.get_current().register_state(MockedState)
        return application.get_current().state

    def stop():
        try:
            application.get_current().deregister_state(MockedState.__name__)
        except application.ApplicationNotInitializedError:
            pass

    request.addfinalizer(stop)

    return inner


class MockedApplication(application.Application):

    @staticmethod
    def _finalize():
        app = application.get_current()
        app.stop()


class MockedState(state.State):
    pass

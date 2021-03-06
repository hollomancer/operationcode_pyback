from abc import ABC, abstractmethod
from uuid import uuid4

from ocbot.external.all import external_router


class RouteHandler(ABC):
    # __slots__ = ()
    # "*," prevents erroneous keyword arguments
    def __init__(self):
        self.key = uuid4()
        self.response = []
        self.api_dict = {}
        self.db_dict = {}
        self.text_dict = {}

    def event_route(self):
        self.api_calls()
        self.database_calls()
        self.build_templates()
        self.build_responses()
        self.final_response()

    @abstractmethod
    def api_calls(self):
        pass

    @abstractmethod
    def build_responses(self):
        pass

    @abstractmethod
    def database_calls(self):
        pass

    @abstractmethod
    def build_templates(self):
        pass

    def include_resp(self, method, *args, **kwargs):
        self.response.append(method(*args, **kwargs))

    def final_response(self):
        external_router(self.response)
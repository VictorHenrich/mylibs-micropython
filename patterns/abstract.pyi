from typing import Mapping, Type, Callable

class AbstractClass:
    default_error_messages: Mapping[str, str]

    def __init__(self, class_: Type) -> None: ...
    @classmethod
    def abstract_method(cls, function: Callable) -> Callable: ...

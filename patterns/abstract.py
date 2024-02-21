class AbstractClass:
    default_error_messages = {
        "constructor": "It is not possible to instantiate the AbstractSocketConnection class directly",
        "abstract_method": "Method was not implemented!",
    }

    def __init__(self, class_):
        if type(self) is class_:
            raise NotImplementedError(
                AbstractClass.default_error_messages["constructor"]
            )

    @classmethod
    def abstract_method(cls):
        def wrapper(*args, **kwargs):
            raise NotImplementedError(cls.default_error_messages["abstract_method"])

        return wrapper

class Wrapper:
    def __init__(self, wrapped):
        # hit __dict__ directly to avoid calling __setattr__ before `_fallback` is assigned
        self.__dict__['_wrapped'] = wrapped

    def __getattr__(self, attr):
        return getattr(self._wrapped, attr)

    def __setattr__(self, attr, value):
        if attr not in self.__dict__ and hasattr(self._wrapped, attr):
            setattr(self._wrapped, attr, value)
        else:
            # default behavior
            super().__setattr__(attr, value)

from screen.utils import *

class Scraper:
    def get_data(self, *args, **kwargs):
        return {}

    def initialize(self, source_image, *args, **kwargs):
        self.source_image = source_image.copy()
        self.args = args
        self.kwargs = kwargs

        self.preprocess()

    @with_screenshot_source
    def __run__(self, *args, **kwargs):
        self.initialize(kwargs.pop('source_image'), *args, **kwargs)
        return self.get_data(*args, **kwargs)

    def __call__(self, operation, *args, **kwargs):
        def __w(*args, **kwargs):
            kwargs.update(self.__run__(*args, **kwargs))
            return operation(*args, **kwargs)

        return __w

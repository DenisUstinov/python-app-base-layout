from .database import Database
from .models import App, Source

MODEL_MAP = {
    "App": App,
    "Source": Source,
}

class Storage(Database):
    def __init__(self, settings):
        self.settings = settings
        super().__init__(self.settings["PATH"])

    async def initialize(self):
        await self.create_table()
        await self._add_initial_source()

    async def _add_initial_source(self):
        for data in self.settings["SOURCES"]:
            await self.insert_record(Source, data)

    async def get_sources(self):
        fields = ['id', 'url', 'selectors', 'timeout']
        records = await self.select_fields(Source, fields=fields)
        return records

    async def save_data(self, model, data):
        model_cls = MODEL_MAP.get(model)
        if not model_cls:
            raise ValueError(f"Unknown model: {model}")
        await self.insert_record(model_cls, data)
from src.data_access.base.source import ImagerySource
from dataclasses import asdict


class Orchestrator:
    def __init__(self):
        self.source = None

    def set_source(self, source: ImagerySource):
        self.source = source

    def run_process(self):
        image_id = self.source.search()
        metadata = self.source.get_metadata(image_id)

        return {"image_id": image_id, "metadata": asdict(metadata)}

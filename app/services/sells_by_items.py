from app.repository import SellsByItemsRepository
from app.services import ReportService


class SellsByItemsService(ReportService):
    def __init__(self, repository: SellsByItemsRepository):
        self.repository = repository

    def get_report(self, filters: dict):
        return self.repository.get_report(filters)

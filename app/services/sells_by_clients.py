from app.repository import Sells_By_Client_Repository
from app.services import ReportService


class SellsByUsersService(ReportService):
    def __init__(self, repository: Sells_By_Client_Repository):
        self.repository = repository

    def get_report(self, filters: dict):
        return self.repository.get_report(filters)

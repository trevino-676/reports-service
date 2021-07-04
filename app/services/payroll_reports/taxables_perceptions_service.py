from app.repository import TaxablesPerceptionsRepository
from app.services import ReportService


class TaxablesPerceptionsService(ReportService):
    def __init__(self, repository: TaxablesPerceptionsRepository):
        self.repository = repository

    def get_report(self, filters: dict):
        return self.repository.get_report(filters)

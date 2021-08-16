from app.repository import DetailedReportRepository


class DetailedService:
    def __init__(self, repository: DetailedReportRepository):
        self.repository = repository

    def get_provider_report(self, filters: dict):
        return self.repository.provider_report(filters)

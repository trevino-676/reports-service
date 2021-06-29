from app import app
from app.models import SellsByItems
from app.repository import ReportRepository


class SellsByItemsRepository(ReportRepository):
    def get_report(self, filters: dict) -> list:
        try:
            report = SellsByItems.get_sells_by_items(filters)
            if len(report) == 0:
                return None
            return report
        except Exception as e:
            app.logger.error(e)
            return None

from abc import ABC, abstractmethod


class ReportRepository(ABC):
    @abstractmethod
    def get_report(self, filters: dict) -> list:
        pass

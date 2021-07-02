from app.repository.repository import ReportRepository
from app.repository.sells_by_client import Sells_By_Client_Repository
from app.repository.sell_by_item import SellsByItemsRepository
from app.repository.taxables_perceptions import TaxablesPerceptionsRepository

sells_clients_repo = Sells_By_Client_Repository()
sells_by_items_repo = SellsByItemsRepository()
taxables_perceptions_repo = TaxablesPerceptionsRepository()

from abc import ABC, abstractmethod


class CompanyFinancialsRepository(ABC):
    
    @abstractmethod
    def save(self, data_list: list) -> None:
        pass

    @abstractmethod
    def fetch(self, symbol: str, start_year: int = None, end_year: int = None):
        pass


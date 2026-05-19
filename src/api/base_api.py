from abc import ABC, abstractmethod
from typing import Any, Dict, List


class BaseAPI(ABC):
    """Абстрактный класс для API платформ с вакансиями."""

    @abstractmethod
    def _connect(self) -> None:
        """Выполняет подключение/проверку базового URL (заглушка)."""
        raise NotImplementedError

    @abstractmethod
    def get_vacancies(
        self, text: str, per_page: int = 20, page: int = 0
    ) -> List[Dict[str, Any]]:
        """Возвращает список вакансий в виде списка словарей (как дал API)."""
        raise NotImplementedError

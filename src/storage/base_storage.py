from abc import ABC, abstractmethod
from typing import List

from ..vacancies.vacancy import Vacancy


class BaseStorage(ABC):
    """Абстрактный класс для хранилищ вакансий."""

    @abstractmethod
    def add_vacancies(self, vacancies: List[Vacancy]) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_all(self) -> List[Vacancy]:
        raise NotImplementedError

    @abstractmethod
    def delete_vacancy(self, vacancy: Vacancy) -> None:
        raise NotImplementedError

from typing import Any, Dict, Optional


class Vacancy:
    """
    Модель вакансии.
    Использует __slots__ для экономии памяти.
    """

    __slots__ = ("title", "url", "salary_from", "salary_to", "description", "raw_id")

    def __init__(
        self,
        title: str,
        url: str,
        salary_from: Optional[float],
        salary_to: Optional[float],
        description: str,
        raw_id: Optional[str] = None,
    ) -> None:
        self.title = title
        self.url = url
        self.salary_from = self._validate_salary(salary_from)
        self.salary_to = self._validate_salary(salary_to)
        self.description = description
        self.raw_id = raw_id

    def _validate_salary(self, value: Optional[float]) -> float:
        """Приватная валидация зарплаты: если не указана — возвращаем 0.0"""
        if value is None:
            return 0.0
        try:
            return float(value)
        except (TypeError, ValueError):
            return 0.0

    @property
    def avg_salary(self) -> float:
        """Средняя зарплата для сравнения: если обе нули — 0.0"""
        if self.salary_from and self.salary_to:
            return (self.salary_from + self.salary_to) / 2.0
        return max(self.salary_from, self.salary_to, 0.0)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "title": self.title,
            "url": self.url,
            "salary_from": self.salary_from,
            "salary_to": self.salary_to,
            "description": self.description,
            "raw_id": self.raw_id,
        }

    @classmethod
    def from_hh_item(cls, item: Dict[str, Any]) -> "Vacancy":
        """Конвертация из формата hh.ru -> Vacancy."""
        title = item.get("name")
        url = item.get("alternate_url")
        raw_id = str(item.get("id"))
        salary = item.get("salary") or {}
        salary_from = salary.get("from")
        salary_to = salary.get("to")
        description = (
            item.get("snippet", {}).get("responsibility")
            or item.get("snippet", {}).get("requirement")
            or ""
        )
        return cls(title, url, salary_from, salary_to, description, raw_id)

    # магические методы сравнения по avg_salary
    def __lt__(self, other: "Vacancy") -> bool:
        return self.avg_salary < other.avg_salary

    def __gt__(self, other: "Vacancy") -> bool:
        return self.avg_salary > other.avg_salary

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Vacancy):
            return False
        return self.raw_id == other.raw_id or (self.url == other.url)

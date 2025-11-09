from typing import List

from src.vacancies.vacancy import Vacancy


def cast_items_to_vacancies(items: List[dict]) -> List[Vacancy]:
    """Преобразует список dict (API items) в список Vacancy объектов."""
    return [Vacancy.from_hh_item(it) for it in items]


def filter_by_keyword(vacancies: List[Vacancy], keyword: str) -> List[Vacancy]:
    """Фильтрует вакансии по ключевому слову в title или description."""
    kw = keyword.lower()
    return [
        v
        for v in vacancies
        if kw in (v.title or "").lower() or kw in (v.description or "").lower()
    ]


def get_top_by_salary(vacancies: List[Vacancy], top_n: int) -> List[Vacancy]:
    """Возвращает топ N вакансий по средней зарплате (avg_salary)."""
    return sorted(vacancies, key=lambda v: v.avg_salary, reverse=True)[:top_n]

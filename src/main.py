"""
Точка входа. Простой консольный интерфейс:
- делаем запрос к hh.ru
- сохраняем вакансии в JSON
- показываем топ N по зарплате
- фильтруем по ключевому слову
"""

from typing import List

from src.api.hh_api import HeadHunterAPI
from src.storage.json_storage import JSONStorage
from src.utils import (cast_items_to_vacancies, filter_by_keyword,
                       get_top_by_salary)
from src.vacancies.vacancy import Vacancy


def input_int(prompt: str, default: int) -> int:
    text = input(prompt).strip()
    if not text:
        return default
    try:
        return int(text)
    except ValueError:
        print("Неверное число, использую значение по умолчанию.")
        return default


def main() -> None:
    api = HeadHunterAPI()
    storage = JSONStorage()

    query = input("Введите поисковый запрос " "(например: Python developer): ").strip()
    if not query:
        print("Пустой запрос, завершаю.")
        return

    per_page = input_int(
        "Сколько вакансий скачать" " (per_page, max 20) [default 20]: ", 20
    )
    items = api.get_vacancies(query, per_page=per_page)
    vacancies = cast_items_to_vacancies(items)
    print(f"Получено вакансий: {len(vacancies)}")

    storage.add_vacancies(vacancies)
    print("Сохранено в файл.")

    n = input_int("Вывести топ N вакансий по зарплате. N = [default 5]: ", 5)
    all_vacs: List[Vacancy] = storage.get_all()
    top = get_top_by_salary(all_vacs, n)
    print("Топ вакансий:")
    for v in top:
        print(f"- {v.title} — avg salary: {v.avg_salary} — {v.url}")

    keyword = input(
        "Введите слово для фильтрации по описанию " "(Enter чтобы пропустить): "
    ).strip()
    if keyword:
        found = filter_by_keyword(all_vacs, keyword)
        print(f"Найдено {len(found)} вакансий по '{keyword}':")
        for v in found:
            print(f"- {v.title} ({v.url})")


if __name__ == "__main__":
    main()

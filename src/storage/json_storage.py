import json
from pathlib import Path
from typing import List

from src.storage.base_storage import BaseStorage
from src.vacancies.vacancy import Vacancy


class JSONStorage(BaseStorage):
    """
    Хранилище вакансий в JSON-файле.
    Не перезаписывает файл полностью — добавляет вакансии, избегая дублей.
    """

    def __init__(self, filename: str = "vacancies.json") -> None:
        self._filename = Path(filename)
        if not self._filename.exists():
            self._filename.write_text("[]", encoding="utf-8")

    def _load_raw(self) -> List[dict]:
        raw_text = self._filename.read_text(encoding="utf-8") or "[]"
        return json.loads(raw_text)

    def _save_raw(self, data: List[dict]) -> None:
        self._filename.write_text(
            json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8"
        )

    def add_vacancies(self, vacancies: List[Vacancy]) -> None:
        raw = self._load_raw()
        existing_ids = {item.get("raw_id") for item in raw if item.get("raw_id")}
        existing_urls = {item.get("url") for item in raw if item.get("url")}
        for v in vacancies:
            if (v.raw_id and v.raw_id in existing_ids) or (
                v.url and v.url in existing_urls
            ):
                continue
            raw.append(v.to_dict())
            if v.raw_id:
                existing_ids.add(v.raw_id)
            if v.url:
                existing_urls.add(v.url)
        self._save_raw(raw)

    def get_all(self) -> List[Vacancy]:
        raw = self._load_raw()
        # если формат словарей совпадает с Vacancy.to_dict,
        # можно просто создавать
        result = []
        for item in raw:
            # используем конструктор напрямую (имя ключей совпадает)
            result.append(
                Vacancy(
                    title=item.get("title", ""),
                    url=item.get("url", ""),
                    salary_from=item.get("salary_from"),
                    salary_to=item.get("salary_to"),
                    description=item.get("description", ""),
                    raw_id=item.get("raw_id"),
                )
            )
        return result

    def delete_vacancy(self, vacancy: Vacancy) -> None:
        raw = self._load_raw()
        filtered_raw = [
            item
            for item in raw
            if not (
                (vacancy.raw_id and item.get("raw_id") == vacancy.raw_id)
                or (item.get("url") == vacancy.url)
            )
        ]
        self._save_raw(filtered_raw)

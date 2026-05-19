from typing import Any, Dict, List

import requests

from .base_api import BaseAPI


class HeadHunterAPI(BaseAPI):
    """Реализация API-клиента для hh.ru"""

    BASE_URL = "https://api.hh.ru"

    def __init__(self) -> None:
        self._session = requests.Session()

    def _connect(self) -> None:
        url = f"{self.BASE_URL}/vacancies"
        resp = self._session.get(url, params={"per_page": 1})
        if resp.status_code != 200:
            raise ConnectionError(
                f"Не удалось подключиться к" f" {self.BASE_URL}: {resp.status_code}"
            )

    def get_vacancies(
        self, text: str, per_page: int = 20, page: int = 0
    ) -> List[Dict[str, Any]]:
        """Получает вакансии по ключевому слову text."""
        self._connect()
        url = f"{self.BASE_URL}/vacancies"
        params = {"text": text, "per_page": per_page, "page": page}
        resp = self._session.get(url, params=params)
        resp.raise_for_status()
        data = resp.json()
        # items — список вакансий
        return data.get("items", [])

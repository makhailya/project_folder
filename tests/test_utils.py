from src.utils import (cast_items_to_vacancies,
                       filter_by_keyword, get_top_by_salary)
from src.vacancies.vacancy import Vacancy


def test_cast_items_to_vacancies():
    items = [{"name": "Python Dev",
              "alternate_url": "url", "salary": {}, "snippet": {}}]
    result = cast_items_to_vacancies(items)
    assert len(result) == 1
    assert isinstance(result[0], Vacancy)


def test_filter_by_keyword_and_top():
    v1 = Vacancy("Junior Python", "u1", 100000, 150000, "опыт Python")
    v2 = Vacancy("Java Dev", "u2", 200000, 250000, "опыт Java")
    v3 = Vacancy("Go Dev", "u3", 50000, 100000, "описание")
    data = [v1, v2, v3]

    filtered = filter_by_keyword(data, "python")
    assert len(filtered) == 1
    assert filtered[0].title.startswith("Junior")

    top2 = get_top_by_salary(data, 2)
    assert top2[0].title == "Java Dev"
    assert len(top2) == 2

from src.vacancies.vacancy import Vacancy


def test_vacancy_validation_and_avg_salary():
    v1 = Vacancy("Dev", "url", None, None, "desc")
    v2 = Vacancy("Dev", "url", 100000, 200000, "desc")
    assert v1.avg_salary == 0.0
    assert v2.avg_salary == 150000.0


def test_vacancy_from_hh_item_parsing():
    item = {
        "id": "123",
        "name": "Python Developer",
        "alternate_url": "https://hh.ru/vacancy/123",
        "salary": {"from": 100000, "to": 150000},
        "snippet": {"requirement": "Опыт работы с Python"},
    }
    v = Vacancy.from_hh_item(item)
    assert v.title == "Python Developer"
    assert v.url.endswith("/123")
    assert v.salary_from == 100000
    assert v.salary_to == 150000
    assert "Python" in v.description


def test_vacancy_comparison_and_equality():
    v1 = Vacancy("A", "url1", 100, 200, "desc", "id1")
    v2 = Vacancy("B", "url2", 200, 300, "desc", "id2")
    v3 = Vacancy("A", "url1", 50, 60, "desc", "id1")
    assert v2 > v1
    assert v1 < v2
    assert v1 == v3

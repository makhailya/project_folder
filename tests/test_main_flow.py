from src.utils import filter_by_keyword, get_top_by_salary
from src.vacancies.vacancy import Vacancy


def test_end_to_end_flow(tmp_path):
    v1 = Vacancy("Python Dev", "url1", 100000, 150000, "описание")
    v2 = Vacancy("Java Dev", "url2", 200000, 220000, "описание Java")
    data = [v1, v2]

    top = get_top_by_salary(data, 1)
    assert top[0].title == "Java Dev"

    filt = filter_by_keyword(data, "python")
    assert filt[0].title == "Python Dev"

import json
from src.vacancies.vacancy import Vacancy
from src.storage.json_storage import JSONStorage


def test_add_get_delete_vacancy(tmp_path):
    file = tmp_path / "vac.json"
    store = JSONStorage(str(file))

    v1 = Vacancy("Dev1", "url1", 100000, 150000, "desc", "id1")
    v2 = Vacancy("Dev2", "url2", 120000, 160000, "desc", "id2")

    store.add_vacancies([v1, v2])
    all_vacs = store.get_all()
    assert len(all_vacs) == 2
    assert all_vacs[0].title == "Dev1"

    # повторное добавление не должно создавать дубликаты
    store.add_vacancies([v1])
    all_vacs2 = store.get_all()
    assert len(all_vacs2) == 2

    store.delete_vacancy(v1)
    remaining = store.get_all()
    assert len(remaining) == 1
    assert remaining[0].title == "Dev2"

    # файл должен быть корректным JSON
    raw = json.loads(file.read_text(encoding="utf-8"))
    assert isinstance(raw, list)

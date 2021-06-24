from app.utils import make_filters


def test_make_filters():
    expected = {"a": "1", "b": "2", "c": "3"}
    result = make_filters(a=1, b=2, c="3")
    assert expected == result


def test_make_none_filters():
    expected = {"a": "1", "b": "2"}
    result = make_filters(a=1, b=2, c=None)
    assert expected == result


def test_date_filters():
    expected = {"datos.Fecha": {"$gte": "2021-05-24", "$lte": "2021-06-25"}}
    result = make_filters(
        from_date="2021-05-24", to_date="2021-06-25", date_field="datos.Fecha"
    )
    assert expected == result


def test_date_and_extra_filters():
    expected = {
        "datos.Fecha": {"$gte": "2021-05-24", "$lte": "2021-06-25"},
        "a": "1",
        "b": "2",
    }
    result = make_filters(
        from_date="2021-05-24", to_date="2021-06-25", date_field="datos.Fecha", a=1, b=2
    )
    assert expected == result


def test_real_example_filters():
    expected = {
        "datos.Fecha": {"$gte": "2021-05-24", "$lte": "2021-06-25"},
        "datos.Rfc": "1",
    }
    result = make_filters(
        from_date="2021-05-24", to_date="2021-06-25", date_field="datos.Fecha", rfc=1
    )
    assert expected == result

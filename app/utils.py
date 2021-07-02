def make_filters(**kwargs) -> dict:
    filters = {}
    date_filters = {}
    if (
        "date_field" in kwargs
        and kwargs["from_date"] is not None
        and kwargs["to_date"] is not None
    ):
        date_filters[kwargs["date_field"]] = {
            "$gte": kwargs["from_date"],
            "$lte": kwargs["to_date"],
        }
        kwargs.pop("date_field")
        kwargs.pop("from_date")
        kwargs.pop("to_date")
    if "date_field" in kwargs:
        kwargs.pop("date_field")
    filters = {key: str(value) for key, value in kwargs.items() if value is not None}
    filters = __change_key_names(filters)
    return filters | date_filters


def __change_key_names(filters):
    new_filters = {}
    for key, value in filters.items():
        if key == "rfc":
            new_filters["Receptor.Rfc"] = value
        elif key == "amount":
            new_filters["datos.Total"] = value
        elif key == "company_rfc":
            new_filters["datos.Rfc"] = value
        # elif "status" in filters:
        #     filters["datos.Estado"] = filters["status"]
        #     filters.pop("status")

    return new_filters

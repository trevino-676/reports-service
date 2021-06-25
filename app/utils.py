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
    if "rfc" in filters:
        filters["datos.Rfc"] = filters["rfc"]
        filters.pop("rfc")
    elif "amount" in filters:
        filters["datos.Total"] = filters["amount"]
        filters.pop("amount")
    # elif "status" in filters:
    #     filters["datos.Estado"] = filters["status"]
    #     filters.pop("status")

    return filters

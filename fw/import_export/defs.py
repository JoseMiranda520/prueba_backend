def get_verbose_name_headers(fields, model) -> list:
    """
    :param fields: list
    :param model: django.db.models.Model
    :return: list
    """
    headers = []
    for field in fields:
        # noinspection Unresolved,PyProtectedMember
        model_fields = model._meta.get_fields()
        header = next((x.verbose_name.__str__().capitalize() for x in model_fields if x.name == field.column_name),
                      field.column_name)
        headers.append(header)

    return headers

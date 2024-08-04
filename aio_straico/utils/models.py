def _to_model_mapping_by_key(models, _key):
    if "chat" in models and "image" in models:  # v1
        mapping = {}
        for m in models["chat"]:
            key = m[_key]
            mapping[key] = m
        for m in models["image"]:
            key = m[_key]
            mapping[key] = m
        return mapping
    else:  # v0
        return dict([(m[_key], m) for m in models])


def to_model_mapping(models):
    return _to_model_mapping_by_key(models, "model")


def to_model_mapping_by_name(models):
    return _to_model_mapping_by_key(models, "name")


def __cheapest_model_v0(model_data):
    return sorted(model_data, key=lambda x: x["pricing"]["coins"])[0]


def __cheapest_model_v1(model_data):
    data = model_data["chat"]
    return sorted(data, key=lambda x: x["pricing"]["coins"])[0]


def cheapest_model(models):
    if "chat" in models and "image" in models:  # v1
        return __cheapest_model_v1(models)
    else:  # v0
        return __cheapest_model_v0(models)

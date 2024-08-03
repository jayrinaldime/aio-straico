def _to_model_mapping_by_key(models, _key):
    if "success" in models and models["success"]:
        if "data" in models:
            model_data = models["data"]
            if "chat" in model_data and "image" in model_data:  # v1
                # chat
                mapping = {}
                for m in model_data["chat"]:
                    key = m[_key]
                    mapping[key] = m
                for m in model_data["image"]:
                    key = m[_key]
                    mapping[key] = m
                return mapping
            else:  # v0
                return dict([(m[_key], m) for m in model_data])


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
    if "success" in models and models["success"]:
        if "data" in models:
            model_data = models["data"]
            if "chat" in model_data and "image" in model_data:  # v1
                return __cheapest_model_v1(model_data)
            else:  # v0
                return __cheapest_model_v0(model_data)

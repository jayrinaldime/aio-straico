class ModelCategory:
    pass


class ModelProvider:
    pass


class Model:
    def __init__(self, **properties):
        self.model = properties["model"]
        self.properties = properties

    def __getitem__(self, key):
        return self.properties.get(key)

    def __str__(self):
        return self.model

    def __repr__(self):
        return str(self.properties)


def __python_name(name):
    f = []
    for x in name:
        if x.isalnum():
            f.append(x)
        else:
            f.append("_")
    x = "".join(f)
    x = x.replace("__", "_").replace("__", "_")
    return x.strip("_").lower()


def __rename(model, name, value):
    name = name.split(":")[-1].strip()
    namespace = model.split("/")[0]
    return __python_name(namespace), __python_name(name), value


def __create_object(mapping):
    object = ModelCategory()
    for namespace, models in mapping.items():
        namespace_enum = ModelProvider()
        for name, value in models:
            setattr(namespace_enum, name, Model(**value))
        setattr(object, namespace, namespace_enum)
    return object


def __to_enum_object(models):
    f = [__rename(m["model"], m["name"], m) for m in models]
    mapping = {}
    for namespace, model, value in f:
        v = mapping.get(namespace, list())
        v.append((model, value))
        mapping[namespace] = v
    return __create_object(mapping)


def to_model_enum(models):
    if "chat" in models and "image" in models:  # v1
        return __to_enum_object(models["chat"]), __to_enum_object(models["image"])
    else:  # v0
        return __to_enum_object(models)

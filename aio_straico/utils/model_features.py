from .models_to_enum import _python_name, ModelProvider


def __to_enum(values):
    # remove duplicates
    values = list(set(values))
    python_values = list(map(_python_name, values))

    namespace_enum = ModelProvider()
    for name, value in zip(python_values, values):
        setattr(namespace_enum, name, value)

    return namespace_enum


def to_features(models):
    if "chat" in models and "image" in models:  # v1
        chat_models = models["chat"]
        capabilities = []
        features = []
        applications = []
        for model in chat_models:
            app = model["metadata"]["applications"]
            cap = model["metadata"]["capabilities"]
            feat = model["metadata"]["features"]
            capabilities.extend(cap)
            features.extend(feat)
            applications.extend(app)

        return __to_enum(capabilities), __to_enum(features), __to_enum(applications)
    else:  # v0
        return None, None, None


def filter_chat_models(models, capabilities=[], applications=[], features=[]):
    filtered_models = []
    for model in models:
        rejected = False
        for cap in capabilities:
            if cap not in model["metadata"]["capabilities"]:
                rejected = True
                break
        if rejected:
            continue

        for feat in features:
            if feat not in model["metadata"]["features"]:
                rejected = True
                break
        if rejected:
            continue

        for app in applications:
            if app not in model["metadata"]["applications"]:
                rejected = True
                break
        if rejected:
            continue
        else:
            filtered_models.append(model)
    return filtered_models

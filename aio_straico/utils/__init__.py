from .models import (
    cheapest_model,
    cheapest_models,
    to_model_mapping,
    to_model_mapping_by_name,
)
from .model_features import to_features, filter_chat_models

from .transcript_utils import (
    youtube_trasncript_to_objects,
    youtube_trasncript_to_plain_text,
)

from .models_to_enum import to_model_enum


from collections.abc import Iterable


def is_listable_not_string(obj):
    return not isinstance(obj, str) and isinstance(obj, Iterable)

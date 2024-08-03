from json import loads


def youtube_trasncript_to_plain_text(text):
    objects = youtube_trasncript_to_objects(text)
    return " ".join((obj["text"] for obj in objects))


def youtube_trasncript_to_objects(text):
    return loads(text)

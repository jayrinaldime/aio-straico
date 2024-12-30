from os import environ

TRACING_ENABLED = environ.get("STRAICO_TRACING_ENABLED", "False").lower() == "true"
if TRACING_ENABLED:
    from langfuse.decorators import observe
    from langfuse.decorators import langfuse_context as tracing_context

    def tracing_flush():
        tracing_context.flush()

else:

    def observe(*args, **kwargs):
        def d(func):
            return func

        return d

    class tracing_context:
        @classmethod
        def update_current_observation(cls, *args, **kwargs):
            return

    def tracing_flush():
        return None

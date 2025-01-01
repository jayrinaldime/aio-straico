from os import environ

TRACING_ENABLED = environ.get("STRAICO_TRACING_ENABLED", "False").lower() == "true"
if TRACING_ENABLED:
    from langfuse.decorators import observe
    from langfuse.decorators import langfuse_context as tracing_context

    def tracing_flush():
        tracing_context.flush()

else:
    from functools import wraps
    from inspect import iscoroutinefunction, isfunction

    def observe(*args, **kwargs):
        def decorator(func):
            return func

        if len(args) == 1 and (isfunction(args[0]) or iscoroutinefunction(args[0])):
            return args[0]
        return decorator

    class tracing_context:
        @classmethod
        def update_current_observation(cls, *args, **kwargs):
            return

    def tracing_flush():
        return None

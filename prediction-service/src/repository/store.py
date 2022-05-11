"""
This module stores all the loaded models.
Since modules in python are basically singletons and can be shared
we can use this to share the model with the processes that handle
the request.
"""
models = {
    'PYTHON3': None,
    'JAVA': None,
    'KOTLIN': None
}
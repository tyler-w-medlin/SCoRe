# ==============================================================
# This file is mostly for accessing and populating that database
# It should not be run for any other purpose. It's basically just
# a scratch file.
# ==============================================================

from main import db, Score

tests = [
    Score(
        raw_code = """
def foo():
    return bar
""",
        vector_coordinates = None,
        keywords = "foo bar"
    ),
    Score(
        raw_code = """"
def bar():
    return foo
""",
        vector_coordinates = None,
        keywords = "bar foo"
    )
]



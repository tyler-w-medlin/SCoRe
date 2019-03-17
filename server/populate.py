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


for item in tests:
    print(item)
    db.session.add(item)

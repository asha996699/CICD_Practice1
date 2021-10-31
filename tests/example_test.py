from CICDPractice2.example import foo, bar

def test_foo():
    num = 42
    assert foo(num) == 42

def test_bar():
    num = 10
    assert bar(num) == 20

code = """
def foo(a):
    b = a * 2
    return b

k = foo(2)
print(k)
"""

co = compile(code, '<string>', 'exec')
print(co.co_code)
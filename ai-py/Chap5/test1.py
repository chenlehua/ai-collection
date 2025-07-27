from functools import wraps


def my_decorator(func):
    # @wraps(func)
    def wrapper(*args, **kwargs):
        print("Before the function call")
        result = func(*args, **kwargs)
        print("After the function call")
        return result

    return wrapper


@my_decorator
def example_function():
    """This is an example function."""
    print("Inside the function")


example_function()

print(example_function.__name__)  # 输出: example_function
print(example_function.__doc__)  # 输出: This is an example function.

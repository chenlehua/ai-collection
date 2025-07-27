def repeat(n):
    print("repeat")
    def decorator(func):
        print("decorator")
        def wrapper(*args, **kwargs):
            print("wrapper")
            for i in range(n):
                func(*args, **kwargs)

        return wrapper

    return decorator


@repeat(3)
def a():
    print("a")


a()

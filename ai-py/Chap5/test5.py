def call_counter(threshold):
    def decorator(func):
        count = 0

        def wrapper(*args, **kwargs):
            nonlocal count
            count += 1

            if count > threshold:
                print(f"函数 {func.__name__} 调用次数已经达到阈值 {threshold} ，程序将正常退出")
                exit(0)
            func(*args, **kwargs)
            print(f"函数 {func.__name__} 已被调用 {count} 次")

        return wrapper

    return decorator


@call_counter(3)
def a():
    print("a")


a()
a()
a()
a()

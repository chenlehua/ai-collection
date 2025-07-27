from functools import partial


# 使用 lambda 表达式定义排序键
def custom_sort(data, key):
    return sorted(data, key=lambda x: x[key])


# 使用 functools.partial 创建自定义排序函数
sort_by_age = partial(custom_sort, key="age")
sort_by_score = partial(custom_sort, key="score")

students = [
    {"name": "Alice", "age": 25, "score": 85},
    {"name": "Bob", "age": 22, "score": 90},
    {"name": "Charlie", "age": 23, "score": 88},
]

# 根据年龄排序
sorted_by_age = sort_by_age(students)
print(sorted_by_age)

# 根据成绩排序
sorted_by_score = sort_by_score(students)
print(sorted_by_score)

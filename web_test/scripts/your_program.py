def continuous_accumulation():
    num = 0
    while True:
        num += 1
        yield num


# 使用示例
accumulator = continuous_accumulation()
for i in range(10):
    print(next(accumulator))
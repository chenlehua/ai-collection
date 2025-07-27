# 日志将详细记录每个线程进入和退出函数的时间、参数、返回值以及异常信息。
# 这对于调试并发问题和性能瓶颈非常有帮助。

# logging_util.py

import functools
import logging
import time
import threading

# 配置全局日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def detailed_logger(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        thread_id = threading.get_ident()
        start_time = time.time()
        logging.info(f"[Thread-{thread_id}] Entering {func.__name__} with args: {args}, kwargs: {kwargs}")
        try:
            result = func(*args, **kwargs)
            elapsed_time = (time.time() - start_time) * 1000  # 转换为毫秒
            logging.info(f"[Thread-{thread_id}] Exiting {func.__name__} with result: {result} (Elapsed: {elapsed_time:.2f}ms)")
            return result
        except Exception as e:
            logging.error(f"[Thread-{thread_id}] Exception in {func.__name__}: {e}", exc_info=True)
            raise
    return wrapper

# 2024-03-21 10:30:15,123 - INFO - [Thread-123] Entering some_function with args: (1, 2), kwargs: {}
# 2024-03-21 10:30:15,124 - INFO - [Thread-123] Exiting some_function with result: 3 (Elapsed: 1.23ms)

# service.py

from logging_util import detailed_logger

@detailed_logger
def process_transaction(transaction_id, amount):
    # 模拟处理交易的复杂逻辑
    if amount < 0:
        raise ValueError("交易金额不能为负数")
    # 假设这里有数据库操作、网络请求等
    time.sleep(0.5)  # 模拟耗时操作
    return {"transaction_id": transaction_id, "status": "success"}

# 在多线程环境下调用函数
import threading

def worker(tid):
    process_transaction(tid, amount=100)

threads = [threading.Thread(target=worker, args=(i,)) for i in range(5)]

for t in threads:
    t.start()

for t in threads:
    t.join()

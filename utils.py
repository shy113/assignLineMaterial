# 工具文件
import random
import string

# 生成随机字符串函数


def generate_random_string(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))

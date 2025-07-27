import re
import logging
from typing import List, Tuple, Optional

# 配置日志记录，确保在生产环境中可以追踪问题
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class DataParser:
    def __init__(self, pattern: str):
        """
        初始化 DataParser 类，接收正则表达式模式。
        :param pattern: 用于分隔数据的正则表达式模式
        """
        self.pattern = re.compile(pattern)
        logging.info(f"Initialized DataParser with pattern: {pattern}")

    def parse(self, data: str) -> Optional[List[str]]:
        """
        使用正则表达式分隔数据。
        :param data: 输入的字符串数据
        :return: 分隔后的字符串列表，如果匹配失败则返回 None
        """
        try:
            logging.debug(f"Parsing data: {data}")
            result = self.pattern.split(data)
            logging.debug(f"Split result: {result}")
            return result
        except re.error as e:
            logging.error(f"Regex error occurred: {e}")
            return None

    def extract_groups(self, data: str) -> Optional[Tuple]:
        """
        使用正则表达式提取数据中的分组信息。
        :param data: 输入的字符串数据
        :return: 提取的分组元组，如果匹配失败则返回 None
        """
        try:
            logging.debug(f"Extracting groups from data: {data}")
            match = self.pattern.match(data)
            if match:
                logging.debug(f"Match groups: {match.groups()}")
                return match.groups()
            else:
                logging.warning(f"No match found for data: {data}")
                return None
        except re.error as e:
            logging.error(f"Regex error occurred: {e}")
            return None

# 正则表达式模式示例：分隔逗号、空格、分号等符号
# 例如： 'value1, value2; value3 value4'
pattern = r'[,\s;]+'

# 初始化 DataParser 类
parser = DataParser(pattern)

# 示例数据
data = "value1, value2; value3 value4"

# 分隔数据
split_result = parser.parse(data)
if split_result:
    logging.info(f"Split result: {split_result}")

# 提取分组示例（假设我们有一个带分组的正则表达式）
group_pattern = r'(\w+),\s*(\w+);?\s*(\w+)?'
group_parser = DataParser(group_pattern)

# 提取分组
group_data = "value1, value2; value3"
group_result = group_parser.extract_groups(group_data)
if group_result:
    logging.info(f"Extracted groups: {group_result}")

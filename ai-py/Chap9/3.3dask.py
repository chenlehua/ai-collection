import dask.dataframe as dd
import logging
from dask.distributed import Client

# 配置日志记录，确保在生产环境中可以追踪问题
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class DaskPivotTable:
    def __init__(self, client_address: str = None):
        """
        初始化 DaskPivotTable 类，连接 Dask 分布式集群。
        :param client_address: Dask 分布式集群的地址，如果为 None 则使用本地集群
        """
        if client_address:
            self.client = Client(client_address)
            logging.info(f"Connected to Dask distributed cluster at {client_address}")
        else:
            self.client = Client()
            logging.info("Initialized local Dask client")

    def load_data(self, file_path: str, file_type: str = 'csv', **kwargs) -> dd.DataFrame:
        """
        加载大规模数据集，支持 CSV 和 Parquet 格式。
        :param file_path: 数据文件路径
        :param file_type: 文件类型，支持 'csv' 和 'parquet'
        :param kwargs: 传递给 dask.dataframe 读取函数的其他参数
        :return: Dask DataFrame
        """
        logging.info(f"Loading data from {file_path} as {file_type}")
        if file_type == 'csv':
            df = dd.read_csv(file_path, **kwargs)
        elif file_type == 'parquet':
            df = dd.read_parquet(file_path, **kwargs)
        else:
            raise ValueError(f"Unsupported file type: {file_type}")
        logging.info(f"Data loaded with {df.npartitions} partitions")
        return df

    def pivot_table(self, df: dd.DataFrame, index: str, columns: str, values: str, aggfunc: str = 'mean') -> dd.DataFrame:
        """
        使用 Dask 进行数据透视操作。
        :param df: Dask DataFrame
        :param index: 透视表的行索引
        :param columns: 透视表的列索引
        :param values: 透视表中的值
        :param aggfunc: 聚合函数，默认为 'mean'
        :return: 透视后的 Dask DataFrame
        """
        logging.info(f"Performing pivot table with index={index}, columns={columns}, values={values}, aggfunc={aggfunc}")

        try:
            # 首先计算唯一的类别值
            unique_columns = df[columns].unique().compute()
            unique_index = df[index].unique().compute()

            # 将 columns 和 index 列转换为具有已知类别的分类类型
            df[columns] = df[columns].astype('category').cat.set_categories(unique_columns)
            df[index] = df[index].astype('category').cat.set_categories(unique_index)

            pivot_df = df.pivot_table(index=index, columns=columns, values=values, aggfunc=aggfunc)
            logging.info("Pivot table operation completed")
            return pivot_df
        except Exception as e:
            logging.error(f"Error during pivot table operation: {e}")
            raise

    def compute_result(self, df: dd.DataFrame) -> dd.DataFrame:
        """
        触发 Dask 计算并返回结果。
        :param df: Dask DataFrame
        :return: 计算后的 Pandas DataFrame
        """
        logging.info("Computing the result")
        try:
            result = df.compute()
            logging.info("Computation completed")
            return result
        except Exception as e:
            logging.error(f"Error during computation: {e}")
            raise

# 示例使用
if __name__ == "__main__":
    # 初始化 DaskPivotTable 类，使用本地 Dask 集群
    dask_pivot = DaskPivotTable()

    # 加载大规模 CSV 数据集
    file_path = 'large_dataset.csv'
    df = dask_pivot.load_data(file_path, file_type='csv')

    # 执行数据透视操作
    pivot_df = dask_pivot.pivot_table(df, index='category', columns='region', values='sales', aggfunc='sum')

    # 计算并获取结果
    result = dask_pivot.compute_result(pivot_df)

    # 输出结果
    print(result)

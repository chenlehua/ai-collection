# 📦 Offline模块

离线索引构建模块，负责文档预处理和倒排索引构建。

## 📁 文件说明

### `offline_index.py`
- **功能**: 倒排索引构建和离线处理
- **职责**:
  - 文档预处理和分词
  - TF-IDF计算
  - 倒排索引构建
  - 索引持久化
  - 文档存储管理

## 🔧 核心功能

### 文本预处理
- 中文分词（jieba）
- 停用词过滤
- 词频统计

### 倒排索引
- 词项到文档的映射
- TF-IDF分数计算
- 文档向量化

### 搜索功能
- 文档召回
- 相似度计算
- 结果排序

## 🚀 使用方式

```python
# 导入模块
from offline.offline_index import InvertedIndex

# 初始化索引
index = InvertedIndex()

# 添加文档
index.add_document("doc1", "文档内容")

# 搜索
results = index.search("查询词", top_k=10)
```

## 📊 索引统计

```python
# 获取索引统计
stats = index.get_index_stats()
print(f"文档数: {stats['total_documents']}")
print(f"词项数: {stats['total_terms']}")
``` 
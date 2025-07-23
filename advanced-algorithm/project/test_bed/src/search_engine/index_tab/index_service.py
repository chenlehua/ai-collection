#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
倒排索引服务模块
提供标准的索引写入和查询接口
"""

import json
import os
from typing import List, Dict, Tuple, Optional, Any
from abc import ABC, abstractmethod
from .offline_index import InvertedIndex

class IndexServiceInterface(ABC):
    """倒排索引服务接口"""
    
    @abstractmethod
    def add_document(self, doc_id: str, content: str) -> bool:
        """添加文档到索引"""
        pass
    
    @abstractmethod
    def search(self, query: str, top_k: int = 20) -> List[Tuple[str, float, str]]:
        """搜索文档"""
        pass
    
    @abstractmethod
    def get_document(self, doc_id: str) -> Optional[str]:
        """获取文档内容"""
        pass
    
    @abstractmethod
    def get_stats(self) -> Dict[str, Any]:
        """获取索引统计信息"""
        pass
    
    @abstractmethod
    def save_index(self, filepath: str) -> bool:
        """保存索引到文件"""
        pass
    
    @abstractmethod
    def load_index(self, filepath: str) -> bool:
        """从文件加载索引"""
        pass
    
    @abstractmethod
    def clear_index(self) -> bool:
        """清空索引"""
        pass
    
    @abstractmethod
    def get_all_documents(self) -> Dict[str, str]:
        """获取所有文档"""
        pass

class InvertedIndexService(IndexServiceInterface):
    """倒排索引服务实现"""
    
    def __init__(self, index_file: str = "models/index_data.json"):
        """
        初始化倒排索引服务
        
        Args:
            index_file: 索引文件路径
        """
        self.index = InvertedIndex()
        self.index_file = index_file
        self._load_or_create_index()
    
    def _load_or_create_index(self):
        """加载或创建索引"""
        try:
            if os.path.exists(self.index_file):
                self.load_index(self.index_file)
                print(f"从文件加载索引成功: {self.index_file}")
            else:
                print(f"索引文件不存在，将创建新索引: {self.index_file}")
                # 创建示例文档
                from .offline_index import create_sample_documents
                documents = create_sample_documents()
                for doc_id, content in documents.items():
                    self.add_document(doc_id, content)
                print("创建示例索引成功")
        except Exception as e:
            print(f"加载索引失败: {e}")
    
    def add_document(self, doc_id: str, content: str) -> bool:
        """
        添加文档到索引
        
        Args:
            doc_id: 文档ID
            content: 文档内容
            
        Returns:
            bool: 是否添加成功
        """
        try:
            self.index.add_document(doc_id, content)
            return True
        except Exception as e:
            print(f"添加文档失败: {e}")
            return False
    
    def delete_document(self, doc_id: str) -> bool:
        """
        删除文档从索引
        
        Args:
            doc_id: 文档ID
            
        Returns:
            bool: 是否删除成功
        """
        try:
            success = self.index.delete_document(doc_id)
            if success:
                print(f"文档 '{doc_id}' 删除成功")
            else:
                print(f"文档 '{doc_id}' 不存在")
            return success
        except Exception as e:
            print(f"删除文档失败: {e}")
            return False
    
    def search(self, query: str, top_k: int = 20) -> List[Tuple[str, float, str]]:
        """
        搜索文档
        
        Args:
            query: 查询字符串
            top_k: 返回结果数量
            
        Returns:
            List[Tuple[str, float, str]]: 搜索结果列表 (doc_id, score, summary)
        """
        try:
            if not query.strip():
                return []
            return self.index.search(query.strip(), top_k=top_k)
        except Exception as e:
            print(f"搜索失败: {e}")
            return []
    
    def get_document(self, doc_id: str) -> Optional[str]:
        """
        获取文档内容
        
        Args:
            doc_id: 文档ID
            
        Returns:
            Optional[str]: 文档内容，如果不存在返回None
        """
        try:
            return self.index.get_document(doc_id)
        except Exception as e:
            print(f"获取文档失败: {e}")
            return None
    
    def get_stats(self) -> Dict[str, Any]:
        """
        获取索引统计信息
        
        Returns:
            Dict[str, Any]: 统计信息
        """
        try:
            return self.index.get_index_stats()
        except Exception as e:
            print(f"获取统计信息失败: {e}")
            return {
                'total_documents': 0,
                'total_terms': 0,
                'average_doc_length': 0
            }
    
    def save_index(self, filepath: Optional[str] = None) -> bool:
        """
        保存索引到文件
        
        Args:
            filepath: 文件路径，如果为None使用默认路径
            
        Returns:
            bool: 是否保存成功
        """
        try:
            save_path = filepath or self.index_file
            # 确保目录存在
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            self.index.save_to_file(save_path)
            return True
        except Exception as e:
            print(f"保存索引失败: {e}")
            return False
    
    def load_index(self, filepath: str) -> bool:
        """
        从文件加载索引
        
        Args:
            filepath: 文件路径
            
        Returns:
            bool: 是否加载成功
        """
        try:
            self.index.load_from_file(filepath)
            return True
        except Exception as e:
            print(f"加载索引失败: {e}")
            return False
    
    def clear_index(self) -> bool:
        """
        清空索引
        
        Returns:
            bool: 是否清空成功
        """
        try:
            self.index = InvertedIndex()
            return True
        except Exception as e:
            print(f"清空索引失败: {e}")
            return False
    
    def batch_add_documents(self, documents: Dict[str, str]) -> int:
        """
        批量添加文档
        
        Args:
            documents: 文档字典 {doc_id: content}
            
        Returns:
            int: 成功添加的文档数量
        """
        success_count = 0
        for doc_id, content in documents.items():
            if self.add_document(doc_id, content):
                success_count += 1
        return success_count
    
    def search_doc_ids(self, query: str, top_k: int = 20) -> List[str]:
        """
        搜索并只返回文档ID列表
        
        Args:
            query: 查询字符串
            top_k: 返回结果数量
            
        Returns:
            List[str]: 文档ID列表
        """
        results = self.search(query, top_k)
        return [doc_id for doc_id, score, summary in results]
    
    def get_document_count(self) -> int:
        """
        获取文档总数
        
        Returns:
            int: 文档总数
        """
        stats = self.get_stats()
        return stats.get('total_documents', 0)
    
    def get_all_documents(self) -> Dict[str, str]:
        """
        获取所有文档
        
        Returns:
            Dict[str, str]: 所有文档的字典 {doc_id: content}
        """
        try:
            return self.index.get_all_documents()
        except Exception as e:
            print(f"获取所有文档失败: {e}")
            return {}

# 全局索引服务实例
_index_service = None

def get_index_service() -> InvertedIndexService:
    """
    获取全局索引服务实例（单例模式）
    
    Returns:
        InvertedIndexService: 索引服务实例
    """
    global _index_service
    if _index_service is None:
        _index_service = InvertedIndexService()
    return _index_service

def reset_index_service():
    """重置全局索引服务实例"""
    global _index_service
    _index_service = None 
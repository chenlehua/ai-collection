# Week3 - 倒排索引检索系统

一个完整的检索系统示例，包含倒排索引、CTR模型训练、Web界面等核心功能。

## 🚀 快速启动

```bash
# 启动系统
python start_system.py
```

## 📁 项目结构

```
week3/
├── README.md              # 项目说明
├── start_system.py        # 启动脚本
├── requirements.txt       # 依赖包
├── online/               # 在线服务模块
│   ├── search_engine.py  # 搜索引擎实现
│   ├── ctr_model.py      # CTR模型
│   └── ctr_collector.py  # CTR数据收集
├── offline/              # 离线模块
│   └── offline_index.py  # 索引构建
├── ui/                   # 用户界面
│   └── ui_interface.py   # Gradio界面
├── test/                 # 测试模块
│   └── test_units.py     # 单元测试
├── tools/                # 工具模块
│   ├── reset_system.py   # 系统重置
│   └── demo_data.py      # 演示数据生成
├── docs/                 # 文档
│   └── *.md             # 详细文档
├── models/               # 模型和数据
│   ├── ctr_model.pkl     # CTR模型
│   └── index_data.json   # 索引数据
└── data/                 # 数据目录
    └── ctr_data*.json    # CTR数据
```

## 🎯 核心功能

- **倒排索引**: 基于TF-IDF的文档检索
- **CTR模型**: 点击率预测和排序优化
- **Web界面**: 交互式搜索和结果展示
- **数据收集**: 自动收集用户行为数据
- **模型训练**: 基于收集数据的模型训练

## 📖 详细文档

- [在线模块文档](docs/online/README.md)
- [离线模块文档](docs/offline/README.md)
- [UI模块文档](docs/ui/README.md)
- [测试模块文档](docs/test/README.md)
- [工具模块文档](docs/tools/README.md)

## 🔧 系统要求

- Python 3.8+
- 依赖包见 [requirements.txt](requirements.txt) 
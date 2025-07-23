#!/bin/bash

# MLOps搜索引擎测试床 - 快速启动脚本
# 功能：一键启动搜索引擎系统，包含完整的预检查和用户指导

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 打印横幅
print_banner() {
    echo -e "${BLUE}===============================================${NC}"
    echo -e "${BLUE}🚀 MLOps搜索引擎测试床 - 快速启动脚本${NC}"
    echo -e "${BLUE}===============================================${NC}"
    echo -e "${GREEN}📖 功能: 一键启动完整的搜索引擎系统${NC}"
    echo -e "${GREEN}🔧 包含: 依赖检查、环境设置、系统启动${NC}"
    echo -e "${GREEN}🌐 访问: http://localhost:7861${NC}"
    echo -e "${GREEN}🛑 停止: 按 Ctrl+C 或关闭终端${NC}"
    echo -e "${BLUE}===============================================${NC}"
}

# 检查系统要求
check_system_requirements() {
    echo -e "\n${YELLOW}🔍 步骤1: 检查系统要求${NC}"
    echo "----------------------------------------"
    
    # 检查操作系统
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        echo -e "${GREEN}✅ 操作系统: Linux${NC}"
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        echo -e "${GREEN}✅ 操作系统: macOS${NC}"
    else
        echo -e "${RED}❌ 不支持的操作系统: $OSTYPE${NC}"
        echo -e "${YELLOW}💡 建议: 使用 Linux 或 macOS${NC}"
        return 1
    fi
    
    # 检查Python
    if ! command -v python &> /dev/null; then
        if ! command -v python3 &> /dev/null; then
            echo -e "${RED}❌ Python未安装或不在PATH中${NC}"
            echo -e "${YELLOW}💡 建议: 安装 Python 3.8 或更高版本${NC}"
            return 1
        else
            echo -e "${GREEN}✅ Python: $(python3 --version)${NC}"
            alias python=python3
        fi
    else
        echo -e "${GREEN}✅ Python: $(python --version)${NC}"
    fi
    
    # 检查pip
    if ! command -v pip &> /dev/null; then
        echo -e "${YELLOW}⚠️  pip未找到，尝试使用pip3${NC}"
        if ! command -v pip3 &> /dev/null; then
            echo -e "${RED}❌ pip未安装${NC}"
            echo -e "${YELLOW}💡 建议: 安装 pip${NC}"
            return 1
        else
            alias pip=pip3
        fi
    fi
    echo -e "${GREEN}✅ pip: $(pip --version | cut -d' ' -f2)${NC}"
    
    return 0
}

# 检查项目结构
check_project_structure() {
    echo -e "\n${YELLOW}📁 步骤2: 检查项目结构${NC}"
    echo "----------------------------------------"
    
    # 检查是否在正确的目录
    if [ ! -f "start_system.py" ]; then
        echo -e "${RED}❌ 请在项目根目录运行此脚本${NC}"
        echo -e "${YELLOW}💡 建议: 进入包含 start_system.py 的目录${NC}"
        return 1
    fi
    echo -e "${GREEN}✅ 项目根目录: $(pwd)${NC}"
    
    # 检查关键文件
    required_files=("requirements.txt" "src/search_engine/portal.py" "src/search_engine/data_service.py")
    for file in "${required_files[@]}"; do
        if [ ! -f "$file" ]; then
            echo -e "${RED}❌ 缺少文件: $file${NC}"
            return 1
        fi
    done
    echo -e "${GREEN}✅ 项目文件完整${NC}"
    
    # 检查关键目录
    required_dirs=("src" "models" "data" "tools")
    for dir in "${required_dirs[@]}"; do
        if [ ! -d "$dir" ]; then
            echo -e "${YELLOW}⚠️  创建目录: $dir${NC}"
            mkdir -p "$dir"
        fi
    done
    echo -e "${GREEN}✅ 项目目录结构完整${NC}"
    
    return 0
}

# 检查和安装依赖
check_dependencies() {
    echo -e "\n${YELLOW}📦 步骤3: 检查Python依赖${NC}"
    echo "----------------------------------------"
    
    # 检查requirements.txt
    if [ ! -f "requirements.txt" ]; then
        echo -e "${RED}❌ 未找到 requirements.txt${NC}"
        return 1
    fi
    
    # 检查关键依赖
    echo -e "${BLUE}🔍 检查关键依赖...${NC}"
    python -c "
import sys
required_packages = ['gradio', 'pandas', 'numpy', 'sklearn', 'jieba']
missing = []
for package in required_packages:
    try:
        __import__(package)
        print(f'✅ {package}')
    except ImportError:
        missing.append(package)
        print(f'❌ {package}')

if missing:
    print(f'\\n缺少 {len(missing)} 个依赖包')
    sys.exit(1)
else:
    print('\\n✅ 所有关键依赖已安装')
    sys.exit(0)
"
    
    if [ $? -ne 0 ]; then
        echo -e "\n${YELLOW}🔧 正在安装依赖...${NC}"
        echo -e "${BLUE}⏳ 这可能需要几分钟时间，请耐心等待...${NC}"
        
        if pip install -r requirements.txt; then
            echo -e "${GREEN}✅ 依赖安装完成${NC}"
        else
            echo -e "${RED}❌ 依赖安装失败${NC}"
            echo -e "${YELLOW}💡 建议: 检查网络连接或使用代理${NC}"
            return 1
        fi
    fi
    
    return 0
}

# 清理端口占用
cleanup_ports() {
    echo -e "\n${YELLOW}🔧 步骤4: 清理端口占用${NC}"
    echo "----------------------------------------"
    
    ports=(7860 7861 7862 7863 7864 7865)
    for port in "${ports[@]}"; do
        if lsof -i:$port &> /dev/null; then
            echo -e "${BLUE}🔄 清理端口 $port${NC}"
            lsof -ti:$port | xargs kill -9 2>/dev/null || true
        else
            echo -e "${GREEN}✅ 端口 $port 未被占用${NC}"
        fi
    done
    
    # 等待端口释放
    sleep 2
    echo -e "${GREEN}✅ 端口清理完成${NC}"
}

# 启动系统
start_system() {
    echo -e "\n${YELLOW}🚀 步骤5: 启动系统${NC}"
    echo "----------------------------------------"
    
    echo -e "${BLUE}🌐 正在启动MLOps系统...${NC}"
    echo -e "${GREEN}⏳ 系统启动中，请稍等...${NC}"
    echo -e "${GREEN}💡 启动完成后会显示访问地址${NC}"
    echo -e "${YELLOW}🛑 按 Ctrl+C 可以停止系统${NC}"
    
    # 启动系统
    if python start_system.py; then
        echo -e "\n${GREEN}✅ 系统启动完成！${NC}"
    else
        echo -e "\n${RED}❌ 系统启动失败${NC}"
        echo -e "${YELLOW}💡 建议: 检查错误信息并重新运行${NC}"
        return 1
    fi
}

# 主函数
main() {
    print_banner
    
    # 执行检查和启动流程
    if check_system_requirements && \
       check_project_structure && \
       check_dependencies && \
       cleanup_ports; then
        
        start_system
        
        echo -e "\n${GREEN}🎉 感谢使用MLOps搜索引擎测试床！${NC}"
        echo -e "${BLUE}📖 更多信息请查看: README.md${NC}"
        echo -e "${BLUE}🐛 问题反馈: 请提交GitHub Issue${NC}"
        
    else
        echo -e "\n${RED}❌ 启动过程中发生错误${NC}"
        echo -e "${YELLOW}💡 建议: 检查上述错误信息并重新运行${NC}"
        exit 1
    fi
}

# 错误处理
set -e
trap 'echo -e "\n${RED}🛑 脚本执行被中断${NC}"; exit 1' INT

# 运行主函数
main "$@" 
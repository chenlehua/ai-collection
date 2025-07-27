1. 首先需要安装依赖
pip install prometheus-fastapi-instrumentator

2. 修改 knowledge_server.py 添加监控代码

3. 创建 prometheus.yml 配置文件

4. 修改 docker-compose.yml 文件，添加 prometheus 服务

5. 修改 Dockerfile 文件


6. 构建镜像
docker-compose build

7. 运行
docker-compose up -d

8. 访问面板
访问监控面板:
Prometheus UI: http://localhost:9090
FastAPI metrics: http://localhost:8000/metrics

## CI/CD 流程

### 配置说明

1. 在项目根目录创建 `.github/workflows` 目录
2. 添加以下工作流配置文件：
   - `test.yml`: 代码测试和质量检查
   - `build.yml`: Docker镜像构建
   - `deploy.yml`: 自动部署

这三个工作流文件的主要功能:
test.yml:
在任意分支推送或PR时触发
设置Python环境
安装依赖
运行单元测试
进行代码质量检查
build.yml:
在main分支推送或打tag时触发
登录Docker Hub
构建并推送Docker镜像
deploy.yml:
在build工作流成功完成后触发
配置SSH密钥
连接到部署服务器
拉取最新镜像并重启服务

### 工作流触发条件
- 测试工作流：推送到任意分支或创建Pull Request时触发
- 构建工作流：推送到main分支或创建新的tag时触发
- 部署工作流：构建工作流成功后自动触发

### 环境变量配置
在GitHub仓库的Settings -> Secrets中配置以下变量：
- `DOCKER_USERNAME`: Docker Hub用户名
- `DOCKER_PASSWORD`: Docker Hub密码
- `SSH_PRIVATE_KEY`: 部署服务器SSH私钥
- `SERVER_HOST`: 部署服务器地址
- `SERVER_USER`: 部署服务器用户名

### 本地开发流程
1. 创建新分支进行开发
2. 提交代码并推送到GitHub
3. 创建Pull Request
4. 等待CI检查通过
5. 合并到main分支后自动部署
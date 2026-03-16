# Engine Logs 分析工具

基于 Python Flask 的日志文件分析网页应用，自动分析 engine.log 文件并生成在线测试用例执行报告。

## 功能特性

### 自动分析
- 支持启动时自动读取本地日志文件（默认路径：`~/.config/Z-Factory/logs/YYYY-MM-DD/engine_logs/engine.log`）
- 支持通过API接口上传日志文件进行实时分析
- 从 `log_service.py` 的 `Log.Info : 测试用例XXX开始` 到 `测试用例XXX结束`
- 自动识别 ERROR 日志中的异常信息

### 局域网访问
- 自动获取本机局域网IP地址
- 支持同一WiFi下的其他设备访问
- 每次生成带时间戳的唯一报告链接（格式：`http://x.x.x.x:5000/report/YYYYMMDDHHmmss`）

### 在线文件上传
- 支持通过POST接口上传engine.log文件
- 自动分析上传的日志文件
- 生成Word报告并发送邮件通知
- 返回带时间戳的报告访问链接

### 组件信息提取
- 组件模块
- 组件中文名
- 组件分类
- 组件方法名
- 组件插件包中文名
- 组件唯一标识

### 运行结果显示
- **正常执行**: 显示"执行正常"状态
- **异常报错**: 
  - 显示"异常报错"状态
  - 从 ERROR 或 Exception 关键词开始提取错误信息
  - 简略显示：最多 150 字符
  - 点击可展开查看完整错误信息（最多 250 字符）
  - 再次点击可折叠

### 日志上下文查看
- 点击"查看日志上下文"链接打开模态框
- 显示错误行前后各 500 行（共 1000 行）日志上下文
- 错误行自动滚动到视图中央位置并高亮显示
- 支持上下滚动条查看完整的日志上下文
- 日志字体大小：15px
- 行号宽度：2px（紧凑显示）

## 安装步骤

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

requirements.txt 已自动适配不同 Python 版本（3.7 使用 python-docx 0.8.11，3.8+ 使用 python-docx 1.2.0）。

### 2. 配置邮件服务（可选）

如需自动发送报告邮件，复制配置文件并填写信息：

```bash
cp config.yaml.example config.yaml
```

编辑 `config.yaml` 文件，参考以下常用邮件服务器配置：

- **Gmail**: smtp.gmail.com:587 (TLS) 或 465 (SSL)，需应用专用密码
- **QQ邮箱**: smtp.qq.com:587 (TLS) 或 465 (SSL)，需授权码
- **163邮箱**: smtp.163.com:465 (SSL)，需授权码
- **阿里企业邮箱**: smtp.qiye.aliyun.com:465 (SSL)

### 3. 放置日志文件

将 `engine.log` 文件放置到 `static/` 目录下：
```bash
cp /path/to/engine.log static/
```

### 3. 运行应用

```bash
python3 app.py
```

应用启动后会：
1. 自动读取本地日志文件并生成Word报告
2. 如果配置了邮件信息，自动发送邮件通知
3. 显示局域网访问地址（如：`http://192.168.1.100:5000/analysis`）
4. 显示带时间戳的报告链接（如：`http://192.168.1.100:5000/report/20260316185030`）

## 使用方法

### 方式一：访问Web界面

1. 启动应用后，在浏览器访问显示的局域网地址
2. 同一WiFi下的其他设备也可以通过该地址访问
3. 浏览测试用例列表，查看执行状态和组件信息
4. 错误信息显示：
   - 默认显示简略错误（150字符）
   - 点击可展开查看完整内容（250字符）
   - 再次点击可折叠
5. 点击"查看日志上下文"链接查看错误行前后各500行的日志

### 方式二：通过API上传日志文件

使用curl命令上传日志文件：

```bash
curl -X POST -F "file=@/path/to/engine.log" http://192.168.1.100:5000/upload
```

返回示例：
```json
{
  "success": true,
  "report_url": "http://192.168.1.100:5000/report/20260316185030",
  "timestamp": "20260316185030",
  "total": 10,
  "errors": 2
}
```

也可以使用Python脚本上传：

```python
import requests

url = "http://192.168.1.100:5000/upload"
files = {'file': open('engine.log', 'rb')}
response = requests.post(url, files=files)
print(response.json())
```

## 界面说明

### 统计卡片
- 总测试用例、正常用例、异常用例、总组件数

### 表格列说明
| 列名 | 说明 |
|-----|------|
| 测试用例ID | 测试用例编号 |
| 组件模块 | 组件所属模块 |
| 组件中文名 | 组件的中文名称 |
| 组件分类 | 组件的分类标签 |
| 组件方法名 | 组件的方法名称 |
| 组件插件包中文名 | 组件插件包的中文名称 |
| 组件唯一标识 | 组件的唯一标识符 |
| 运行结果 | 测试用例执行状态和错误信息 |

### 运行结果状态
- **执行正常**: 测试用例成功执行
- **异常报错**: 显示ERROR异常信息，可点击查看完整错误和日志上下文

## API 接口

### GET 接口

- `GET /analysis` - 查看分析页面
- `GET /report/<timestamp>` - 查看指定时间戳的报告页面
- `GET /analyze/default` - 获取默认日志文件的分析结果（JSON）
- `GET /engine.log` - 读取日志文件
- `GET /log/context/<error_line>` - 获取错误行的日志上下文（前后各500行）

### POST 接口

- `POST /upload` - 上传engine.log文件并生成分析报告
  - 参数：`file` (multipart/form-data)
  - 返回：
    ```json
    {
      "success": true,
      "report_url": "http://x.x.x.x:5000/report/YYYYMMDDHHmmss",
      "timestamp": "YYYYMMDDHHmmss",
      "total": 10,
      "errors": 2
    }
    ```

## 更新日志

### v2.0 (2026-03-16)

**新增功能：**
1. 局域网访问支持
   - 自动获取本机局域网IP地址
   - Flask监听地址改为0.0.0.0，支持局域网内其他设备访问
   - 启动时显示局域网访问地址

2. 带时间戳的报告链接
   - 每次生成报告都有唯一的时间戳标识
   - 报告URL格式：`http://x.x.x.x:5000/report/YYYYMMDDHHmmss`
   - 新增 `/report/<timestamp>` 路由

3. 在线文件上传接口
   - 新增 `POST /upload` 接口
   - 支持上传engine.log文件进行实时分析
   - 自动生成Word报告并发送邮件
   - 返回带时间戳的报告访问链接

**改进：**
- 日志文件路径改为读取本地配置目录：`~/.config/Z-Factory/logs/YYYY-MM-DD/engine_logs/engine.log`
- 邮件中的报告链接使用局域网IP和时间戳
- 优化报告生成逻辑，支持多种触发方式（启动时/API上传）

### v1.0
- 初始版本
- 基础日志分析功能
- Word报告生成
- 邮件发送功能

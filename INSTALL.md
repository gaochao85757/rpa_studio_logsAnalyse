# 安装说明

## 前置要求
- Python 3.7 或更高版本

## 安装步骤

### 1. 克隆或下载项目

```bash
git clone https://github.com/gaochao85757/rpa_studio_logsAnalyse.git
cd rpa_studio_logsAnalyse
```

### 2. 创建虚拟环境（推荐）

```bash
python3 -m venv .venv

# 激活虚拟环境
source .venv/bin/activate  # Linux/Mac
# 或
.venv\Scripts\activate     # Windows
```

### 3. 安装依赖

**如果不使用虚拟环境：**
```bash
pip3 install -r requirements.txt
```

**如果使用虚拟环境：**
```bash
pip install -r requirements.txt
```

### 4. 配置邮件服务

复制配置文件示例并编辑：

```bash
cp config.yaml.example config.yaml
```

编辑 `config.yaml` 文件，填写您的邮件服务器信息：

```yaml
mail:
  server: smtp.gmail.com  # SMTP 服务器地址
  port: 587              # SMTP 端口
  use_tls: true           # 是否使用 TLS
  from_email: your-email@gmail.com  # 发件人邮箱
  password: your-password  # 邮箱密码或授权码

recipients:
  - recipient1@example.com
  - recipient2@example.com

report:
  title: Engine Logs 分析报告
  company: 您的公司名称
```

### 5. 运行应用

```bash
python3 app.py
```

应用启动后会：
1. 自动生成 Word 报告
2. 如果配置了邮件信息，自动发送邮件
3. 启动 Web 服务在 http://localhost:5000

## 常见邮件服务器配置

### Gmail
- 服务器: smtp.gmail.com
- 端口: 587 (TLS) 或 465 (SSL)
- 需要使用应用专用密码

### QQ 邮箱
- 服务器: smtp.qq.com
- 端口: 587 (TLS) 或 465 (SSL)
- 需要使用授权码

### 163 邮箱
- 服务器: smtp.163.com
- 端口: 465 (SSL)
- 需要使用授权码

### 阿里企业邮箱
- 服务器: smtp.qiye.aliyun.com
- 端口: 465 (SSL)

## 依赖包

- Flask==1.1.4
- Werkzeug==1.0.1
- python-docx==1.1.2
- PyYAML==6.0.1

## 注意事项

1. `config.yaml` 包含敏感信息，已被加入 `.gitignore`，不会被提交到 Git
2. 请妥善保管您的邮箱密码和授权码
3. 建议在虚拟环境中运行，避免污染系统 Python 环境
4. 如果使用 Gmail，必须启用"两步验证"并生成应用专用密码

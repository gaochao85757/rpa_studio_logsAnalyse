# Engine Logs 分析工具

基于 Python Flask 的日志文件分析网页应用，支持上传 engine.logs 文件并生成在线表格报告。

## 功能特性

- 文件上传: 支持 .log 格式文件上传
- 自动分析: 从 `Log.Info : 测试用例XXX` 开始到测试用例XXX结束
- 组件信息提取:
  - 组件模块
  - 组件中文名
  - 组件分类
  - 组件方法名
  - 组件插件包中文名
  - 组件唯一标识
- 错误检测: 自动识别 Exception 和 Error 异常
- 在线表格: 生成可交互的测试用例执行报告
- 错误详情: 点击错误链接查看日志上下文

## 安装步骤

1. 安装依赖:
   ```bash
   pip install -r requirements.txt
   ```

2. 运行应用:
   ```bash
   python app.py
   ```

3. 访问网页: 打开浏览器访问 http://localhost:5000

## 使用方法

1. 点击上传区域或拖拽 .log 文件
2. 点击"上传并分析"按钮
3. 查看生成的测试用例报告
4. 点击错误链接查看日志上下文

## 日志格式示例

```
2026-01-26 10:00:00 [INFO] rpa.main() start
2026-01-26 10:00:01 [INFO] Log.Info : 测试用例0001开始
2026-01-26 10:00:02 [INFO] 组件模块: CoreModule, 组件中文名: 核心模块, 组件分类: 基础, 组件方法名: Initialize, 组件插件包中文名: 基础插件包, 组件唯一标识: Core_Init_001
2026-01-26 10:00:03 [ERROR] Exception: NullPointerException - 错误描述
2026-01-26 10:00:04 [INFO] Log.Info : 测试用例0001结束
```

## 技术栈

- Python 3.x
- Flask
- HTML5/CSS3/JavaScript

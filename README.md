# Engine Logs 分析工具

基于 Python Flask 的日志文件分析网页应用，自动分析 engine.log 文件并生成在线测试用例执行报告。

## 功能特性

- **自动分析**: 自动读取并分析 `/static/engine.log` 文件
- **测试用例解析**: 从 `log_service.py` 的 `Log.Info : 测试用例XXX开始` 到 `测试用例XXX结束`
- **组件信息提取**:
  - 组件模块
  - 组件中文名
  - 组件分类
  - 组件方法名
  - 组件插件包中文名
  - 组件唯一标识
- **错误检测**: 自动识别 ERROR 日志中的异常信息
- **在线表格**: 生成可交互的测试用例执行报告
- **错误详情**: 点击错误链接查看详细错误信息

## 安装步骤

1. 安装依赖:
   ```bash
   pip install -r requirements.txt
   ```

2. 将 `engine.log` 文件放置到 `static/` 目录下:
   ```bash
   cp /path/to/engine.log static/
   ```

3. 运行应用:
   ```bash
   python3 app.py
   ```

4. 访问网页: 打开浏览器访问 http://localhost:5000/analysis

## 使用方法

1. 将 `engine.log` 文件放置到项目的 `static/` 目录
2. 启动 Flask 应用: `python3 app.py`
3. 访问 http://localhost:5000/analysis 查看自动生成的分析报告
4. 浏览测试用例列表，查看执行状态和组件信息
5. 如有错误，点击"查看详细错误"链接查看错误详情

## 日志格式示例

```
|2026-01-29 13:55:57,229| INFO|pid:2544967|tid:140270006922240|log_service.py: 25|None|None|engine|None|Log.Info : 测试用例0001开始|
|2026-01-29 13:55:57,230| DEBUG|pid:2544967|tid:140270006922240|option_util.py: 326|None|None|engine|None|组件模块为Element|
|2026-01-29 13:55:57,231| DEBUG|pid:2544967|tid:140270006922240|option_util.py: 328|None|None|engine|None|组件中文名为点击界面元素|
|2026-01-29 13:55:57,231| DEBUG|pid:2544967|tid:140270006922240|option_util.py: 330|None|None|engine|None|组件分类为["interface_element","webBrowser"]|
|2026-01-29 13:55:57,231| DEBUG|pid:2544967|tid:140270006922240|option_util.py: 332|None|None|engine|None|组件方法名为Click_V3|
|2026-01-29 13:55:57,231| DEBUG|pid:2544967|tid:140270006922240|option_util.py: 334|None|None|engine|None|组件插件包中文名为["interface_element","webBrowser"]|
|2026-01-29 13:55:57,232| DEBUG|pid:2544967|tid:140270006922240|option_util.py: 338|None|None|engine|None|组件唯一标识为Element.Click_V3|
|2026-01-29 13:55:58,136| INFO|pid:2544967|tid:140270006922240|log_service.py: 25|None|None|engine|None|Log.Info : 测试用例0001结束|
```

## API 接口

- `GET /analysis` - 查看分析页面
- `GET /analyze/default` - 获取默认日志文件的分析结果（JSON）
- `GET /engine.log` - 读取日志文件
- `GET /log/context/<line_idx>/<start>/<end>` - 获取日志上下文

## 技术栈

- Python 3.x
- Flask
- HTML5/CSS3/JavaScript

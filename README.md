# Engine Logs 分析工具

基于 Python Flask 的日志文件分析网页应用，自动分析 engine.log 文件并生成在线测试用例执行报告。

## 功能特性

### 自动分析
- 自动读取并分析 `/static/engine.log` 文件
- 从 `log_service.py` 的 `Log.Info : 测试用例XXX开始` 到 `测试用例XXX结束`
- 自动识别 ERROR 日志中的异常信息

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
5. 如有错误，查看运行结果列：
   - 默认显示简略的错误信息（150字符）
   - 点击错误信息可展开查看完整内容（250字符）
   - 再次点击可折叠
6. 点击"查看日志上下文"链接查看错误行周围的1000行日志

## 界面说明

### 统计卡片
- **总测试用例**: 日志中识别的测试用例总数
- **正常用例**: 执行成功的测试用例数量
- **异常用例**: 包含ERROR异常的测试用例数量
- **总组件数**: 所有测试用例中的组件总数

### 表格列说明
| 列名 | 说明 |
|-----|------|
| 测试用例ID | 测试用例编号（如：测试用例0001） |
| 组件模块 | 组件所属模块（如：Element） |
| 组件中文名 | 组件的中文名称（如：点击界面元素） |
| 组件分类 | 组件的分类标签（如：["interface_element","webBrowser"]） |
| 组件方法名 | 组件的方法名称（如：Click_V3） |
| 组件插件包中文名 | 组件插件包的中文名称 |
| 组件唯一标识 | 组件的唯一标识符（如：Element.Click_V3） |
| 运行结果 | 测试用例执行状态和错误信息 |

### 运行结果状态
- **执行正常**: 测试用例成功执行，无错误
- **异常报错**: 测试用例执行过程中发现ERROR异常
  - 简略显示：从ERROR/Exception开始的150字符
  - 展开显示：最多250字符的完整错误信息
  - 可点击"查看日志上下文"查看详细的日志上下文

### 错误详情模态框
- 标题：错误日志上下文（共1000行）
- 显示内容：错误行前后各500行的日志
- 错误行高亮：红色背景高亮显示
- 自动定位：打开时自动滚动到错误行中央
- 字体大小：15px
- 行号显示：紧凑的2px宽度

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
- `GET /log/context/<error_line>` - 获取错误行的日志上下文（前后各500行，共1000行）

### API 返回格式

#### /analyze/default
```json
{
  "success": true,
  "test_cases": [
    {
      "test_case_id": "0001",
      "component_info": {
        "module": "Element",
        "name_cn": "点击界面元素",
        "category": "[\"interface_element\",\"webBrowser\"]",
        "method": "Click_V3",
        "plugin_name": "[\"interface_element\",\"webBrowser\"]",
        "unique_id": "Element.Click_V3"
      },
      "has_error": false,
      "errors": [],
      "start_line": 41
    }
  ],
  "total": 2,
  "errors": 1
}
```

#### /log/context/<error_line>
```json
{
  "lines": [
    {
      "line_num": 0,
      "content": "日志内容",
      "is_error": false
    }
  ],
  "error_line": 438,
  "total_lines": 500,
  "context_start": 0,
  "context_end": 925,
  "context_size": 500
}
```

## 技术栈

- Python 3.x
- Flask
- HTML5/CSS3/JavaScript

## 界面参数

### 模态框
- 宽度：95%（最大 1400px）
- 高度：90vh
- 标题：错误日志上下文（共1000行）

### 日志显示
- 字体大小：15px
- 行高：1.3
- 行号宽度：2px
- 错误行背景：rgba(231, 76, 60, 0.3)
- 错误行左边框：3px #e74c3c

### 错误信息显示
- 简略显示：最多 150 字符
- 展开显示：最多 250 字符
- 背景：#fff5f5
- 字体大小：11px
- 字体粗细：500

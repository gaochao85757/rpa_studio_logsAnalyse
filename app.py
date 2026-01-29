from flask import Flask, render_template, request, jsonify, send_from_directory
import os
import re
from datetime import datetime

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['STATIC_FOLDER'] = 'static'

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['STATIC_FOLDER'], exist_ok=True)

class LogAnalyzer:
    def __init__(self, log_content):
        self.log_content = log_content
        self.test_cases = []
        self.log_lines = log_content.split('\n')

    def analyze(self):
        current_test_case = None
        current_lines = []
        in_test_case = False

        for idx, line in enumerate(self.log_lines):
            match_start = re.search(r'log_service\.py.*?Log\.Info\s*:\s*测试用例(\d+)\s*开始', line)
            match_end = re.search(r'log_service\.py.*?Log\.Info\s*:\s*测试用例(\d+)\s*结束', line)

            if match_start:
                test_case_id = match_start.group(1)

                if in_test_case and current_test_case:
                    self._process_test_case(current_test_case, current_lines)

                current_test_case = {
                    'test_case_id': test_case_id,
                    'component_info': {},
                    'has_error': False,
                    'errors': [],
                    'start_line': idx
                }
                current_lines = [(idx, line)]
                in_test_case = True

            elif match_end and in_test_case and current_test_case:
                end_test_case_id = match_end.group(1)
                if end_test_case_id == current_test_case['test_case_id']:
                    current_lines.append((idx, line))
                    self._process_test_case(current_test_case, current_lines)
                    current_test_case = None
                    in_test_case = False

            elif in_test_case:
                current_lines.append((idx, line))

        if in_test_case and current_test_case:
            self._process_test_case(current_test_case, current_lines)

        return self.test_cases

    def _extract_timestamp(self, line):
        match = re.search(r'(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})', line)
        return match.group(1) if match else ''

    def _process_test_case(self, test_case, lines):
        component_info = {
            'module': '',
            'name_cn': '',
            'category': '',
            'method': '',
            'plugin_name': '',
            'unique_id': ''
        }

        for line_idx, line in lines:
            if 'ERROR' in line:
                # 从ERROR或Exception开始提取错误信息
                error_match = re.search(r'(ERROR|Exception|Error)(.*)', line)
                if error_match:
                    error_message = (error_match.group(1) + error_match.group(2)).strip()
                    test_case['has_error'] = True
                    test_case['errors'].append({
                        'line': line_idx,
                        'message': error_message
                    })

            for key, pattern in {
                'module': r'组件模块为([^|]+)',
                'name_cn': r'组件中文名为([^|]+)',
                'category': r'组件分类为([^|]+)',
                'method': r'组件方法名为([^|]+)',
                'plugin_name': r'组件插件包中文名为([^|]+)',
                'unique_id': r'组件唯一标识为([^|]+)'
            }.items():
                if not component_info.get(key):
                    match = re.search(pattern, line)
                    if match and match.group(1):
                        value = match.group(1).strip()
                        if value and value != '为':
                            component_info[key] = value

        test_case['component_info'] = component_info
        self.test_cases.append(test_case)

    def _extract_component_info(self, line):
        patterns = {
            'module': r'组件模块[为]?[：:]\s*(\S+)',
            'name_cn': r'组件中文名[为]?[：:]\s*(.+?)(?:\s+组件|$)',
            'category': r'组件分类[为]?[：:]\s*(\[[^\]]+\]|[^\s,]+)',
            'method': r'组件方法名[为]?[：:]\s*(\S+)',
            'plugin_name': r'组件插件包中文名[为]?[：:]\s*(\[[^\]]+\]|[^\s,]+)',
            'unique_id': r'组件唯一标识[为]?[：:]\s*(\S+)'
        }

        component = {}
        for key, pattern in patterns.items():
            match = re.search(pattern, line)
            if match:
                value = match.group(1)
                if value and value != '为':
                    component[key] = value

        if component:
            return component
        return None

    def _get_context(self, line_idx, context_lines=10):
        start = max(0, line_idx - context_lines)
        end = min(len(self.log_lines), line_idx + context_lines + 1)
        return {
            'start': start,
            'end': end,
            'lines': [{'line_num': i, 'content': self.log_lines[i]} for i in range(start, end)]
        }

    def get_line_content(self, line_idx):
        if 0 <= line_idx < len(self.log_lines):
            return self.log_lines[line_idx]
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analysis')
def analysis():
    return render_template('log_analysis.html')

@app.route('/engine.log')
def get_engine_log():
    return send_from_directory(app.config['STATIC_FOLDER'], 'engine.log')

@app.route('/analyze/default')
def analyze_default_log():
    try:
        with open('/workspace/static/engine.log', 'r', encoding='utf-8') as f:
            log_content = f.read()

        analyzer = LogAnalyzer(log_content)
        test_cases = analyzer.analyze()

        return jsonify({
            'success': True,
            'test_cases': test_cases,
            'total': len(test_cases),
            'errors': sum(1 for tc in test_cases if tc['has_error'])
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/log/context/<int:error_line>')
def get_log_context(error_line):
    try:
        with open('/workspace/static/engine.log', 'r', encoding='utf-8') as f:
            all_lines = f.readlines()

        total_lines = len(all_lines)
        context_size = 500  # 错误行前后各500行，总共1000行

        start = max(0, error_line - context_size)
        end = min(total_lines, error_line + context_size + 1)

        context_lines = []
        for i in range(start, end):
            context_lines.append({
                'line_num': i,
                'content': all_lines[i].strip(),
                'is_error': i == error_line
            })

        return jsonify({
            'lines': context_lines,
            'error_line': error_line,
            'total_lines': total_lines,
            'context_start': start,
            'context_end': end,
            'context_size': context_size
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

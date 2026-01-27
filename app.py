from flask import Flask, render_template, request, jsonify
import os
import re
from datetime import datetime

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

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
            match_start = re.search(r'测试用例(\d+)\s*开始', line)
            match_end = re.search(r'测试用例(\d+)\s*结束', line)

            if match_start:
                test_case_id = match_start.group(1)

                if in_test_case and current_test_case:
                    current_test_case['end_line'] = idx - 1
                    self._process_test_case(current_test_case, current_lines)

                current_test_case = {
                    'test_case_id': test_case_id,
                    'components': [],
                    'has_error': False,
                    'errors': [],
                    'start_line': idx,
                    'start_time': self._extract_timestamp(line),
                    'end_line': None,
                    'end_time': None
                }
                current_lines = [(idx, line)]
                in_test_case = True

            elif match_end and in_test_case and current_test_case:
                end_test_case_id = match_end.group(1)
                if end_test_case_id == current_test_case['test_case_id']:
                    current_lines.append((idx, line))
                    current_test_case['end_line'] = idx
                    current_test_case['end_time'] = self._extract_timestamp(line)
                    self._process_test_case(current_test_case, current_lines)
                    current_test_case = None
                    in_test_case = False

            elif in_test_case:
                current_lines.append((idx, line))

        if in_test_case and current_test_case:
            current_test_case['end_line'] = len(self.log_lines) - 1
            self._process_test_case(current_test_case, current_lines)

        return self.test_cases

    def _extract_timestamp(self, line):
        match = re.search(r'(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})', line)
        return match.group(1) if match else ''

    def _process_test_case(self, test_case, lines):
        current_component = None

        for line_idx, line in lines:
            if 'Exception' in line or 'Error' in line:
                error_match = re.search(r'(Exception|Error)[:\s]*(.*)', line)
                if error_match:
                    error_message = error_match.group(2).strip() if error_match.group(2) else line.strip()
                    test_case['has_error'] = True
                    test_case['errors'].append({
                        'line': line_idx,
                        'message': error_message,
                        'context': self._get_context(line_idx)
                    })

            component_info = self._extract_component_info(line)
            if component_info:
                if current_component:
                    test_case['components'].append(current_component)
                current_component = component_info
            elif current_component:
                test_case['components'].append(current_component)
                current_component = None

        if current_component:
            test_case['components'].append(current_component)

        test_case['end_line'] = lines[-1][0] if lines else test_case['start_line']
        self.test_cases.append(test_case)

    def _extract_component_info(self, line):
        patterns = {
            'module': r'组件模块[：:]\s*(\S+)',
            'name_cn': r'组件中文名[：:]\s*(\S+)',
            'category': r'组件分类[：:]\s*(\S+)',
            'method': r'组件方法名[：:]\s*(\S+)',
            'plugin_name': r'组件插件包中文名[：:]\s*(\S+)',
            'unique_id': r'组件唯一标识[：:]\s*(\S+)'
        }

        component = {}
        for key, pattern in patterns.items():
            match = re.search(pattern, line)
            if match:
                component[key] = match.group(1)

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

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    if file.filename is None or file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    if not file.filename.endswith('.log'):
        return jsonify({'error': 'File must be .log format'}), 400

    try:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'engine_logs_{timestamp}.log'
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        with open(filepath, 'r', encoding='utf-8') as f:
            log_content = f.read()

        analyzer = LogAnalyzer(log_content)
        test_cases = analyzer.analyze()

        return jsonify({
            'success': True,
            'test_cases': test_cases,
            'total': len(test_cases),
            'errors': sum(1 for tc in test_cases if tc['has_error']),
            'file_path': filepath
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/log/context/<int:line_idx>/<int:start>/<int:end>')
def get_log_context(line_idx, start, end):
    try:
        log_file = request.args.get('file_path')
        if not log_file:
            return jsonify({'error': 'No file path provided'}), 400

        with open(log_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        context_lines = []
        for i in range(start, min(end + 1, len(lines))):
            context_lines.append({
                'line_num': i,
                'content': lines[i].strip(),
                'is_error': i == line_idx
            })

        return jsonify({'lines': context_lines})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

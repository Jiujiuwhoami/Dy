import os
import click
import re
import concurrent.futures
import datetime

# 定义漏洞规则
rules = {
    'SQL注入': r'union.*select|select.*(from|where).*',
    '任意文件读取': r'(\.\./|\\.\\./|\\.\.\\|\\|\\w|file=|path=|filepath=|open\(|load_file\(|pg_read_file\()',
    '命令执行': r'`|system\(|exec\(|shell_exec\(|popen\(|proc_open\(|passthru\(|pcntl_exec\(',
    'XSS攻击': r'<script|<img|<svg|javascript:|onload=|alert\(|prompt\(|confirm\(',
    'SSRF攻击': r'(http|https):\/\/[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}'
}
def get_current_time():
    now = datetime.datetime.now()
    return now.strftime("%Y-%m-%d_%H-%M-%S")
def analyze_log(log):
    vuln_results = []
    for vuln_type, vuln_pattern in rules.items():
        if re.search(vuln_pattern, log, re.IGNORECASE):
            vuln_results.append({'漏洞类型': vuln_type, '日志内容': log})
    return vuln_results

def get_log_files(logs_dir):
    log_files = []
    for root, dirs, files in os.walk(logs_dir):
        for file in files:
            if file.endswith('.log'):
                log_files.append(os.path.join(root, file))
    return log_files

def process_log(log_file):
    vuln_results = []
    with open(log_file, 'r') as log_file:
        logs = log_file.readlines()
        for log in logs:
            vuln_results.extend(analyze_log(log))
    return vuln_results

def generate_html_report(vuln_results):
    html_report = '<html><head><title>Vulnerability Report</title></head><body><h1>Vulnerability Report</h1>'
    
    if vuln_results:
        html_report += '<table border="1"><tr><th>漏洞类型</th><th>日志内容</th></tr>'
        for result in vuln_results:
            html_report += f'<tr><td>{result["漏洞类型"]}</td><td>{result["日志内容"]}</td></tr>'
        html_report += '</table>'
    else:
        html_report += '<p>No vulnerabilities found.</p>'
    
    html_report += '</body></html>'
    
    with open('vuln_report.html', 'w') as report_file:
        report_file.write(html_report)
def write_to_file(vuln_results):
    if vuln_results:
        current_time = get_current_time()
        output_dir = 'results'  # 创建一个名为 "results" 的文件夹
        os.makedirs(output_dir, exist_ok=True)  # 确保文件夹存在，如果不存在则创建
        output_file = os.path.join(output_dir, f'self-log-analysis_{current_time}.txt')  # 生成带有当前时间的文件名并设置路径
        with open(output_file, 'w', encoding='utf-8') as file:
            for result in vuln_results:
                # print(f'[!] 漏洞类型: {result["漏洞类型"]}\n   日志内容: {result["日志内容"]}\n')
                file.write(f'[!] 漏洞类型: {result["漏洞类型"]}\n   日志内容: {result["日志内容"]}\n')

# @click.command()
# @click.option('-d', '--logs-dir', type=click.Path(exists=True), help='日志文件夹路径')
current_dir = os.path.dirname(os.path.abspath(__file__))
logs_dir = os.path.join(current_dir, "logs")
def main(logs_dir):
    print("[*]logs文件路径为",logs_dir)
    log_files = get_log_files(logs_dir)

    vuln_results = []
    
    def process_logs(log_file):
        vuln_results.extend(process_log(log_file))
        
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        executor.map(process_logs, log_files)
    
    # generate_html_report(vuln_results)
    write_to_file(vuln_results)
    print('[*]日志分析脚本执行结束，请查看 results 文件夹下.txt文件')

if __name__ == '__main__':
    main(logs_dir)

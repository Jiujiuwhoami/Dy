
import configparser
from tabulate import tabulate  # 导入tabulate库
import os 

def automatic_execution(config,executor):
    command_list = []
    print("自动选择多个要执行的程序：")
    # 列出配置文件中的程序选项
    for section in config.sections():
        command_list.append([section,config[section]['common_command']])
    headers = ['程序名称', '命令信息']
    table = tabulate(command_list, headers, tablefmt='grid')
    print(table)
    choice = input("请输入选择程序（多个程序用‘,’分隔）：")
    choice_list = [c.strip() for c in choice.split(',')]  # 将输入的多个程序选择拆分为列表
    # 提示用户输入共享的参数
    shared_args = input("如有多个程序共享的参数请输入(用‘,’分隔),没有按回车：")
    input_values_list = shared_args.split(',')
    for section in choice_list:
        program_template = config[section]['common_command']
        # 如果程序通过路径方式执行，则完善绝对路径
        # if '/scripts/' in program_template:
        #     print('程序路径含有/scripts/')
        #     # 获取当前程序的完整路径
        #     current_script_path = os.path.abspath(__file__)
        #     # 使用当前程序的完整路径和相对路径构建完整路径
        #     program_template = os.path.join(os.path.dirname(current_script_path), program_template)
        # else:
        #     pass
        # 获取占位符和对应的值
        placeholders = get_placeholders(program_template)
        # 创建字典来映射占位符和值
        values = {placeholder: value for placeholder, value in zip(placeholders, input_values_list)}
        print(f"执行程序：{section}")
        program = program_template.format(**values)
        print('[*]开始执行命令:',program)
        print("$"*100)
        executor.execute_command(program)
        # print(f"执行结果 ({section})：")
        # print("标准输出：")
        # print(result["stdout"])
        # print("标准错误：")
        # print(result["stderr"])
        print("[*]命令执行结束")
        print("$"*100)
def get_placeholders(command_template):
    # 从命令模板中提取占位符
    import re
    placeholders = re.findall(r'\{(\w+)\}', command_template)
    return placeholders
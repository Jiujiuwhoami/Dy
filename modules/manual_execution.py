import configparser
from tabulate import tabulate  # 导入tabulate库
import os

def manual_execution(config, executor):
    while True:
        print('\n')
        print("手动选择单个要执行的操作：")
        print("1. 选择程序执行")
        print("2. 查看帮助信息")
        print("C. 进入控制台")
        print("Q. 退出")

        choice = input("请输入选项：")

        if choice == "1":
            execute_program(config, executor)
        elif choice == "2":
            display_program_help(config)  # 显示所选择程序的帮助信息
        elif choice == "C" or choice == "c":
            executor.open_new_terminal()
        elif choice == "Q" or choice == "q":
            break
        else:
            print("无效的选项，请重新选择。")

def display_program_help(config):
    print("请选择要查看帮助信息的程序：")
    
    # 列出配置文件中的程序选项
    for section in config.sections():
        print(section)
    
    choice = input("请输入选项：")
    
    if choice in config:
        help_message = config[choice].get('help_message', '无帮助信息可用')
        # 使用tabulate库创建表格并打印
        headers = ['程序名称', '帮助信息']
        table = tabulate([[choice,help_message]], headers, tablefmt='grid')
        print(table)
    else:
        print("无效的选项，请重新选择。")

def execute_program(config, executor):
    print("请选择要执行的程序：")
    
    # 列出配置文件中的程序选项
    for section in config.sections():
        print(section)
    
    choice = input("请输入选项：")
    
    if choice in config:
        help_message = config[choice].get('help_message', '无帮助信息可用')
        # 使用tabulate库创建表格并打印
        headers = ['程序名称', '帮助信息']
        table = tabulate([[choice,help_message]], headers, tablefmt='grid')
        print(table)
        program_template = config[choice]['command']
        extra_args = input("如有额外的参数请输入（空格分隔），无参请按回车：")
        extra_args = extra_args.split()   
        # if '/scripts/' in program_template:
        #     print('程序路径含有/scripts/')
        #     # 获取当前程序的完整路径
        #     current_script_path = os.path.abspath(__file__)
        #     # 使用当前程序的完整路径和相对路径构建完整路径
        #     program_template = os.path.join(os.path.dirname(current_script_path), program_template)
        #     program_template = program_template + " " + " ".join(extra_args)
        # else:
            # 构建完整的命令
        program_template = program_template + " " + " ".join(extra_args)
           
        print('[*]开始执行命令:',program_template)
        print("$"*100)
        executor.execute_command(program_template)

        # print(f"执行结果 ({choice})：")
        # print("标准输出：")
        # print(result["stdout"])
        # print("标准错误：")
        # print(result["stderr"])     
    else:
        print("无效的选项，请重新选择。")
    print("[*]命令执行结束")
    print("$"*100)

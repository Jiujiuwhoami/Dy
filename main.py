import configparser
from modules.manual_execution import manual_execution
from modules.automatic_execution import automatic_execution
from modules.executor import CommandLineExecutor
from modules.notebook import notebook
import io
from tabulate import tabulate  # 导入tabulate库
# import textwrap
software_header ='''

______                                             
|  _  \                                            
| | | |_   _                                       
| | | | | | |                                      
| |/ /| |_| |                                      
|___/  \__, |_ _       _ _                         
        __/ (_(_)     (_(_)                        
       |___/ _ _ _   _ _ _ _   _ _   _  __ _  ___  
            | | | | | | | | | | | | | |/ _` |/ _ \ 
            | | | |_| | | | |_| | |_| | (_| | (_) |
            | |_|\__,_| |_|\__,_|\__, |\__,_|\___/ 
           _/ |      _/ |         __/ |            
          |__/      |__/         |___/             

'''
additional_text = '''
    * 程序被简单加密，如需解密，请 WX 搜索公众号： 九九妖舍 ，号内发送“ 天缺 ” ，将自动获取密码。
    * 初心想要编写一个像 msf 那样的框架，因此有很多开源程序的直接引用，这一部分原作者保留全部解释权。
    * 免责声明：此程序仅供学习交流使用，请勿用于违法行为。
    
    * The program is encrypted. To decrypt it, please search for the official WeChat (WX) public account: jiujiuyao_home, and send "Dy" within the account. You will automatically receive the password.
    * I originally wanted to develop a framework similar to Metasploit (MSF), so there are many direct references to open-source programs. The original authors retain all rights to interpretation for this part.
    * Disclaimer: This program is for educational and exchange purposes only. Please do not use it for illegal activities.
'''
def main():
    config_path = ""
    while True:
        print('\n')
        s = input("请输入密码：")
        if s == '666666':
            while True:
                print('\n')
                print("请选择模块：")
                print("1. 信息收集与漏洞扫描")
                print("2. 应急响应")
                print("3. 添加后门")
                print("4. bug利用")
                print("Q. 退出")
                choice = input("请输入选项：")

                if choice == "1":
                    config_path = "config/config_web.ini"
                    a(config_path)
                elif choice == "2":
                    config_path = "config/config_emergency.ini"
                    a(config_path)
                elif choice == "3":
                    config_path = "config/config_back.ini"
                    a(config_path)
                elif choice == "4":
                    config_path = "config/config_virus.ini"
                    a(config_path)
                elif choice == "Q" or choice == "q":
                    break
                else:
                    print("无效的选项，请重新选择。")
        else:
            print('密码错误，请重新输入')
def a(config_path):
   # 打开配置文件并以utf-8编码读取
    with io.open(config_path, "r", encoding="utf-8") as file:
        config_data = file.read()

    config = configparser.ConfigParser()
    config.read_string(config_data)

    # 实例化CommandLineExecutor类
    executor = CommandLineExecutor()

    while True:
        print('\n')
        print("请选择操作：")
        print("1. 查看程序列表与帮助信息")
        print("2. 手动执行单个程序")
        print("3. 自动执行多个程序")
        print("4. 启动记事簿")
        print("C. 进入控制台")
        print("Q. 退出")

        choice = input("请输入选项：")

        if choice == "1":
            display_help_messages(config)  # 显示帮助信息
        elif choice == "2":
            manual_execution(config, executor)
        elif choice == "3":
            automatic_execution(config, executor)
        elif choice == "C" or choice == "c":
            executor.open_new_terminal()
        elif choice == "4":
            notebook(executor)
        elif choice == "Q" or choice == "q":
            break
        else:
            print("无效的选项，请重新选择。")

def display_help_messages(config):
    help_data = []  # 用于存储帮助信息的列表

    # 提取帮助信息并转换为表格
    for section in config.sections():
        program_name = section
        help_message = config[section].get('help_message', '无帮助信息可用')
        #  # 使用textwrap.wrap包装帮助信息，以确保在表格中显示整齐
        # wrapped_help_message = '\n'.join(textwrap.wrap(help_message, width=60))
        help_data.append([program_name, help_message])

    # 使用tabulate库创建表格并打印
    headers = ['程序名称', '帮助信息']
    table = tabulate(help_data, headers, tablefmt='grid',colalign=("left", "left"), stralign=("center", "left"), numalign="center")
    print(table)
if __name__ == "__main__":
    print(software_header + additional_text)
    main()

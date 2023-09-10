# import subprocess

# class CommandLineExecutor:
#     def execute_command(self, command):
#         try:
#             # 使用subprocess执行命令
#             process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#             stdout, stderr = process.communicate()

#             # 检查命令的返回代码
#             if process.returncode == 0:
#                 return {
#                     "success": True,
#                     "stdout": stdout.decode("utf-8"),
#                     "stderr": stderr.decode("utf-8")
#                 }
#             else:
#                 return {
#                     "success": False,
#                     "stdout": stdout.decode("utf-8"),
#                     "stderr": stderr.decode("utf-8")
#                 }
#         except Exception as e:
#             return {
#                 "success": False,
#                 "stderr": str(e)
#             }

import subprocess
import threading
import platform
class CommandLineExecutor:
    def execute_command(self, command):
        try:
            # 使用subprocess创建一个交互式子进程
            process = subprocess.Popen(
                command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                stdin=subprocess.PIPE,
                text=True,
                bufsize=1,  # 行缓冲，以便实时交互
                universal_newlines=True  # 使用文本模式，以便处理换行符
            )

            # 创建一个线程来读取并打印子进程的标准输出
            stdout_thread = threading.Thread(target=self._read_and_print_output, args=(process.stdout,))
            stdout_thread.start()

            # 创建一个线程来读取并打印子进程的标准错误输出
            stderr_thread = threading.Thread(target=self._read_and_print_output, args=(process.stderr,))
            stderr_thread.start()

            # 读取用户输入并发送到程序的标准输入
            while True:
                user_input = input()
                if not user_input:
                    break
                process.stdin.write(user_input + '\n')
                process.stdin.flush()

            # 等待子进程完成
            process.wait()

            # 等待标准输出和标准错误输出的线程完成
            stdout_thread.join()
            stderr_thread.join()
           
            return {
                "success": process.returncode == 0,
                "returncode": process.returncode
            }
        except Exception as e:
            print(str(e))
            return {
                "success": False,
                "stderr": str(e)
            }

    def _read_and_print_output(self, stream):
        while True:
            line = stream.readline()
            if not line:
                break
            print(line.strip())
    def open_new_terminal(self):
        while True:
            command = input("console >>")
            if command == 'exit':
                break
            self.execute_command(command)
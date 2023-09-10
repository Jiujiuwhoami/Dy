import os
def notebook(executor):
	# 获取当前模块所在目录（modules目录）
	module_directory = os.path.dirname(__file__)

	# 定义存储XSS POC和一句话木马的文件路径，包括notebooks文件夹
	notebooks_folder = os.path.join(module_directory, "..", "notebooks")
	xss_poc_file = os.path.join(notebooks_folder, "xss_poc.txt")
	web_back_file = os.path.join(notebooks_folder, "web_back.txt")
	while True:
		print('\n')
		print("请选择主题：")
		print("1. xss_poc")
		print("2. web木马")
		print("C. 进入控制台")
		print("Q. 退出")

		choice = input("请输入选项：")

		if choice == "1":
			view_xss_poc(xss_poc_file)
		elif choice == "2":
			view_web_back(web_back_file)  # 显示所选择程序的帮助信息
		elif choice == "C" or choice == "c":
			executor.open_new_terminal()
		elif choice == "Q" or choice == "q":
			break
		else:
			print("无效的选项，请重新选择。")
def view_xss_poc(xss_poc_file):
	if os.path.exists(xss_poc_file):
		with open(xss_poc_file, "r") as file:
			xss_poc = file.read()
			print("XSS_POC语句：")
			print(xss_poc)
	else:
		print("XSS_POC文件为空。")
def view_web_back(web_back_file):
	if os.path.exists(web_back_file):
		with open(web_back_file, "r") as file:
			web_back = file.read()
			print("web_back语句：")
			print(web_back)
	else:
		print("web_back文件为空。")
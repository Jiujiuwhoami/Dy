from pyfiglet import Figlet

def create_ascii_art(text):
    custom_fig = Figlet(font='block')  # 选择字体，您可以根据需要更改字体
    ascii_art = custom_fig.renderText(text)
    return ascii_art

if __name__ == "__main__":
    text = "天缺"  # 您想要生成的中文字符
    ascii_art = create_ascii_art(text)
    print(ascii_art)

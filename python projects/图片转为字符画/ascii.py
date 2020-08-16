from PIL import Image
import argparse
# 构建命令行输入参数处理 ArgumentParser实例
parser = argparse.ArgumentParser()
#定义输入/出文件，输出字符的宽高
parser.add_argument('file')       #输入文件
parser.add_argument('-o','--output')    #输出文件
parser.add_argument('--width',type=int,default=80)  #输出字符画宽
parser.add_argument('--height',type=int,default=80)   #输出字符画高

#解析并获取参数
args = parser.parse_args()

#输入的图片文件路径
IMG = args.file

#输出字符画的宽度
WIDTH = args.width

#输出字符画的高度
HEIGHT = args.height

#输出字符画的路径
OUTPUT = args.output
#字符画所使用的字符集
ascii_char = list("$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. ")

#RGB转字符的函数
def get_char(r,g,b,alpha = 250):
    #判断alpha的值
    if alpha == 0:
        return ''
    #获取字符集的长度
    length = len(ascii_char)

    #将RGB值转为灰度值gray，灰度值范围为0~255
    gray = int(0.2126*r+0.7152*g+0.0722*b)
    #灰度值范围为0~255,而字符集的长度为70
    #需要进行下方操作才能将灰度值映射到指定的字符上
    unit = (256.0+1)/length
    #返回灰度值相应的字符
    return ascii_char[int(gray/unit)]

if __name__ == '__main__':
    #打开并调整图片的宽和高
    im = Image.open(IMG)
    im = im.resize((WIDTH,HEIGHT), Image.NEAREST)

    txt = ""

    for i in range(HEIGHT):
        for j in range(WIDTH):
            # 将(j,i)坐标的RGB，像素转为字符后添加到txt字符串
            txt += get_char(*im.getpixel((j,i)))        
        txt += '\n'
    print(txt)

    # 字符画输出到文件
    if OUTPUT:
        with open(OUTPUT,'w') as f:
            f.write(txt)
    else:
        with open("ouput.txt",'w') as f:
            f.write(txt)
# -*- coding: UTF-8 -*-
"""
# @Time: 2021/8/21 20:11
# @Author: 远方的星
# @CSDN: https://blog.csdn.net/qq_44921056
"""
import os
from PIL import Image
from PIL import ImageFile
# 跳过“损坏”图片
ImageFile.LOAD_TRUNCATED_IMAGES = True
# 读取文件内部文件名，并生成一个列表
image_list = os.listdir("H:/极简壁纸")
# 定义一个参数，有助于行、列的确定
lines = 10
# 定义照片墙中每一张图片的宽和高
image_width = 192
image_height = 108
# 定义一个照片墙的大小
image_wall = Image.new("RGB", (image_width*lines, image_height*lines))
# 定义两个参数用于记录坐标
x = 0
y = 0
# 这里的范围注意，要与image_wall相匹配，应该是10*10
for i in range(0, lines*6):
    # 读取每一张素材图片
    image = Image.open("H:/极简壁纸/" + image_list[i])
    # 对素材图片进行重新设定大小
    image = image.resize((image_width, image_height))
    # 把素材图片放到照片墙的相应位置
    image_wall.paste(image, (x*image_width, y*image_height))
    # 按行摆放图片
    x += 1
    if x == lines:
        x = 0
        y += 1
    # 按列摆放图片
    # y += 1
    # if y == lines
    #     y = 0
    #     x += 1
# 展示图片
image_wall.show()
# 保存图片
image_wall.save("H:/image_wall.png")
print("照片墙保存完成啦^_^")

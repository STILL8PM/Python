from PIL import Image  # 导入PIL的Image包
import os
gifFileName = "./demo.gif"  # 把gif图赋值给gifFileName
im = Image.open(gifFileName)  # 使用Image的open函数打开test.gif图像
pngDir = gifFileName[:-4]  # 倒着从gifFileName中的倒数第四个开始取字符（跳过.gif），赋值给pngDir，作为文件夹的名字
if not os.path.exists(pngDir):
    os.makedirs('./img')  # 用图片名创建一个文件夹，用来存放每帧图片，名字为pngDir的值

try:
  while True:  # 死循环
    current = im.tell()  # 用tell函数保存当前帧图片，赋值给current
    im.save('./img'+pngDir+str(current+1)+'.png')  # 调用save函数保存该帧图片
    im.seek(current+1)  # 调用seek函数获取下一帧图片，参数变为current帧图片+1
    # 这里再次进入循环，当为最后一帧图片时，seek会抛出异常，代码执行except
except EOFError:
    pass  # 最后一帧时，seek抛出异常，进入这里，pass跳过



# # 将视频按照每一帧转成图片png
# import cv2
# videoFileName = "./demo.mp4"  # 把视频路径赋值给videoFileName
# pngDir = videoFileName[:-4]  # 倒着从gifFileName中的倒数第四个开始取字符（跳过.后缀），赋值给pngDir，作为文件夹的名字
# if not os.path.exists(pngDir):
#     os.makedirs(pngDir)  # 用图片名创建一个文件夹，用来存放每帧图片，名字为pngDir的值
# # 视频处理 分割成一帧帧图片
# cap = cv2.VideoCapture(videoFileName)
# num = 1
# while True:
#     # 逐帧读取视频  按顺序保存到本地文件夹
#     ret, frame = cap.read()
#     if ret:
#         cv2.imwrite(f"{pngDir}/{num}.png", frame)  # 保存一帧帧的图片
#         num += 1
#     else:
#         break
# cap.release()   # 释放资源

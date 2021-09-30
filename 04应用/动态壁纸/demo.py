FILE_FORMATS={
"图片资料":[".jpg",".jpeg",".bpm",'.png','.gif'],
"文档资料":[".doc",".docx",".xls",".xlsx",".ppt",".pptx",".pdf",".txt",".md"],
"视频文件":[".mp4","avi","wmv",],
"音频文件":[".mp3"],
"压缩文件":[".rar",".zip",".tar",".gz",".7z","bz"],
"脚本文件":[".ps1",".sh",".bat",".py"],
"可执行文件":['.exe','.msi'],
"网页文件":['.html','.xml','.mhtml','.html'],
"快捷方式":[".lnk"],
}
#定义要整理的文件夹
orginizePath='D:\\direct'
print(os.scandir(orginizePath))
 
#循环整理的文件夹。
for myfile in os.scandir(orginizePath):
    #跳过文件夹
    if myfile.is_dir():
        print('%s是文件夹'%myfile)
        continue
    #输出文件的名
    print(myfile.name)
    #找到要整理的文件路径
    file_path=Path(orginizePath+'\\'+myfile.name)
    lower_file_path=file_path.suffix.lower()
    #循环遍历我们定义的格式类型
    for geshi in FILE_FORMATS:
        if lower_file_path in FILE_FORMATS[geshi]:
            directory_path=Path(orginizePath+'\\'+geshi)
            directory_path.mkdir(exist_ok=True)
            file_path.rename(directory_path.joinpath(myfile.name))
            print('文件整理已完成！')
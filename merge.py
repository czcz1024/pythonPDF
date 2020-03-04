# -*- coding:utf-8*-
# 利用PyPDF2模块合并同一文件夹下的所有PDF文件
# 只需修改存放PDF文件的文件夹变量：file_dir 和 输出文件名变量: outfile

import os
try:
    from PyPDF2 import PdfFileReader, PdfFileWriter
except:
    os.system('pip install pypdf2')
    from PyPDF2 import PdfFileReader, PdfFileWriter
    
import time
try:
    from gooey import Gooey,GooeyParser
except :
    os.system('pip install gooey')
    from gooey import Gooey,GooeyParser
# 使用os模块的walk函数，搜索出指定目录下的全部PDF文件
# 获取同一目录下的所有PDF文件的绝对路径
def getFileName(filedir):

    file_list = [os.path.join(root, filespath) \
                 for root, dirs, files in os.walk(filedir) \
                 for filespath in files \
                 if str(filespath).endswith('pdf')
                 ]
    return file_list if file_list else []

# 合并同一目录下的所有PDF文件
def MergePDF(filepath, outfile):

    output = PdfFileWriter()
    outputPages = 0
    pdf_fileName = getFileName(filepath)

    if pdf_fileName:
        for pdf_file in pdf_fileName:
            print("路径：%s"%pdf_file)

            # 读取源PDF文件
            input = PdfFileReader(open(pdf_file, "rb"))

            # 获得源PDF文件中页面总数
            pageCount = input.getNumPages()
            outputPages += pageCount
            print("页数：%d"%pageCount)

            # 分别将page添加到输出output中
            for iPage in range(pageCount):
                output.addPage(input.getPage(iPage))

        print("合并后的总页数:%d."%outputPages)
        # 写入到目标PDF文件
        outputStream = open(os.path.join(filepath, outfile), "wb")
        output.write(outputStream)
        outputStream.close()
        print("PDF文件合并完成！")

    else:
        print("没有可以合并的PDF文件！")

# 主函数

@Gooey(language='chinese',progress_regex=r"(\d+)%",hide_progress_msg=True
        ,program_name='PdfMerge',program_description='合并文件夹下的PDF')
def main():
    parser = GooeyParser(description="合并文件夹下的PDF") 
    parser.add_argument('Dirname', widget="DirChooser",metavar='要合并的pdf存放目录', help="选择存放PDF的文件夹",gooey_options={'full_width': True,'message': "选择存放PDF的文件夹"})
    parser.add_argument('Filename',default='output.pdf',metavar="保存文件名", help="选择pdf文件",gooey_options={'full_width': True,'message': "合并后的文件名称"})    
    args = parser.parse_args()
    

    # time1 = time.time()
    # file_dir = r'E:\LearnAndTest\python\pdf2img\srouce' # 存放PDF的原文件夹
    # outfile = "Cheat_Sheets.pdf" # 输出的PDF文件的名称
    MergePDF(args.Dirname, args.Filename)
    # time2 = time.time()
    # print('总共耗时：%s s.' %(time2 - time1))

if __name__=='__main__':
    main()
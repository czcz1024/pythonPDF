import os
try:
    from PyPDF2 import PdfFileReader, PdfFileWriter
except:
    os.system('pip install pypdf2')
    from PyPDF2 import PdfFileReader, PdfFileWriter
from PIL import Image    
import time
try:
    from gooey import Gooey,GooeyParser
except :
    os.system('pip install gooey')
    from gooey import Gooey,GooeyParser

def getFileName(filedir):

    file_list = [os.path.join(root, filespath) \
                 for root, dirs, files in os.walk(filedir) \
                 for filespath in files \
                 if str(filespath).endswith('png') or str(filespath).endswith('jpg') or str(filespath).endswith('jpeg')
                 ]
    return file_list if file_list else []

def Img2PDF(filepath, outfile):

    output = PdfFileWriter()
    outputPages = 1
    img_fileName = getFileName(filepath)
    img_fileName.sort(key= lambda x: int(x[x.index('images_')+7:-4]))
    if img_fileName:
        im_list = []
        im1 = Image.open(img_fileName[0])
        img_fileName.pop(0)
        for i in img_fileName:
            print("路径：%s"%i)
            img = Image.open(i)
            # im_list.append(Image.open(i))
            if img.mode == "RGBA":
                img = img.convert('RGB')                
            im_list.append(img)
            outputPages+=1

        im1.save(outfile, "PDF", resolution=100.0, save_all=True, append_images=im_list)


        # for img_file in img_fileName:
        #     print("路径：%s"%img_file)
        #     img=Image.open(img_file)
            # 读取源PDF文件
            # input = PdfFileReader(open(pdf_file, "rb"))

            # # 获得源PDF文件中页面总数
            # pageCount = input.getNumPages()
            # outputPages += pageCount
            # print("页数：%d"%pageCount)

            # 分别将page添加到输出output中
            #for iPage in range(pageCount):
            # output.addPage(img)

        print("合并后的总页数:%d."%outputPages)
        # 写入到目标PDF文件
        # outputStream = open(os.path.join(filepath, outfile), "wb")
        # output.write(outputStream)
        # outputStream.close()
        print("PDF文件合并完成！")

    else:
        print("没有可以合并的PDF文件！")


@Gooey(language='chinese',progress_regex=r"(\d+)%",hide_progress_msg=True,program_name='PdfMerge',program_description='合并文件夹下的PDF')
def main():
    parser = GooeyParser(description="合并文件夹下的PDF") 
    parser.add_argument('Dirname', widget="DirChooser",metavar='要合并的pdf存放目录', help="选择存放PDF的文件夹",gooey_options={'full_width': True,'message': "选择存放PDF的文件夹"})
    parser.add_argument('Filename',default='output.pdf',metavar="保存文件名", help="选择pdf文件",gooey_options={'full_width': True,'message': "合并后的文件名称"})    
    args = parser.parse_args()
    

    # time1 = time.time()
    # file_dir = r'E:\LearnAndTest\python\pdf2img\srouce' # 存放PDF的原文件夹
    # outfile = "Cheat_Sheets.pdf" # 输出的PDF文件的名称
    Img2PDF(args.Dirname, args.Filename)
    # time2 = time.time()
    # print('总共耗时：%s s.' %(time2 - time1))

if __name__=='__main__':        
    main()
import sys
import os
import datetime
import io
try:
    from tqdm import tqdm
except :
    os.system('pip install tqdm')
    from tqdm import tqdm

try:
    from gooey import Gooey,GooeyParser
except :
    os.system('pip install gooey')
    from gooey import Gooey,GooeyParser

from contextlib import redirect_stderr

try:
    import fitz
except:
    print('install pymupdf')
    os.system('pip install pymupdf')

    import fitz
 
def pyMuPDF_fitz(pdfPath, imagePath):
    startTime_pdf2img = datetime.datetime.now()#开始时间
    
    print("imagePath="+imagePath)
    pdfDoc = fitz.open(pdfPath)

    progress_bar_output = io.StringIO()
    with redirect_stderr(progress_bar_output):
        for pg in tqdm(range(pdfDoc.pageCount)):
            page = pdfDoc[pg]
            rotate = int(0)
            # 每个尺寸的缩放系数为1.3，这将为我们生成分辨率提高2.6的图像。
            # 此处若是不做设置，默认图片大小为：792X612, dpi=96
            zoom_x = 1.33333333 #(1.33333333-->1056x816)   (2-->1584x1224)
            zoom_y = 1.33333333
            mat = fitz.Matrix(zoom_x, zoom_y).preRotate(rotate)
            pix = page.getPixmap(matrix=mat, alpha=False)
            
            if not os.path.exists(imagePath):#判断存放图片的文件夹是否存在
                os.makedirs(imagePath) # 若图片文件夹不存在就创建
            
            pix.writePNG(imagePath+'/'+'images_%s.png' % pg)#将图片写入指定的文件夹内
            #tqdm.write("progress: {}/{}".format(pg + 1, pdfDoc.pageCount))
            prog = progress_bar_output.getvalue().split('\r ')[-1].strip()
            print(prog)
            #print("progress: {}/{}".format(pg + 1, pdfDoc.pageCount))            
            #sys.stdout.flush()
        
    endTime_pdf2img = datetime.datetime.now()#结束时间
    print('pdf2img时间=',(endTime_pdf2img - startTime_pdf2img).seconds)





#'^(?P<percent>\d+)\%|.+$'

#@Gooey(progress_regex=r'^(?P<percent>\d+)\%|.+$',progress_expr="percent")
#@Gooey
#@Gooey(progress_regex=r"^progress: (?P<current>\d+)/(?P<total>\d+)$",progress_expr="current / total * 100",hide_progress_msg=True)
@Gooey(language='chinese',progress_regex=r"(\d+)%",hide_progress_msg=True
        ,program_name='Pdf2Img',program_description='pdf 转图片')
def main():
    # try:
    #     pdfFile=sys.argv[1]    
    #     saveDir=sys.argv[2]
    #     if(not pdfFile.endswith('.pdf')):
    #         print('pdf file must end with .pdf')
    #         return
        
    #     print(pdfFile,'save to ',saveDir)
    #     pyMuPDF_fitz(pdfFile,saveDir)
    # except :
    #     print('usage:python convert.py pdfFile saveDir')
    parser = GooeyParser(description="pdf转图片") 
    parser.add_argument('Filename', widget="FileChooser", help="选择pdf文件",gooey_options={'full_width': True,'wildcard':"PDF file (*.pdf)|*.pdf|",'message': "选择一个pdf文件"})
    parser.add_argument('Dirname', widget="DirChooser", help="选择保存图片的文件夹",gooey_options={'full_width': True,'message': "选择图片保存目录"})

    args = parser.parse_args()
    #t(args.Filename,args.Dirname)
    #print(len(args))
    #print('Hooray!',type(args))
    pyMuPDF_fitz(args.Filename,args.Dirname)
 
if __name__ == "__main__":    
    main()
        
    # pdfPath = 'a.pdf'
    # imagePath = 'image/'
    # pyMuPDF_fitz(pdfPath, imagePath)
    #pyMuPDF_fitz(pdfFile,saveDir)
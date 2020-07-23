import os

from PIL import Image, ImageFile
from config import INPUT_DIR, OUTPUT_DIR
from PIL import Image, ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES =True
class MangaToPDF:
    def __init__(self, manga_name):
        self._manga_name = manga_name
        self._output_dir = ""
        self._input_dir = ""
        self.set_output_dir()
        self.set_input_dir()
    
    def set_input_dir(self,folder_name=None):
        if folder_name == None:
            self._input_dir = os.path.join(INPUT_DIR,self._manga_name)

    def set_output_dir(self,folder_name=None):
        if folder_name == None:
            self._output_dir = os.path.join(OUTPUT_DIR)
            os.makedirs(self._output_dir, exist_ok=True)
    
    def convert_to_pdf(self):
        files = []
        chapter_dir = sorted([int(i) for i in  os.listdir(self._input_dir)])
        chapter_dir = [os.path.join(self._input_dir,str(i)) for i in chapter_dir]
        for chap in chapter_dir:
            for r,d,f in os.walk(chap):
                chap_files = []
                for file in f:
                    if '.jpg' in file:
                        chap_files.append(int(file[:len(file)-4]))
                        chap_files.sort()
                for file in chap_files:
                    files.append(os.path.join(r,str(file)+'.jpg'))

        img1 = Image.open(files[0]).convert('RGB')
        img_list = []
        for f in files[1:]:
            img_list.append(Image.open(f).convert('RGB'))
        output_path = os.path.join(self._output_dir, self._manga_name+'.pdf')
        try:
            img1.save(output_path, save_all=True, append_images=img_list)
            return 1
        except:
            return 0
    
# ----- TEST ----------
# if __name__ == "__main__":
#     m = MangaToPDF(manga_name='TOG')
#     m.convert_to_pdf()
# input_path = os.path.join(INPUT_DIR, 'TOG')      
# files = []
# for r, d, f in os.walk(input_path):
#     for file in f:
#         if '.jpg' in file:
#             files.append(os.path.join(r, file))
# files.sort()
# for i in files:
#     print(i)



# file_name = '0.jpg'
# input_path = os.path.join(INPUT_DIR, 'TOG','chap_0',file_name)
# o_file_name = '0.pdf'
# output_path = os.path.join(OUTPUT_DIR,o_file_name)

# os.makedirs(OUTPUT_DIR, exist_ok=True)
# input_data = Image.open(input_path)
# output_data = input_data.convert('RGB')
# output_data.save(output_path)

#D:\project\mangaToPdf\main\data\input\TOG\chap_0\0.jpg
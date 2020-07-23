
import requests 
import shutil 
import os

from config import INPUT_DIR
from requests_html import HTMLSession




class NetTruyenScraw():
    SESSION = HTMLSession()
    def __init__(self,name="None",url="None"):
        self._url = url
        self._name = name # Shouldn't contain space
        self._r = self.SESSION.get(self._url)
        
        if self._r.status_code != 200:
            print(self._r.status_code)
            raise ValueError("Url error")

    def get_chapter_links(self):
        # OUTPUT >> return a list of chapter links
        chapter_class_list = self._r.html.find('.col-xs-5.chapter')
        links = []
        for chapter in chapter_class_list:
            for l in chapter.links:
                links.append(l)
        return links

    def download_img(self,img_el,chapter_url,file_name,dl_path):
        # save imgs to dl_path/MangaName/ChapterNo/file_name.jpg
        manga_name = self._name if self._name != None else self._url.split('/')[-1]
        img_url = img_el.attrs['src']
        chapter = chapter_url.split('/')[-2]
        chapter = chapter[5:]
        
        headers = {
            "Referer": chapter_url # Chapter URL , set this to pass Cloudfare service
        }
        filename = str(file_name) + '.jpg'
        r = requests.get(img_url, stream = True, headers=headers)
        # Check if the image was retrieved successfully
        print(r.status_code)
        if r.status_code == 200:
            # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
            r.raw.decode_content = True
            # Open a local file with wb ( write binary ) permission.
            img_path = os.path.join(dl_path,manga_name,chapter)
            os.makedirs(img_path, exist_ok=True)
            img_dir = os.path.join(img_path, filename)
            with open(img_dir,'wb') as f:
                shutil.copyfileobj(r.raw, f)
            print('Image sucessfully Downloaded: ',filename)
        else:
            print('Image Couldn\'t be retreived')

    def run(self, chapter_links=None, chapter_start=1, total=1, dl_path=INPUT_DIR):
        # INPUT >>> list of chapter links
        # OUTPUT >>> return a list of img elements
        
        if chapter_links == None :
            chapter_links = self.get_chapter_links()
        chapter_range = []
        if total == '__all__':
            chapter_range = chapter_links[::-1]
        else:
            chapter_links = chapter_links[::-1]
            chapter_range = chapter_links[chapter_start-1:total]
        for c in chapter_range:
            chapter = self.SESSION.get(c)
            img_el_list = chapter.html.find(".page-chapter > img") # Class in each IMG
            # chapter_img = chapter_class[0].find('img')
            # img_url = chapter_img[0].attrs['src']
            for i,img in enumerate(img_el_list):
                try:
                    #  download_img(self,img_el,chapter_url,file_name,dl_path):
                    self.download_img(img_el=img,chapter_url=c,file_name=i,dl_path=dl_path)
                except:
                    print(f"error in {img.attrs['alt']}")

# ---------- TEST --------- 
# if __name__ == "__main__":
#     n = NetTruyenScraw(name="The_gamer", url="http://www.nettruyen.com/truyen-tranh/the-gioi-game-thu-4478")
#     n.run(chapter_start=1, total=3)
#     tog = NetTruyenScraw( name='TOG',url ="http://www.nettruyen.com/truyen-tranh/cuoc-chien-trong-toa-thap")
#     tog.run(chapter_start=1,total=22)
    

# 
# ----------- SAMPLE CODE ----------
# 

# manga_name = "The_gamer"
# chapter = "126"
# url = "http://www.nettruyen.com/truyen-tranh/the-gioi-game-thu/chap-126/257378"
# session = HTMLSession()
# r = session.get(url)

# chapter_class = r.html.find(".page-chapter")
# chapter_img = chapter_class[0].find('img')
# img_url = chapter_img[0].attrs['src']

# headers = {
#     "Referer": url # Chapter URL
# }
# filename = img_url.split('/')[-1]
# r = requests.get(img_url, stream = True, headers=headers)
# # Check if the image was retrieved successfully
# print(r.status_code)
# if r.status_code == 200:
#     # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
#     r.raw.decode_content = True
#     # Open a local file with wb ( write binary ) permission.
#     img_path = os.path.join(INPUT_DIR,manga_name,chapter)
#     print(img_path)
#     os.makedirs(img_path, exist_ok=True)
#     img_dir = os.path.join(img_path, filename)
#     with open(img_dir,'wb') as f:
#         shutil.copyfileobj(r.raw, f)
#     print('Image sucessfully Downloaded: ',filename)
# else:
#     print('Image Couldn\'t be retreived')
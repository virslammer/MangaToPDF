import sys,shutil
from scraw_manga import NetTruyenScraw
from pdf import MangaToPDF
from config import INPUT_DIR

def help_message():
    print("Usage:python -m main.py [name] [url] [start] [total] [make_pdf[default:True]]")
    print("name: name of output file")
    print("url: a valid url of a manga from Nettruyen.com , exp : http://www.nettruyen.com/truyen-tranh/cuoc-chien-trong-toa-thap-55201")
    print("start: chapter start")
    print("total: total chapter from start")

def clear_input():
    shutil.rmtree(INPUT_DIR, ignore_errors=True)

def main(name="",url=None, start=0, total=0, make_pdf=True):

    manga = NetTruyenScraw(name=name, url= url)
    manga.run(chapter_start=start,total=total)
    if make_pdf:

        m = MangaToPDF(manga_name=name)
        m.convert_to_pdf()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        name=""
        url=None
        start=0
        total=0

        try:
            name = sys.argv[1]
            url = sys.argv[2]
            start = int(sys.argv[3])
            total = int(sys.argv[4])
            
        except:
            print("Invalid command")
            help_message()
        main(name,url,start,total)
        clear_input()
    else:
        help_message()



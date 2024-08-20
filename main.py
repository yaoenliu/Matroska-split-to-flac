import subprocess
import xml.etree.ElementTree as ET
import ffmpeg
import os

filename = "test.mka"
output_path = filename.split(".")[0]
# make directory
os.makedirs (output_path, exist_ok=True)



result = subprocess.run(['mkvextract', 'chapters', filename], stdout=subprocess.PIPE, text=True, encoding='UTF-8')

text = result.stdout
root = ET.fromstring(text)
idx = 1
for ele in root.iter('ChapterAtom'):
    name = ele.find('ChapterDisplay').find('ChapterString').text
    stime = ele.find('ChapterTimeStart').text
    etime = ele.find('ChapterTimeEnd').text
    # export to ffmpeg as flac
    ffmpeg.input("test.mka", ss=stime, to=etime).output(output_path+"\\"+str(idx).zfill(2)+". "+name+".flac").run()
    idx += 1  
    
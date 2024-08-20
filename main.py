import subprocess
import xml.etree.ElementTree as ET
import ffmpeg
import os
import sys

if len(sys.argv) < 2:
    print("Usage: python main.py <filename>")
    sys.exit()

filepath = sys.argv[1]
filename = filepath[filepath.rfind("\\")+1:filepath.rfind(".")]
if filename == "":
    filename = filepath.split(".")[0]

# make directory
os.makedirs (filename, exist_ok=True)

result = subprocess.run(['mkvextract', 'chapters', filepath], stdout=subprocess.PIPE, text=True, encoding='UTF-8')

text = result.stdout
root = ET.fromstring(text)
idx = 1
for ele in root.iter('ChapterAtom'):
    name = ele.find('ChapterDisplay').find('ChapterString').text
    stime = ele.find('ChapterTimeStart').text
    etime = ele.find('ChapterTimeEnd').text
    # export to ffmpeg as flac
    ffmpeg.input("test.mka", ss=stime, to=etime).output(filename+"\\"+str(idx).zfill(2)+". "+name+".flac").run()
    idx += 1
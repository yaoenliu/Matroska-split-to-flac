import subprocess
import ffmpeg
import os
import sys

import ffmpeg.stream

if len(sys.argv) < 2:
    print("Usage: python main.py <filename>")
    sys.exit()

filepath = sys.argv[1]
filename = filepath[filepath.rfind("\\")+1:filepath.rfind(".")]
if filename == "":
    filename = filepath.split(".")[0]

# make directory
os.makedirs (filename, exist_ok=True)

result = subprocess.run(['mkvextract', 'chapters', filepath,'-s'], stdout=subprocess.PIPE, text=True, encoding='UTF-8')

lines = result.stdout.split("\n")
start_time = []
name = []
for i in range(0, len(lines)-1, 2):
    print(lines[i], lines[i+1])
    start_time.append(lines[i].split("=")[1])
    name.append(lines[i+1].split("=")[1])

for i in range(len(start_time)):
    stime = start_time[i]
    etime = start_time[i+1] if i+1 < len(start_time) else None
    cname = name[i]
    idx = i+1
    print(stime, etime, cname)
    if etime != None:
        ffmpeg.input(filepath, ss=stime, to=etime, vn=None).output(filename+"\\"+str(idx).zfill(2)+". "+cname+".flac").run()
    else:
        ffmpeg.input(filepath, ss=stime, vn=None).output(filename+"\\"+str(idx).zfill(2)+". "+cname+".flac").run()
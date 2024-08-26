import subprocess
import ffmpeg
import os
import sys
import re
from tqdm import tqdm
from time import sleep

def sanitize_chapter_name(name):
    # Windows not allowed characters：\/:*?"<>|
    new_name = re.sub(r'[\\/:*?"<>|]', '_', name)
    if new_name != name:
        print("Sanitize chapter name: ", name, " -> ", new_name)
    return new_name

if len(sys.argv) < 2:
    print("Usage: python main.py <filename>")
    sys.exit()

filepath = sys.argv[1]
filename = filepath[filepath.rfind("\\")+1:filepath.rfind(".")]
if filename == "":
    filename = filepath.split(".")[0]

result = subprocess.run(['mkvextract', 'chapters', filepath,'-s'], stdout=subprocess.PIPE, text=True, encoding='UTF-8')

if result.returncode != 0:
    print("Error code: ", result.returncode)
    sys.exit()

# make directory
os.makedirs (filename, exist_ok=True)

lines = result.stdout.split("\n")
start_time = []
name = []
for i in range(0, len(lines)-1, 2):
    print(lines[i], lines[i+1])
    start_time.append(lines[i].split("=")[1])
    name.append(lines[i+1].split("=")[1])

p_list = []

# for i in range(15):
for i in range(len(start_time)):
    stime = start_time[i]
    etime = start_time[i+1] if i+1 < len(start_time) else None
    cname = sanitize_chapter_name(name[i])
    idx = i+1
    print(stime, etime, cname)
    if etime != None:
        p = ffmpeg.input(filepath, ss=stime, to=etime, vn=None).output(filename+"\\"+str(idx).zfill(2)+". "+cname+".flac").overwrite_output().run_async(pipe_stderr =True)
    else:
        p = ffmpeg.input(filepath, ss=stime, vn=None).output(filename+"\\"+str(idx).zfill(2)+". "+cname+".flac").overwrite_output().run_async(pipe_stderr =True)
    p_list.append(p)
    p.stderr.close()

i = len (p_list)

for r in tqdm(range(i)):
    while True:
        flag = False
        for n in p_list:
            if n.poll() != None:
                p_list.remove(n)
                flag = True
                break
        if flag:
            break
        else:
            sleep(0.1)

print("All done!")

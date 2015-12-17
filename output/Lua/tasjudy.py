import os
import re
import time
import datetime
from multiprocessing import Pool

bizhawkPath = "C:\\Users\\phil\\NES\\BizHawkMaster\\output\\EmuHawk.exe"
romPath = "C:\\Users\\phil\\NES\\games\\streemerz-v02.nes"
moviePath = "C:\\Users\\phil\\NES\\Scripts\\movies\\bk2\\"

def emu(arg):
    time.sleep(arg) #make sure the processes are offset so they don't easily collide to start with.
    while 1:
        currentList = os.listdir(moviePath)
        for file in currentList:
            hash_regex = re.search("(.*)\.bk2", file)
            if hash_regex:
                hash = hash_regex.group(1)
                if not os.path.exists(moviePath + hash):
                    print("%d creating " % (arg) + hash)
                    claim = open(moviePath + hash, "w")
                    claim.close()
                    ret = os.system(bizhawkPath + " " + romPath + " --movie=" + moviePath + file)
                    print("%d judged as %d-" % (arg, ret) + hash)
                    judged = open(moviePath + str(ret) + "-" + hash, "w")
                    judged.close()
        print("Ending %d with %d at %s" % (arg,ret,datetime.datetime.now().time()))
        break
    
if __name__ == '__main__':
    print("Starting at %s" % datetime.datetime.now().time())
    p = Pool(processes=4)
    p.map(emu,range(4))
    print("Ending parent at %s" % datetime.datetime.now().time())    


import os
import re
import time
import datetime
from multiprocessing import Pool

# About this script:
# This script was created for the purposes of judging a speed TAS competition. The expectation is that there is a folder (presumably mounted) which contains bizhawk movie files, a folder named 'claims' and a folder named 'results'. The movie files must be uniquely named (presumably with hashes).
# Because there is confusion in paths otherwise the script should be run from the bizhawk ouput folder (The one containing "EmuHawk.exe"). The movie folder must be mounted to a subdirectory of that same folder so that a relative path can be used (since it needs to be used by both this python script and the windows executable which have different bases).
# This script will create a number of threads (as defined by you at the top of this script). Each thread will constantly compare the hashes in the movie folder to the hashes in the 'claims' folder
# For any movie that has not been claimed (does not have an emtpy file with the hash name in the 'claims' folder) this script will create a file in the 'claims' folder thereby claiming the entry for judging. It will then invoke bizhawk through crossover providing the movie to be judged. Bizhawk will judge the movie and put the results in the 'results' folder. Once judged the 'results' folder will create a file named [end frame]-hash which contains the movie header. Note that if the movie is disqualified the end frame will be -1. It is worth noting that I have created a build of bizhawk that does the judging and produces the results from within the C# source, but this could also be done in a Lua script with a release version of Bizhawk. I made this choice for performance reasons.
# There are break statements in the loop for testing purposes, but I would note that without them I'm not sure of a clean way to exit the program so you may need to look up the process in another command line and kill it manually.
# Lastly the design is set up to be parallelized, you could run multiple instances or VMs that have mounted the same movie folder. They will watch the folder and judge anything there making use of the 'claims' folder as a sort of arbitrator.

# Quick start guide:
# 1. Put your custom build of bizhawk in a folder in your crossover bottle. (Alternatively if you were using Lua you would need to make sure you had the appropriate script auto-loaded).
# 2. create a sub-folder and mount the directory with the movie files there.
# 3. in the movie folder create sub-folders 'claims' and 'results' if they do not already exist.
# 4. modify the bizhawk path, rom path, movie path, wine path, and thread count as appropriate. Note that the movie path must be relative
# 5. cd to the dir you put bizhawk in and run the script, then wait for your results.

bizhawkPath = "EmuHawk.exe"
romPath = "/home/pgrimsrud/Downloads/streemerz-v02.nes"
moviePath = "movies/bk2/"
winePath = "/opt/cxoffice/bin/wine --bottle=\"Test\" --cx-app "
numberOfThreads = 2

def emu(arg):
    time.sleep(arg) #make sure the processes are offset so they don't easily collide to start with.
    while 1:
        ret = -1
        currentList = os.listdir(moviePath)
        for file in currentList:
            hash_regex = re.search("(.*)\.bk2", file)
            if hash_regex:
                hash = hash_regex.group(1)
                if not os.path.exists(moviePath + "claims" + os.sep + hash):
                    print("%d creating " % (arg) + hash)
                    claim = open(moviePath + "claims" + os.sep + hash, "w")
                    claim.close()
                    print(winePath + bizhawkPath + " " + romPath + " --movie=\"" + moviePath + file + "\"")
                    ret = os.system(winePath + bizhawkPath + " " + romPath + " --movie=" + moviePath + file)
                    print("%d judged as %d-" % (arg, ret) + hash)
                    # This is commented out, but you would use it to write out the results if you judged in Lua and returned the frame count as an exit code.
                    #judged = open(moviePath + str(ret) + "-" + hash, "w")
                    #judged.close()
                    # The break here is for testing purposes
                    #break
        print("Ending %d with %d at %s" % (arg,ret,datetime.datetime.now().time()))
        # The break here is for testing purposes
        #break
    
if __name__ == '__main__':
    print("Starting at %s" % datetime.datetime.now().time())
    p = Pool(processes=numberOfThreads)
    p.map(emu,range(numberOfThreads))
    print("Ending parent at %s" % datetime.datetime.now().time())    


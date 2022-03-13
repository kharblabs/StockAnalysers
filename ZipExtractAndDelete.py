import os
import time
import datetime
import zipfile

#returns month number from string (full name)
def getMonthNum(s):
    
    n=datetime.datetime.strptime(s, '%B').month
    if(n<10):
        return '0'+str(n)
    else:
        return  str(n)
#return folders

def fast_scandir(dirname):
    subfolders= [f.path for f in os.scandir(dirname) if f.is_dir()]
    for dirname in list(subfolders):
        subfolders.extend(fast_scandir(dirname))
    return subfolders
    
allSubFolds=fast_scandir(os.getcwd())
for fold in allSubFolds:        
    os.chdir(fold)
    for file in os.listdir(fold):   # get the list of files
        print(os.getcwd()+file)
        if zipfile.is_zipfile(file): # if it is a zipfile, extract it
            print("Found")
            with zipfile.ZipFile(file) as item: # treat the file as a zip
                item.extractall()  # extract it in the working directory
    for item in os.listdir(fold):
        if item.endswith(".zip"):
            os.remove( os.path.join( fold, item ) )  

input("Press Enter to continue...")
                
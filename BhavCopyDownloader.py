import os
import datetime
import requests
def download(url: str, dest_folder: str , name :str):
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)  # create folder if it does not exist

    filename = name # be careful with file names
    file_path = os.path.join(dest_folder, filename)

    r = requests.get(url, stream=True)
    if r.ok:
        print("                         saving to", os.path.abspath(file_path))
        with open(file_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024 * 8):
                if chunk:
                    f.write(chunk)
                    f.flush()
                    os.fsync(f.fileno())
    else:  # HTTP status code 4XX/5XX
        print("Download failed: status code {}\n{}".format(r.status_code, r.text))

begin = datetime.date(2022,1,1 )
end = datetime.date(2022, 2, 27)
string_q="https://www1.nseindia.com/archives/equities/bhavcopy/pr/PR100811.zip"
next_day = begin
while True:
    if next_day > end:
        break
    if(next_day.weekday()<5):  
        
        string_url="https://www1.nseindia.com/content/historical/DERIVATIVES/"+str(next_day.strftime("%Y"))+"/"+str(next_day.strftime("%b")).upper()+"/fo"+ str(next_day.strftime("%d%b%Y")).upper()+"bhav.csv.zip"
        print( next_day.strftime("%d %B %Y"))
        download(string_url,dest_folder="BhavDownloads",name= str(next_day.strftime("%d%m%Y")).upper()+".csv.zip")
    next_day += datetime.timedelta(days=1)
wDir1 = os.getcwd()
wd=wDir1+'\BhavDownloads'
os.chdir(wd)
for file in os.listdir(wd):   # get the list of files
    print(os.getcwd()+file)
    if zipfile.is_zipfile(file): # if it is a zipfile, extract it
        print("Found")
        with zipfile.ZipFile(file) as item: # treat the file as a zip
               item.extractall()  # extract it in the working directory

#deletes Zips               
for item in os.listdir(wd):
    if item.endswith(".zip"):
        os.remove( os.path.join( wd, item ) )   
#name formatting        
for fileName in os.listdir("."):
    os.rename(fileName, fileName.replace("fo", ""))
for fileName in os.listdir("."):
    os.rename(fileName, fileName.replace("bhav", ""))               
#Changes Name
for fileName in os.listdir("."):
    oldNametime= datetime.datetime.strptime(fileName.replace(".csv",""), '%d%b%Y')
    newN=oldNametime.strftime('%Y-%m-%d')+'.csv'
    os.rename(fileName,newN)    
os.chdir(wDir1)    

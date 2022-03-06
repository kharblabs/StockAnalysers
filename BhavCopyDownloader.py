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
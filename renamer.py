import os
for fileName in os.listdir("."):
    try:
        if 'WKCE ' in fileName:
            f2=fileName.replace("WKCE ","WKNIFTY")
            f2=f2.replace(".csv","CE.csv")
            f2=f2.replace(" ","")
            os.rename(fileName, f2)
            print(f2)
        
        if 'WKPE ' in fileName:
            f2=fileName.replace("WKPE ","WKNIFTY")
            f2=f2.replace(".csv","PE.csv")
            f2=f2.replace(" ","")
            os.rename(fileName, f2)
            print(f2)
        if '11APR19' in fileName:
            f2=fileName.replace("11APR19","")
            os.rename(fileName, f2)
            print(f2)
      
        if '18APR19' in fileName:
            f2=fileName.replace("18APR19","")
            os.rename(fileName, f2)
            print(f2)
        if '25APR19' in fileName:
            f2=fileName.replace("25APR19","")
            os.rename(fileName, f2)
            print(f2)
        
        if '20MAR19' in fileName:
            f2=fileName.replace("20MAR19","")
            os.rename(fileName, f2)
            print(f2)
        if '14FEB19' in fileName:
            f2=fileName.replace("14FEB19","")
            os.rename(fileName, f2)
            print(f2)
        if '21FEB19' in fileName:
            f2=fileName.replace("21FEB19","")
            os.rename(fileName, f2)
            print(f2)
        
        if len(fileName) > 27 :
            f2=fileName[:15]+fileName[22:]
            print(fileName)
            print(f2)
            os.rename(fileName, f2)
    except Exception as e:
        print(e)
       

input("Press Enter to continue...")

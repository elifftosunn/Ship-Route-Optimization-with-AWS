import pandas as pd
import glob 
import pymongo
import re

regex = "[0-9]{8}\-[0-9]+"
def dataConcat(regex, files):
    # all_data = pd.DataFrame()
    all_data = []
    for file in glob.glob(files):
        time = re.findall(regex,file)       
        df = pd.read_csv(file,sep=",")
        for i in range(len(df)):
            time = ''.join(str(e) for e in time)
            df.loc[i,"time"] = time
        df["time"] = pd.to_datetime(df["time"]) # YYYY-mm-dd HH:MM:ss
        all_data.append(df)
        # all_data.from_records(df)

    # all_data = pd.concat(df,all_data.from_records(list(df)))
    all_data = pd.concat(all_data)

    all_data = all_data.drop("Unnamed: 0",axis=1)
    all_data.to_csv("datas/mongoData/concatDatas/concatData10.csv",index=False)
    return all_data

all_data = dataConcat(regex, "datas/11_1828-13_0939/*.csv")

def createDataFrame(FeatureResult):
    shipNameList, latList, lonList, cogList, sogList, headingList, typeList, timeList = [],[],[],[],[],[],[],[]
    for feature in FeatureResult:
        shipNameList.append(feature["ship_name"])
        latList.append(feature["lat"])
        lonList.append(feature["lon"])
        cogList.append(feature["cog"])
        sogList.append(feature["sog"])
        headingList.append(feature["heading"])
        typeList.append(feature["type"])
        timeList.append(feature["time"])
    shipNameDf = pd.DataFrame(shipNameList, columns=["ship_name"])
    latDf = pd.DataFrame(latList, columns=["lat"])
    lonDf = pd.DataFrame(lonList, columns=["lon"])
    cogDf = pd.DataFrame(cogList, columns=["cog"])
    sogDf = pd.DataFrame(sogList, columns=["sog"])
    headingDf = pd.DataFrame(headingList, columns=["heading"])
    typeDf = pd.DataFrame(typeList, columns=["type"])
    timeDf = pd.DataFrame(timeList, columns=["time"])
    
    resultDf = pd.concat([shipNameDf,latDf,
                           lonDf,cogDf,sogDf,headingDf,
                           typeDf, timeDf],axis=1)
    return resultDf

def mongo():
    client = pymongo.MongoClient(host = "localhost", port = 27017)    
    marineDB = client["Marine"]
    shipCollection = marineDB["Ship"]
    # for col in shipCollection.find():
    #     print(col,"\n")
    query = {"$and":[{"$or":[{"type":"Tankers"},{"type":"Cargo"}]},{"$and":[{"cog":{"$gte":60}},{"cog":{"$lte":200}}]},{"sog":{"$gt":0}}]}  
    FeatureResult = shipCollection.find(query)
    resultDf = createDataFrame(FeatureResult)
    #for line in shipCollection.find(query):
        #print(line,"\n")
    return resultDf
resultDf = mongo()
resultDf.to_csv("datas/mongoData/ResultDatas/resultData10.csv", index=False)

def resultPush():
    dataList = []
    for file in glob.glob("datas/mongoData/ResultDatas/*.csv"):
        df = pd.read_csv(file)
        dataList.append(df)
        
    df = pd.concat(dataList)
    df.to_csv("/home/eliftosun/Desktop/marine.csv",index=False)

resultPush()






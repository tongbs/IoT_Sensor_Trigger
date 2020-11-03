# 取得空氣品質專案的值
import requests,json

# device對照表
'''
24448091106 台北校區
24448147255 六家校區-東南側六家古厝面
24448224796 六家校區-東北側六家一路面
24449647874 六家校區-大門口    (default)
24449735910 光復校區-綜合一館
24449803581 光復校區-基礎科學教學研究大樓
24449953693 博愛校區-竹銘館後門
24450049144 博愛校區-竹銘館大門
24450111167 六家校區-西北側自強南路面
24450246464 光復校區-電子資訊研究大樓
24450355457 台南校區-奇美樓南側
24450450732 博愛校區-學生活動中心
24450576158 博愛校區-實驗一館
24450671517 光復校區-人社一館
24450776164 光復校區-浩然圖書資訊中心
24450808307 台南校區-奇美樓北側
'''

def get_air_data(device = 24450111167):
    rD = {}
    url = "https://iot.cht.com.tw/iot/v1/device/" + str(device)
    headers = {"CK": "PK0154ZPXFWEBC2Y73"}
    r = requests.get(url, headers=headers, timeout=5.0)
    rText = json.loads(r.text)
    #print(rText)
    #print(AIoT_deviceL["name"], AIoT_deviceL["id"])
    rD["name"] = rText["name"]
    rD["lat"] = rText["lat"]
    rD["lon"] = rText["lon"]
    url = "https://iot.cht.com.tw/iot/v1/device/"+str(device)+"/rawdata"
    r = requests.get(url, headers=headers, timeout=5.0)
    rText = json.loads(r.text)
    #print(rText)
    data = {"pm2.5" : rText[0]["value"][0], 
            "pm10" : rText[1]["value"][0], 
           }
    iftoohigh= {"pm2.5" : rText[2]["value"][0], 
                "pm10" : rText[3]["value"][0], 
               }
    rD["value"] = data
    rD["if_too_high"] = iftoohigh
    return rD
'''
return data example : {
 'name': '六家校區-西北側自強南路面', 
 'lat': 24.812641, 
 'lon': 121.022958, 
 'value': {'pm2.5': '13', 'pm10': '9'},     # int
 'if_too_high': {'pm2.5': '0', 'pm10': '0'} # 0 or 1
 }
'''
# default為六家校區-西北側自強南路面
#result = get_air_data()
#print(result)
# 或是填入上面的代號
result = get_air_data(24448091106)
print(result)
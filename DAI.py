import time, DAN, requests, random, json

ServerURL = 'https://test.iottalk.tw' #with no secure connection
#ServerURL = 'https://DomainName' #with SSL connection
Reg_addr = "IoTContestSensor" #if None, Reg_addr = MAC address

DAN.profile['dm_name']='IoTContest'
DAN.profile['df_list']=['IoTWaring']
DAN.profile['d_name']= "IoTContest" # None for autoNaming
DAN.device_registration_with_retry(ServerURL, Reg_addr)


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
result = get_air_data(24448091106)
print(result)
'''
push_list = []


while True:
    try:
        time.sleep(5)
        print(len(push_list))
    #Push data to a device feature called "Dummy_Sensor"
        result = get_air_data(24450111167)
        print(result)
        warning_string = "空氣品質不佳"
        print("push data: ",result['lat'])
        print(result['lon'])
        print(result['name'])
        print(int(result['if_too_high']['pm2.5']))
        print(warning_string)
        map_push_flag = 0  # increase obstacle(warning) on map
        map_del_flag = 1   # delete obstacle(warning) on map
        if len(push_list)==0 and int(result['if_too_high']['pm2.5'])==1:
            push_list.append([result['lat'], result['lon'], result['name'], int(result['if_too_high']['pm2.5']), warning_string])
            DAN.push ('IoTWaring', result['lat'], result['lon'], result['name'], map_push_flag, warning_string)
        if int(result['if_too_high']['pm2.5'])==1 and len(push_list)==0:
            DAN.push ('IoTWaring', result['lat'], result['lon'], result['name'], map_del_flag, warning_string)
            push_list.clear()

    except Exception as e:
        print(e)
        if str(e).find('mac_addr not found:') != -1:
            print('Reg_addr is not found. Try to re-register...')
            DAN.device_registration_with_retry(ServerURL, Reg_addr)
        else:
            print('Connection failed due to unknow reasons.')
            time.sleep(1)    

    time.sleep(30)


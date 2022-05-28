from crawler import get_house_pirce_raw_data_from_url

import json

target_addresses = [
    '北投段', '北投堡段', '北投埔段', '頂茄荖段', '光華段', '青宅段', '新埔段', '新興段', '新光段',
    '新豐段', '保安段', '中興段', '上林段', '和平段', '將軍段', '頂園段']

def display_message(records):
    text = ''
    for index, record in enumerate(records):
        text += str(index+1) + '. \n交易日期: ' + record[1][0] + '\n地址: ' + record[0] + '\n總價: ' + str(int(record[1][2].replace(',', ''))/10000) + ' 萬\n總面積: ' + record[1][1] + '(坪)\n\n'   
        if len(text) >= 250: break
    return text

def load_old_data():
    with open('/app/old_data.json', encoding="utf8") as f:
        old_data = json.load(f)

    print('成功: load_old_data')
    return old_data


def handle_house_price_data():
    new_data = get_house_pirce_raw_data_from_url()
    old_data = load_old_data()
    # print('type old data', type(old_data)) # list
    # print(old_data)
    new_records = {}

    cnt = 0
    for i in range(len(new_data)):
        deal = new_data[i] # 這是一個 dict
        # print(type(deal))
        if deal['a'][:3] in target_addresses or deal['a'][:4] in target_addresses:
            # 比對該筆資料是否是新登錄的交易
            if {'AA11': '住', 'AA12': '', 'a': '中興段00680000地號#中興段68地號', 'b': '', 'bn': '', 'bs': '', 'city': 'M', 'commid': '', 'cp': '', 'e': '110/05/19', 'el': '無', 'es': '', 'f': '', 'fi': '0', 'g': '', 'id': '507', 'j': '1', 'k': '0', 'l': '0', 'lat': 23.968084085594217, 'lon': 120.68208760119431, 'm': '無', 'mark': '', 'msg': '總價/總面積', 'note': '', 'p': '101,864', 'pimg': 'bt_A.png', 'pu': '', 'punit': '1', 'r': 10, 'reid': '', 's': '26.02', 'sq': 'xlITTw6HRxRNVlIJ1AP5ir2T4M+DwCOTKxl3v/Pat5Q=', 't': '土地', 'tp': '2,650,000', 'tunit': '1', 'twn': 'M03', 'type': 'Biz', 'unit': '2', 'v': ''} not in old_data:
                print('錯誤!') 
            if {"AA11": "住", "AA12": "", "a": "中興段00680000地號#中興段68地號", "b": "", "bn": "", "bs": "", "city": "M", "commid": "", "cp": "", "e": "110/05/19", "el": "無", "es": "", "f": "", "fi": "0", "g": "", "id": "507", "j": "1", "k": "0", "l": "0", "lat": 23.968084085594217, "lon": 120.68208760119431, "m": "無", "mark": "", "msg": "總價/總面積", "note": "", "p": "101,864", "pimg": "bt_A.png", "pu": "", "punit": "1", "r": 10, "reid": "", "s": "26.02", "sq": "TEeNgLxSCN79UkSMenCGTGfuvc+Gt7P/GM2c+1hN+zE=", "t": "土地", "tp": "2,650,000", "tunit": "1", "twn": "M03", "type": "Biz", "unit": "2", "v": ""} != {'AA11': '住', 'AA12': '', 'a': '中興段00680000地號#中興段68地號', 'b': '', 'bn': '', 'bs': '', 'city': 'M', 'commid': '', 'cp': '', 'e': '110/05/19', 'el': '無', 'es': '', 'f': '', 'fi': '0', 'g': '', 'id': '507', 'j': '1', 'k': '0', 'l': '0', 'lat': 23.968084085594217, 'lon': 120.68208760119431, 'm': '無', 'mark': '', 'msg': '總價/總面積', 'note': '', 'p': '101,864', 'pimg': 'bt_A.png', 'pu': '', 'punit': '1', 'r': 10, 'reid': '', 's': '26.02', 'sq': 'xlITTw6HRxRNVlIJ1AP5ir2T4M+DwCOTKxl3v/Pat5Q=', 't': '土地', 'tp': '2,650,000', 'tunit': '1', 'twn': 'M03', 'type': 'Biz', 'unit': '2', 'v': ''}:
                print('刷新三關!')
            if deal not in old_data:
                print('一筆新資料: ', deal)
                cnt += 1
                start_index = deal['a'].find('#') + 1 
                new_records[deal['a'][start_index::]] = [deal['e'], deal['s'], deal['tp']]

    result = sorted(new_records.items(), key=lambda x:x[1], reverse=True)
    print(cnt ,' 成功: handle_hosue_price_data')
    return display_message(result)

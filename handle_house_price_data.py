from crawler import get_house_pirce_raw_data_from_url

import json

target_addresses = [
    '北投段', '北投堡段', '北投埔段', '頂茄荖段', '光華段', '青宅段', '新埔段', '新興段', '新光段',
    '新豐段', '保安段', '中興段', '上林段', '和平段', '將軍段', '頂園段']

def display_message(records):
    text = ''
    for index, record in enumerate(records):
        text += str(index+1) + '. \n交易日期: ' + record[1][0] + '\n地址: ' + record[0] + '\n總價: ' + str(int(record[1][2].replace(',', ''))/10000) + ' 萬\n總面積: ' + record[1][1] + '\n\n'   

    return text

def load_old_data():
    with open('/app/old_data.json') as f:
        old_data = json.load(f)

    # print(old_data)
    print('成功: load_data')
    return old_data

# def is_new_deal(record):
#     return record

def handle_house_price_data():
    new_data = get_house_pirce_raw_data_from_url()
    old_data = load_old_data()

    new_records = {}

    for i in range(len(new_data)):
        deal = new_data[i] # 這是一個 dict

        if deal['a'][:3] in target_addresses or deal['a'][:4] in target_addresses:
            # 比對該筆資料是否是新登錄的交易
            if deal not in old_data:
                start_index = deal['a'].find('#') + 1 
                new_records[deal['a'][start_index::]] = [deal['e'], deal['s'], deal['tp']]

    result = sorted(new_records.items(), key=lambda x:x[1], reverse=True)[:5]
    print('成功: handle_hosue_price_data')
    return display_message(result)

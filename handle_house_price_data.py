from crawler import get_house_pirce_raw_data_from_url

import json

target_addresses = [
    '北投段', '北投堡段', '北投埔段', '頂茄荖段', '光華段', '青宅段', '新埔段', '新興段', '新光段',
    '新豐段', '保安段', '中興段', '上林段', '和平段', '將軍段', '頂園段']

def display_message(records):
    sorted_records = sorted(records.items(), key=lambda x:x[1][0], reverse=True)

    text = ''
    for index, record in enumerate(sorted_records):
        address = record[0].split('#')[1]
        date = record[1][0]
        area = record[1][1]
        price = str(int(record[1][2].replace(',', ''))/10000)

        text += str(index+1) + '. \n交易日期: ' + date + '\n地址: ' + address + '\n總價: ' + price + ' 萬\n總面積: ' + area + '(坪)\n\n'   
        if len(text) >= 250: break
        
    return text

def load_old_data(file_path):
    with open(file_path, encoding="utf8") as f:
        old_data = json.load(f)

    print('成功載入舊資料，總共有 ', len(old_data), ' 筆資料!')
    return old_data

# def handle_house_price_raw_data():
#     raw_data = get_house_pirce_raw_data_from_url()

#     records = {}
#     for deal in raw_data:
#         if deal['a'][:3] in target_addresses or deal['a'][:4] in target_addresses:
#             records[(deal['e'], deal['a'])] = [deal['s'], deal['tp']]

#     print('總共有 ', len(records), ' 筆資料')
#     print('第一筆資料為: ', records[0])
#     return records       


def handle_house_price_data():
    new_data = get_house_pirce_raw_data_from_url()
    old_data = load_old_data('/app/old_data.json')

    new_records = {}

    cnt = 0
    for deal in new_data:
        if deal['a'][:3] in target_addresses or deal['a'][:4] in target_addresses:
            if old_data.get(deal['e']+deal['a']) == None or old_data.get(deal['a'])[0] != deal['e']:
                # 表示這是沒出現在交易紀錄中的地段 或是 這個地段交易過但交易日期不同 
                cnt += 1
                new_records[deal['e']+deal['a']] = [deal['e'], deal['s'], deal['tp']]

    print('新增 ', len(new_records), ' 筆交易紀錄!')
    return display_message(new_records)
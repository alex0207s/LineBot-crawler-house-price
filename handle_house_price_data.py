from crawler import get_house_pirce_raw_data_from_url
from app import line_bot_api, user_list
from linebot.models import TextSendMessage
# import json, configparser

# config = configparser.ConfigParser()
# config.read('config.ini')

target_addresses = [
    '北投段', '北投堡段', '北投埔段', '頂茄荖段', '光華段', '青宅段', '新埔段', '新興段', '新光段',
    '新豐段', '保安段', '中興段', '上林段', '和平段', '將軍段', '頂園段']

def display_message(records, show_old = True):
    sorted_records = sorted(records.items(), key=lambda x:x[1][0], reverse=True)

    if show_old:
        text = ''
    else:
        text = '找到 ' + str(len(records)) + ' 筆新的資料\n'

    for index, record in enumerate(sorted_records):
        address = record[0].split('#')[1]
        date = record[1][0]
        area = record[1][1]
        price = str(int(record[1][2].replace(',', ''))/10000)

        text += str(index+1) + '. \n交易日期: ' + date + '\n地址: ' + address + '\n總價: ' + price + ' 萬\n總面積: ' + area + '(坪)\n\n'   
        if len(text) >= 280: break
        
    return text

def save_new_data(file_path, records):
    with open(file_path, 'w', encoding='utf8') as f:
        json.dump(records, f, ensure_ascii=False)

def load_old_data(file_path):
    with open(file_path, encoding='utf8') as f:
        old_data = json.load(f)

    print('成功載入舊資料，總共有 ', len(old_data), ' 筆資料!')
    return old_data


def get_house_price_data():
    raw_data = get_house_pirce_raw_data_from_url()
    old_data = load_old_data('/app/old_data.json')

    new_records = {}

    cnt = 0
    for deal in raw_data:
        if deal['a'][:3] in target_addresses or deal['a'][:4] in target_addresses:
            if old_data.get(deal['e'] + deal['a']) == None or old_data.get(deal['e'] + deal['a'])[0] != deal['e']:
                # 表示這是沒出現在交易紀錄中的地段 或是 這個地段交易過但交易日期不同 
                cnt += 1
                new_records[deal['e']+deal['a']] = [deal['e'], deal['s'], deal['tp']]

    print('新增 ', len(new_records), ' 筆交易紀錄!')
    if len(new_records) == 0:
        return ''
    else:
        new_data = {**old_data, **new_records}
        save_new_data('/app/old_data.json', new_data)
        return display_message(new_records, False)


if __name__ == '__main__':
    print('成功執行 main 主程式')

    text = get_house_price_data()
    if text == '':
        print('目前尚未抓到新的交易紀錄')
    else:
        line_bot_api.push_message(user_list, TextSendMessage(text=text))

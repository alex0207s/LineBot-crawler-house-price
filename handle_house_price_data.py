target_address = [
    '北投段', '北投堡段', '北投埔段', '頂茄荖段', '光華段', '青宅段', '新埔段', '新興段', '新光段',
    '新豐段', '保安段', '中興段', '上林段', '和平段', '將軍段', '頂園段']

def display_message(records):
    text = ''
    for index, record in enumerate(records):
        text += str(index) + '. \n交易日期: ' + record[1][0] + '\n地址: ' + record[0] + '\n總價: ' + str(int(record[1][2].replace(',', ''))/10000) + ' 萬\n總面積: ' + record[1][1] + '\n\n'   

    return text

def handle_house_price_data(raw_data):
    records = {}

    for i in range(len(raw_data)):
        deal = raw_data[i]
        if deal['a'][:3] in target_address or deal['a'][:4] in target_address:
            start_index = deal['a'].find('#') + 1 
            records[deal['a'][start_index::]] = [deal['e'], deal['s'], deal['tp']]

    result = sorted(records.items(), key=lambda x:x[1], reverse=True)[:6]
    return display_message(result)

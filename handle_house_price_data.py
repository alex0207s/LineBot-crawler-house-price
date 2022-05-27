target_address = [
    '北投段', '北投堡段', '北投埔段', '頂茄荖段', '光華段', '青宅段', '新埔段', '新興段', '新光段',
    '新豐段', '保安段', '中興段', '上林段', '和平段', '將軍段', '頂園段']

def handle_house_price_data(raw_data):
    house = {"交易日期":[], "地址":[], "總價":[], "總面積":[]}

    for i in range(len(raw_data)):
        deal = raw_data[i]
        if deal['a'][:3] in target_address or deal['a'][:4] in target_address:
            start_index = deal['a'].find('#') + 1 
            house["交易日期"].append(deal['e'])
            house["總面積"].append(deal['s'])
            house["地址"].append(deal['a'][start_index::])
            house["總價"].append(deal['tp'])

    text = ""
    for i in range(1,6):
        text += str(i) + house['交易日期'][i] + ' ' + house['地址'][i] + ' ' + house['總價'][i] + ' ' + house['總面積'][i] + '\n\n'
    return text

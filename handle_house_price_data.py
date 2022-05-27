target_address = [
    '北投段', '北投堡段', '北投埔段', '頂茄荖段', '光華段', '青宅段', '新埔段', '新興段', '新光段',
    '新豐段', '保安段', '中興段', '上林段', '和平段', '將軍段', '頂園段']

def display_message(records, num=6):
    text = ''
    for record in records.items()[:num]:
        text += '交易日期: ' + record[1][0] + '\n地址: ' + record[0] + '\n總價: ' + str(int(record[1][2].replace(',', ''))/10000) + ' 萬\n總面積: ' + record[1][1] + '\n\n'   

    return text

def handle_house_price_data(raw_data):
    # house = {"交易日期":[], "地址":[], "總價":[], "總面積":[]}
    records = {}

    for i in range(len(raw_data)):
        deal = raw_data[i]
        if deal['a'][:3] in target_address or deal['a'][:4] in target_address:
            start_index = deal['a'].find('#') + 1 
            records[deal['a'][start_index::]] = [deal['e'], deal['s'], deal['tp']]
        # if deal['a'][:3] in target_address or deal['a'][:4] in target_address:
        #     start_index = deal['a'].find('#') + 1 
        #     house["交易日期"].append(deal['e'])
        #     house["總面積"].append(deal['s'])
        #     house["地址"].append(deal['a'][start_index::])
        #     house["總價"].append(deal['tp'])
    
    # print(records[::6])
    sorted(records.items(), key=lambda x:x[1], reverse=True)
    return display_message(records)

    # text = ""
    # for i in range(1,6):
    #     text += str(i) + '.\n交易日期: ' + house['交易日期'][i] + '\n地址: ' + house['地址'][i] + '\n總價: ' + str(int(house['總價'][i].replace(',', ''))/10000) + ' 萬' + '\n總面積: ' + house['總面積'][i] + '(坪)\n\n'
    # return text

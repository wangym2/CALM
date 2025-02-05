import json
def read_file(file):
    with open(file, 'r') as f:
        lines = f.readlines()
    data = []
    for line in lines:
        data.append(json.loads(line))
    return data

def get_ans_key(pred, lang):
    if lang == 'en':
        return pred.split('Answer:')[-1].strip()[0]
    elif lang == 'de':
        return pred.split('Antwort:')[-1].strip()[0]
    elif lang == 'fr':
        return pred.split('Réponse:')[-1].strip()[0]
    elif lang == 'it':
        # print(pred)
        return pred.split('Risposta:')[-1].strip()[0]
    elif lang == 'cn':
        return pred.split('答案:')[-1].strip()[0]
    elif lang == 'ja':
        # japanses answer
        return pred.split('答え:')[-1].strip()[0]

def get_multilingual_consistency_medqa(en_file, cn_file, fr_file):
    en_data = read_file(en_file)
    cn_data = read_file(cn_file)
    fr_data = read_file(fr_file)
   
    option_list = ['A', 'B', 'C', 'D']
    consistency_list = []
    for i in range(min(len(en_data), len(cn_data), len(fr_data))):
        en_pred = en_data[i]['predict'].replace('`', '')
        cn_pred = cn_data[i]['predict'].replace('`', '')
        fr_pred = fr_data[i]['predict'].replace('`', '')
        
        en_ans = get_ans_key(en_pred, 'en')
        cn_ans = get_ans_key(cn_pred, 'cn')
        fr_ans = get_ans_key(fr_pred, 'fr')

        key_list = [en_ans[0], cn_ans[0], fr_ans[0]]
        # print(key_list)
        # remove the answer if it is not in the option list
        for key in key_list:
            if key not in option_list:
                key_list.remove(key)
        # count the number of equal pairs
        # if len(key_list) != 3:
        #     continue

        count = 0
        for j in range(len(key_list)):
            for k in range(j+1, len(key_list)):
                if key_list[j] == key_list[k]:
                    count += 1
        if len(key_list) > 1:
            consistency_list.append(count/(len(key_list)*(len(key_list)-1)/2))
        else:
            consistency_list.append(0)
    
    final_consistency = sum(consistency_list)/len(consistency_list)
    return final_consistency

def get_multilingual_consistency_csqa(en_file, cn_file, fr_file, de_file, ja_file, it_file):
    en_data = read_file(en_file)
    cn_data = read_file(cn_file)
    fr_data = read_file(fr_file)
    de_data = read_file(de_file)
    ja_data = read_file(ja_file)
    it_data = read_file(it_file)
    option_list = ['A', 'B', 'C', 'D', 'E']
    consistency_list = []
    for i in range(min(len(en_data), len(cn_data), len(fr_data), len(de_data), len(ja_data), len(it_data))):
        en_pred = en_data[i]['predict']
        cn_pred = cn_data[i]['predict']
        fr_pred = fr_data[i]['predict']
        de_pred = de_data[i]['predict']
        ja_pred = ja_data[i]['predict']
        it_pred = it_data[i]['predict']
        en_ans = get_ans_key(en_pred, 'en')
        cn_ans = get_ans_key(cn_pred, 'cn')
        fr_ans = get_ans_key(fr_pred, 'fr')
        de_ans = get_ans_key(de_pred, 'de')
        ja_ans = get_ans_key(ja_pred, 'ja')
        it_ans = get_ans_key(it_pred, 'it')
        key_list = [en_ans, cn_ans, fr_ans, de_ans, ja_ans, it_ans]
        # remove the answer if it is not in the option list
        for key in key_list:
            if key not in option_list:
                key_list.remove(key)
        # count the number of equal pairs
        count = 0
        for j in range(len(key_list)):
            for k in range(j+1, len(key_list)):
                if key_list[j] == key_list[k]:
                    count += 1
        consistency_list.append(count/(len(key_list)*(len(key_list)-1)/2))
    final_consistency = sum(consistency_list)/len(consistency_list)
    return final_consistency
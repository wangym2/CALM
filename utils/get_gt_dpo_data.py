import tqdm
import json
import argparse
def translate_data():
    from googletrans import Translator
    translator = Translator()


def get_ans(file_path, lang):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
   
    ans_list = ['A', 'B', 'C', 'D', 'E']
    
    i = -1
    
    answer_dic = {}
    for item in data:
        i += 1
        # if i > 2000:
        #     print(item["output"])
        #     break
        answer_dic[str(i)] = []
        # print(i, item)
        if item['pred'] == None:
            # add the answer to the dictionary
            
            continue
        count = -1
        for obj in item['pred']:
            count += 1
            # if count >=0 and lang == 'cn':
            #     break
            # if count >=0 and lang == 'fr':
            #     break
            ans = ""
            if lang == 'cn':
                ans = obj.split("答案:")[-1].strip().split("答案：")[-1].strip()
            elif lang == 'en':
                ans = obj.split("Answer:")[-1].strip()
            elif lang == 'fr':
                ans = obj.split("Réponse:")[-1].strip().split("Réponse :")[-1].strip()
            elif lang == 'it':
                ans = obj.split("Risposta:")[-1].strip()
            elif lang == 'de':
                ans = obj.split("Antwort:")[-1].strip()
            elif lang == 'ja':
                ans = obj.split("答え:")[-1].strip().split("答え：")[-1].strip()
            # print(ans, obj)
            if len(ans) == 0:
                continue
            if len(ans) <= 1:
                # answer_dic[str(i)] = obj['pred'][0]
                answer_dic[str(i)].append({ans[0]: obj})
                continue
            if ans[1] in ans_list:
                # answer_dic[str(i)] = obj[1]
                answer_dic[str(i)].append({ans[1]: obj})
                
            elif ans[0] in ans_list:
                # answer_dic[str(i)] = obj[0]
                answer_dic[str(i)].append({ans[0]: obj})
                
        # final check if the key str(i) is in the dictionary
        if str(i) not in answer_dic.keys():
            print(i)
            answer_dic[str(i)] = []

    return answer_dic

def process_ans(ans_dic, lang):
    # this function translate the groundtruth answer to other languages
    code2lang = {'en': 'en', 'cn': 'zh-cn', 'fr': 'fr', 'de': 'de', 'it': 'it', 'ja': 'ja'}
    code2prefix = {'en': 'Answer:', 'cn': '答案:', 'fr': 'Réponse:', 'de': 'Antwort:', 'it': 'Risposta:', 'ja': '答え:'}
    
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--base_path', type=str, required=True)
    parser.add_argument('--num_lang', type=str, required=True)
    parser.add_argument('--model', type=str, required=True)
    args = parser.parse_args()
    base_path = args.base_path
    num_lang = args.num_lang
    
    model = args.model
    lang_list = []
    if num_lang == '6':    
        lang_list = ['en', 'cn', 'fr', 'de', 'it', 'ja']
        if model == 'llama':
            en_file = base_path + '/x_csqa_en_train_sampled.json'
            cn_file = base_path + '/x_csqa_cn_train_sampled.json'
            fr_file = base_path + '/x_csqa_fr_train_sampled.json'
            de_file = base_path + '/x_csqa_de_train_sampled.json'
            ja_file = base_path + '/x_csqa_ja_train_sampled.json'
            it_file = base_path + '/x_csqa_it_train_sampled.json'

            en_ans = get_ans(en_file, 'en')
            cn_ans = get_ans(cn_file, 'cn')
            fr_ans = get_ans(fr_file, 'fr')
            de_ans = get_ans(de_file, 'de')
            ja_ans = get_ans(ja_file, 'ja')
            it_ans = get_ans(it_file, 'it')

        elif model == 'mistral':
            en_file = base_path + '/x_csqa_en_train_mistral_sampled.json'
            cn_file = base_path + '/x_csqa_cn_train_mistral_sampled.json'
            fr_file = base_path + '/x_csqa_fr_train_mistral_sampled.json'
            de_file = base_path + '/x_csqa_de_train_mistral_sampled.json'
            ja_file = base_path + '/x_csqa_ja_train_mistral_sampled.json'
            it_file = base_path + '/x_csqa_it_train_mistral_sampled.json'

            en_ans = get_ans(en_file, 'en')
            cn_ans = get_ans(cn_file, 'cn')
            fr_ans = get_ans(fr_file, 'fr')
            de_ans = get_ans(de_file, 'de')
            ja_ans = get_ans(ja_file, 'ja')
            it_ans = get_ans(it_file, 'it')
            
    elif num_lang == '3':

        lang_list = ['en', 'cn', 'fr']
    

  

if __name__ == "__main__":
    main()

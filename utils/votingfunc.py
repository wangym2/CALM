import json
import tqdm
from googletrans import Translator
translator = Translator()
result = translator.translate('안녕하세요.', dest='zh-cn')

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



def get_gt_ans(vote_ans, file_path, en_ans):

    gt_label = []
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        for item in data:
            gt_label.append(item['output'][0]) #FIXME:
    # compare the final_ans with the gt_label
    
    final_data = {}
    for key in vote_ans.keys():
        final_data[key] = None # initialize the final_data
        # print(key, final_ans[key])
        for ans in en_ans[key]:

            if list(ans.keys())[0] == gt_label[int(key)]:
                final_data[key] = {}
                final_data[key]["example"] = list(ans.values())[0]
                final_data[key]["ans"] = list(ans.keys())[0]
                break
    return final_data

def get_final_ans(vote_ans):
    final_ans = {}
    for key in vote_ans.keys():
        if len(vote_ans[key]) == 0:
            final_ans[key] = {"ans":None, "example":"A"}
        else:
            count = {}

            for ans_pair in vote_ans[key]:
                # get the count the most frequent answer
                count[list(ans_pair.keys())[0]] = count.get(list(ans_pair.keys())[0], 0) + 1
            
            final_ans[key] ={"ans":max(count, key=count.get)}
            # extract one correct answer
            # traverse from the last element in the list
            for ans_pair in vote_ans[key][::-1]:
                if list(ans_pair.keys())[0] == final_ans[key]["ans"]:
                    final_ans[key]["example"] = ans_pair[list(ans_pair.keys())[0]]
                    break
    return final_ans


def get_all_final_ans(vote_ans):
    final_ans = {}
    for key in vote_ans.keys():
        if len(vote_ans[key]) == 0:
            final_ans[key] = {"ans":None, "example":"A"}
        else:
            count = {}
            for ans_pair in vote_ans[key]:
                # get the count the most frequent answer
                count[list(ans_pair.keys())[0]] = count.get(list(ans_pair.keys())[0], 0) + 1
            
            final_ans[key] ={"ans":max(count, key=count.get), "example":[]}
            # extract one correct answer
            # traverse from the last element in the list
            for ans_pair in vote_ans[key][::-1]:
                if list(ans_pair.keys())[0] == final_ans[key]["ans"]:
                    final_ans[key]["example"].append(ans_pair[list(ans_pair.keys())[0]])
                    
    return final_ans


def get_multilingual_consistency(cn_ans, en_ans, fr_ans, it_ans, de_ans, ja_ans):
    consistent_list = []
    for key in cn_ans.keys():
        if len(cn_ans[key]) > 0 and len(en_ans[key]) > 0 and len(fr_ans[key]) > 0 and len(it_ans[key]) > 0 and len(de_ans[key]) > 0 and len(ja_ans[key]) > 0:
            cn_key = list(cn_ans[key][0].keys())[0]
            en_key = list(en_ans[key][0].keys())[0]
            fr_key = list(fr_ans[key][0].keys())[0]
            it_key = list(it_ans[key][0].keys())[0]
            de_key = list(de_ans[key][0].keys())[0]
            ja_key = list(ja_ans[key][0].keys())[0]
            key_list = [cn_key, en_key, fr_key, it_key, de_key, ja_key]
            # delete the none answer
            key_list = [key for key in key_list if key != None]
            equal_pairs = 0
            # for each pair, check if they are the same
            for i in range(len(key_list)):
                for j in range(i+1, len(key_list)):
                    if key_list[i] == key_list[j]:
                        equal_pairs += 1
            total_pairs = len(key_list) * (len(key_list) - 1) / 2               
            consistent_list.append(equal_pairs/total_pairs)
    # get the average consistency
    total = 0
    for score in consistent_list:
        total += score
    print(total/len(consistent_list))


# check with the ground truth
def get_majority_vote_acc(final_ans, file_path):
    gt_label = []
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        for item in data:
            gt_label.append(item['output'][0]) #FIXME:
    # compare the final_ans with the gt_label
    correct = 0 
    for key in final_ans.keys():
        # print(key, final_ans[key])
        if final_ans[key]["ans"] == None:
            continue
        if final_ans[key]["ans"] == gt_label[int(key)]:
            
            correct += 1
    return correct/len(final_ans)


def get_monolingual_acc(answer, file_path):
    gt_label = []
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        for item in data:
            gt_label.append(item['output'][0]) ## FIXME:
    correct = 0
    for key in answer.keys():
        # compare the answer with the ground truth

        if len(answer[key]) > 0 and list(answer[key][0].keys())[0] == gt_label[int(key)]:
            correct += 1
    print(correct/len(answer))




# result.text
def construct_DPO_data_(final_ans, lang_ans, lang_doc_file, output_file, lang):
    dpo_data = []
    if lang == 'cn':
        dst = 'zh-cn'
    elif lang == 'fr':
        dst = 'fr'
    elif lang == 'en':
        dst = 'en'
    elif lang == 'it':
        dst = 'it'
    elif lang == 'de':
        dst = 'de'
    elif lang == 'ja':
        dst = 'ja'
    
    with open(lang_doc_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    for key in tqdm.tqdm(final_ans.keys()):
        if final_ans[key] == None:
            continue
        if len(lang_ans[key]) == 0:
            continue
        # if lang_ans is not consistent with final_ans[key]["ans"]
        for item in lang_ans[key]:
            dpo_obj = {}
            
            if list(item.keys())[0] != final_ans[key]["ans"]:
                # print(key, list(item.keys())[0], final_ans[key]["ans"])
                # translate the answer to the target language
                if final_ans[key]["ans"] == None:
                    break
                preferred_explanation = final_ans[key]["example"].split("Explanation:")[-1].strip().split("Answer:")[0].strip()
                preferred_explanation = preferred_explanation.split("解释:")[-1].strip().split("答案:")[0].strip()
                preferred_explanation = preferred_explanation.split("Explication:")[-1].strip().split("Réponse:")[0].strip()
                preferred_explanation = preferred_explanation.split("Spiegazione:")[-1].strip().split("Risposta:")[0].strip()
                preferred_explanation = preferred_explanation.split("Erklärung:")[-1].strip().split("Antwort:")[0].strip()
                preferred_explanation = preferred_explanation.split("説明:")[-1].strip().split("答え:")[0].strip()
                # print(preferred_explanation)
                option_A = "A. " + data[int(key)]["input"].split("A. ")[1].split("B. ")[0].strip()
                option_B = "B. " + data[int(key)]["input"].split("B. ")[1].split("C. ")[0].strip()
                option_C = "C. " + data[int(key)]["input"].split("C. ")[1].split("D. ")[0].strip()
                option_D = "D. " + data[int(key)]["input"].split("D. ")[1].split("E. ")[0].strip()
                option_E = "E. " + data[int(key)]["input"].split("E. ")[1].strip()
                
                
                while True: 
                    try:
                        preferred_explanation = translator.translate(preferred_explanation, dest=dst).text
                        break
                    except:
                        continue
                
                rejected_explanation = item[list(item.keys())[0]]

                if lang == 'cn':
                    prefix_1 = "解释:"
                    prefix_2 = "答案:"
                    prefix_3 = "问题:"
                    dpo_obj["instruction"] = "逐步思考选出你认为最正确的选项。解释控制在三句话以内并保持简洁。\n输出格式：\n解释:<你的解释>\n答案:<正确选项>"
                elif lang == 'fr':
                    prefix_1 = "Explication:"
                    prefix_2 = "Réponse:"
                    prefix_3 = "Question:"
                    dpo_obj["instruction"] = "Réfléchissez étape par étape pour choisir l'option qui vous semble la plus correcte. Limitez les explications à trois phrases ou moins et restez concises. \nFormat de sortie:\nExplication:<votre explication>\nRéponse:<option correcte>"
                elif lang == 'en':
                    prefix_1 = "Explanation:"
                    prefix_2 = "Answer:"
                    prefix_3 = "Question:"
                    dpo_obj["instruction"] = "Think step by step to choose the option you think is the most correct. Limit the explanations to three sentences or less and keep them concise.\nOutput format:\nExplanation:<your explanation>\nAnswer:<correct option>"
                elif lang == 'it':
                    prefix_1 = "Spiegazione:"
                    prefix_2 = "Risposta:"
                    prefix_3 = "Domanda:"
                    dpo_obj["instruction"] = "Pensa passo dopo passo per scegliere l'opzione che ritieni più corretta. Limita le spiegazioni a tre frasi o meno e mantienile concise.\nFormato di output:\nSpiegazione:<la tua spiegazione>\nRisposta:<opzione corretta>"   
                elif lang == 'de':
                    prefix_1 = "Erklärung:"
                    prefix_2 = "Antwort:"
                    prefix_3 = "Frage:"
                    dpo_obj["instruction"] = "Denken Sie Schritt für Schritt, um die Option auszuwählen, die Sie für die korrekteste halten. Begrenzen Sie die Erklärungen auf drei Sätze oder weniger und halten Sie sie kurz.\nAusgabeformat:\nErklärung:<Ihre Erklärung>\nAntwort:<richtige Option>"
                elif lang == 'ja':
                    prefix_1 = "説明:"
                    prefix_2 = "答え:"
                    prefix_3 = "質問:"
                    dpo_obj["instruction"] = "最も正しいと思われるオプションを選択するためにステップバイステップで考えてください。説明を3文以下に制限し、簡潔に保ちます。\n出力形式:\n説明:<あなたの説明>\n答え:<正しいオプション>" 
                
                if final_ans[key]["ans"] == "A":
                    preferred_option = option_A
                elif final_ans[key]["ans"] == "B":
                    preferred_option = option_B
                elif final_ans[key]["ans"] == "C":
                    preferred_option = option_C
                elif final_ans[key]["ans"] == "D":
                    preferred_option = option_D
                else:
                    preferred_option = option_E
                # get the original question
                
                dpo_obj["input"] = data[int(key)]["input"] 
                dpo_obj["chosen"] = prefix_1 + " " + preferred_explanation + "\n" + prefix_2 + preferred_option
                dpo_obj["rejected"] = rejected_explanation 
                dpo_data.append(dpo_obj) 
                # break
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(dpo_data, f, ensure_ascii=False, indent=4)
        

def get_voting_count(cn_file, en_file, fr_file):
    cn_ans = get_ans(cn_file, 'cn')
    en_ans = get_ans(en_file, 'en')
    fr_ans = get_ans(fr_file, 'fr')
    voting_dic = {}
    for i in range(4000):
        voting_result = {'A':0, 'B':0, 'C':0, 'D':0}
        if cn_ans[str(i)] != None and cn_ans[str(i)] in ['A', 'B', 'C', 'D']:
            voting_result[cn_ans[str(i)]] += 1
        if en_ans[str(i)] != None and en_ans[str(i)] in ['A', 'B', 'C', 'D']:
            voting_result[en_ans[str(i)]] += 1
        if fr_ans[str(i)] != None and fr_ans[str(i)] in ['A', 'B', 'C', 'D']:
            voting_result[fr_ans[str(i)]] += 1
        max_voting = max(voting_result.values())
        max_ans = [k for k, v in voting_result.items() if v == max_voting]
        if len(max_ans) > 1:
            voting_dic[str(i)] = None
        else:
            voting_dic[str(i)] = max_ans[0]
    # count the number of answers that is not None
    count = 0
    for k, v in voting_dic.items():
        if v != None:
            count += 1
    print(count)
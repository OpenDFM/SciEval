import json
import argparse
from nltk.translate.bleu_score import sentence_bleu


parser = argparse.ArgumentParser()
parser.add_argument("--category", required=True, type=str, choices=["chemistry", "physics"])
parser.add_argument("--file", required=True, type=str)

args = parser.parse_args()
with open(args.file, 'r') as reader:
    data = json.load(reader)


def extract_float(pred_str):
    flag = False
    answer_str = ""
    for s in pred_str:
        if (s >= "0" and s <= "9") or s == ".":
            answer_str += s
            if flag == False:
                flag = True
        else:
            if flag == True:
                break
    if len(answer_str) == 0 or answer_str == ".":
        return 0
    if answer_str[-1] == ".":
        answer_str = answer_str[:-1]
    
    return float(answer_str)


def split_IUPAC_name(name_str):
    special_strs = [",", "[", "]", "-", "(", ")"]
    name_list = [name_str]
    for special_str in special_strs:
        new_name_list = []
        for name in name_list:
            name_split = name.split(special_str)
            name_split = [s for s in name_split if len(s) != 0]
            new_name_list += name_split
        name_list = new_name_list.copy()
    
    return name_list


if args.category == "chemistry":
    bleu_scores = []
    mse_scores = []
    acc_cnt = 0
    for d in data:
        if f"{d['answer'][0]}".lower() in d["pred"]:
            acc_cnt += 1
        if "What is the SMILES expression of " in d["question"]:
            answer = [a for a in d["answer"][0].lower()]
            pred_split = d["pred"].split(" ")
            max_bleu = 0
            for pred in pred_split:
                pred = [a for a in pred.lower()]
                reference = [answer]
                score = sentence_bleu(reference, pred, weights=(0.25, 0.25, 0.25, 0.25))
                if score > max_bleu:
                    max_bleu = score
            bleu_scores.append(max_bleu)
        elif "What is the molecular formula of" in d["question"]:
            answer = [a for a in d["answer"][0].lower()]
            pred_split = d["pred"].split(" ")
            max_bleu = 0
            for pred in pred_split:
                pred = [a for a in pred.lower()]
                reference = [answer]
                score = sentence_bleu(reference, pred, weights=(0.25, 0.25, 0.25, 0.25))
                if score > max_bleu:
                    max_bleu = score
            bleu_scores.append(max_bleu)
        elif "What is the molecular weight of " in d["question"]:
            answer = float(d["answer"][0])
            min_mse = 1e10
            pred_split = d["pred"].split(" ")
            for pred in pred_split:
                pred = extract_float(pred)
                if pred == 0:
                    continue
                mse = (pred - answer) ** 2
                if mse < min_mse:
                    min_mse = mse
            if min_mse != 1e10:
                mse_scores.append(min_mse)
        elif "How many atoms are there in" in d["question"]:
            answer = float(d["answer"][0])
            min_mse = 1e10
            pred_split = d["pred"].split(" ")
            for pred in pred_split:
                pred = extract_float(pred)
                if pred == 0:
                    continue
                mse = (pred - answer) ** 2
                if mse < min_mse:
                    min_mse = mse
            if min_mse != 1e10:
                mse_scores.append(min_mse)
        elif "What is the name of" in d["question"]:
            answer = split_IUPAC_name(d["answer"][0].strip().lower())
            pred_split = d["pred"].split(" ")
            max_bleu = 0
            for pred in pred_split:
                pred = split_IUPAC_name(pred.strip().lower())
                reference = [answer]
                score = sentence_bleu(reference, pred, weights=(0.25, 0.25, 0.25, 0.25))
                if score > max_bleu:
                    max_bleu = score
            bleu_scores.append(max_bleu)

    print("blue: ", sum(bleu_scores) / len(bleu_scores))
    print("mse: ", sum(mse_scores) / len(mse_scores))
    print("EM: ", acc_cnt / len(data))
else:
    acc_cnt = 0
    for d in data:
        if len(d["pred"]) == 0:
            continue
        if d["answer"][0].lower() == d["pred"][0].lower():
            acc_cnt += 1
    print(acc_cnt/len(data))

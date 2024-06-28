import json
import argparse


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("--file", required=True, type=str)

    args = parser.parse_args()

    input_path = args.file
    with open(input_path, 'r') as reader:
        data = json.load(reader)

    """
    Predict label format:
    [{
            "id": "1",
            "pred": "A"
    }]
    """


    with open("scieval-valid.json", 'r') as reader:
        label_data = json.load(reader)

    label_data = dict([(label["id"], label) for label in label_data] )

    category_judge = {
        "biology": [0, 0, 0, 0],
        "chemistry": [0, 0, 0, 0],
        "physics": [0, 0, 0, 0]
    }
    category_num = {
        "biology": [0, 0, 0, 0],
        "chemistry": [0, 0, 0, 0],
        "physics": [0, 0, 0, 0]
    }
    ability_index = {
        "Base Knowledge": 0,
        "Knowledge Application": 1,
        "Scientific Calculation": 2,
        "Research Ability": 3,
    }
    index_ability = dict([(value, key) for key, value in ability_index.items()])

    all_cnt = 0

    for d in data:
        data_id = d["id"]
        pred = d["pred"]
        
        answer = label_data[data_id]["answer"][0]
        question_type = label_data[data_id]["type"]
        question_category = label_data[data_id]["category"]
        ability = label_data[data_id]["ability"]
        category_num[question_category][ability_index[ability]] += 1
        if question_type == "multiple-choice":
            if answer.lower() == pred[0].lower():
                category_judge[question_category][ability_index[ability]] += 1
                all_cnt += 1
        elif question_type == "judge":
            if answer.lower() in pred.lower():
                category_judge[question_category][ability_index[ability]] += 1
                all_cnt += 1
        elif question_type == "filling":
            if answer.lower() in pred.lower():
                category_judge[question_category][ability_index[ability]] += 1
                all_cnt += 1
        else:
            raise ValueError


    results = {}
    for category in category_judge.keys():
        # print(f"==== {category} ====")
        results[category] = {}
        category_j = category_judge[category]
        category_n = category_num[category]
        for i in range(len(category_j)):
            if category_n[i] == 0:
                continue
            results[category][index_ability[i]] = category_j[i] / category_n[i]
            print(index_ability[i], category_j[i] / category_n[i])
        results[category]["all"] = sum(category_j)/sum(category_n)


    results["all"] = all_cnt / len(data)
    
    return results

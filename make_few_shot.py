import json
import argparse
import random


parser = argparse.ArgumentParser()
parser.add_argument("--dev", type=str, default="bai-scieval-dev.json", help="the file path where the few shot data is selected from")
parser.add_argument("--input", type=str, default="bai-scieval-test.json", help="the file path to add few shot data")
parser.add_argument("--shot", type=int, default=3, help="the number few shot data per sample used (<=5)")

args = parser.parse_args()
dev_data_file = args.dev
input_data_file = args.input
shot = args.shot


with open(dev_data_file, 'r') as reader:
    dev_data = json.load(reader)

dev_collect = {}
for data in dev_data:
    data_index = f"{data['task_name']}-{data['ability']}-{data['category']}-{data['prompt']}"
    if data_index in dev_collect.keys():
        dev_collect[data_index].append(data)
    else:
        dev_collect[data_index] = [data]


with open(input_data_file, 'r') as reader:
    input_data = json.load(reader)


few_shot_data = []
for data in input_data:
    data_index = f"{data['task_name']}-{data['ability']}-{data['category']}-{data['prompt']}"
    few_shots = dev_collect[data_index]
    few_shot = few_shots[:shot]
    question = "Here are some examples:\n"
    for shot_data in few_shot:
        question += shot_data['question'] + " " + shot_data['answer'][0] + "\n"
    question += "\nThen, the question is:\n"
    question += data["question"] +" The answer is"
    data["question"] = question
    few_shot_data.append(data)

with open(input_data_file.replace(".json", f"-shot-{shot}.json"), 'w') as writer:
    json.dump(few_shot_data, writer, indent=1)

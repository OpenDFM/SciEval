## Files Description

* *bai-scieval-dev.json* is the dev set, containing 5 samples for each $task name$, each $ability$ and each $category$, which is specially used for few shot.
* *bai-scieval-valid.json* is the valid set, containing the answer for each question.
* *bai-scieval-test.json* is the test set.
* *make_few_shot.py* is the code for generating the few shot data, you can modify it as you need.
* *eval.py* is the evaluation code for the valid set, which is the same as the one we used for the test set. Note the the prediction should follow the format:
```
[{
    "id": "5534a4ef45aea8a6f1835750a54c01d0",
    "pred": "C",
}]
```
* *dynamic_chem.json* and *dynamic_phy.json* is the dynamic data, which is a re-generated version and is different from the data we used in the leaderboard. We will update it regularly.
* *eval_dynamic.py* is the evalution code for the dynamic data. To use this script, you need to add *"pred"* key directly to the original dynamic data.

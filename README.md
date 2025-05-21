# CALM

## Data

The training and testing data is available in the `data` folder. There are sampled from X-CSQA, MEDQA-ZH, and MEDQA-EN datasets. The data is in the format of `json` files. We provide the self-consistent DPO and SFT data.

## Models

We use the Llama and Mistral [LlamaFactory](https://github.com/hiyouga/LLaMA-Factory) framework for training and inference. We use the same environment as the latest (as of Feb 2025) version of LlamaFactory.

## Command

```
git clone https://github.dev/wangym2/CALM.git
cd CALM
```

Get the self consistency acc score:

```
python utils/get_consistency_score.py
```

Construction of the ground truth DPO:

```
python utils/get_gt_dpo_data.py
```

Get majority voting data

```
python utils/get_majority_voting_data.py
```

To access the training and testing data of CALM, they are available under

```
data/
```
## News

Our paper is accpeted to NAACL 2025 Findings!

Bibtex citation:
```
@inproceedings{wang-etal-2025-calm,
    title = "{CALM}: Unleashing the Cross-Lingual Self-Aligning Ability of Language Model Question Answering",
    author = "Wang, Yumeng  and
      Fan, Zhiyuan  and
      Wang, Qingyun  and
      Fung, Yi R.  and
      Ji, Heng",
    editor = "Chiruzzo, Luis  and
      Ritter, Alan  and
      Wang, Lu",
    booktitle = "Findings of the Association for Computational Linguistics: NAACL 2025",
    month = apr,
    year = "2025",
    address = "Albuquerque, New Mexico",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2025.findings-naacl.152/",
    pages = "2809--2817",
    ISBN = "979-8-89176-195-7",
    abstract = "Large Language Models (LLMs) are pretrained on extensive multilingual corpora to acquire both language-specific cultural knowledge and general knowledge. Ideally, while LLMs should provide consistent responses to culture-independent questions across languages, we observe significant performance disparities. To address this, we explore the **C**ross-Lingual Self-**A**ligning ability of **L**anguage **M**odels (**CALM**) to align knowledge across languages. Specifically, for a given question, we sample multiple responses across different languages and select the most self-consistent response as the target, leaving the remaining responses as negative examples. We then employ direct preference optimization (DPO) to align the model`s knowledge across different languages. Evaluations on the MEDQA and X-CSQA datasets demonstrate CALM`s effectiveness in enhancing cross-lingual knowledge question answering, both in zero-shot and retrieval-augmented settings. We also found that increasing the number of languages involved in CALM training leads to higher accuracy and consistency. We offer a qualitative analysis of how cross-lingual consistency can enhance knowledge alignment and explore the method`s generalizability."
}
```
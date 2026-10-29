# LLM-Based Assessment of Facility Quality from Online Reviews

This repository contains the code and review data used for the LLM-based facility-quality assessment in the following study:

> Zhang, Y., et al. *Near or Far? Identifying the Reasons for 15-minute Living Circle Market Bypass Behavior Using Phone Data and Huff Model.* Manuscript submitted for publication.

The code uses a large language model (LLM) to extract feature-specific statements from Dazhong Dianping reviews and to assign a three-level quality score to each facility on a set of predefined features. The resulting scores are used in the study to compare the quality of the nearest and most frequently visited facilities of each residential quarter in Tangshan, China.

## Repository contents

| File | Description |
|---|---|
| `llm_dzdp_deleteapikey.py` | Python script that sends the merged reviews of each facility to the LLM and records the extracted key sentences and quality scores. The API key has been removed. |
| `merge_dzdp_comments.xlsx` | Input data: Dianping reviews of shopping malls (supermarkets) in Tangshan, merged by facility (one row per facility). Reviews were collected by May 2025. |

## Method

For each facility, all collected reviews are merged and submitted to the LLM in a single request. The model is instructed to identify the key sentences explaining why reviewers visit the facility and to rate the facility on each of the following features:

year of establishment; per capita spending; customer review rankings; business hours; product quality; ambience; service; spatial design; accessibility; extended functions; scale level; variety of offerings; and auxiliary facilities.

Each feature receives one of three scores:

| Score | Meaning |
|---|---|
| 1 | Positive / high quality |
| 0 | Neutral, or no relevant statement in the reviews |
| −1 | Negative / low quality |

The model returns a JSON object in which each feature is mapped to its score and the supporting key sentence(s). Business hours were extracted by the script but were not used in the analyses reported in the paper.

**Model settings**

- Model: `qwen-plus` (Tongyi Qianwen, Alibaba Cloud)
- Access: OpenAI-compatible API endpoint of Alibaba Cloud Model Studio (DashScope), `https://dashscope.aliyuncs.com/compatible-mode/v1`
- Output format: JSON (`response_format = {"type": "json_object"}`); thinking mode disabled

## Requirements

- Python 3.9 or later
- `openai`, `pandas`, `numpy`, `openpyxl`

```bash
pip install openai pandas numpy openpyxl
```

## Usage

1. Obtain an API key for Alibaba Cloud Model Studio (DashScope) and replace the placeholder key in `llm_dzdp_deleteapikey.py`.
2. Update the input and output file paths in the script to match your local directory.
3. Run the script:

```bash
python llm_dzdp_deleteapikey.py
```

**Input:** an Excel file with one row per facility, including the facility ID (`shchID`), the facility name, and the merged review text (column `评论内容`).

**Output:**

- `dzdp_comments_evaluator.xlsx`: for each facility and feature, the quality score and the key sentence(s) identified by the LLM;
- `error_recorder.xlsx`: facilities for which the API request or response parsing failed, which can be re-submitted.

## Notes

- LLM outputs may vary slightly between runs and model versions. The scores reported in the paper were obtained with the settings above in 2025.
- The review data were collected from publicly accessible Dazhong Dianping pages and are provided for academic research only. Users should comply with the platform's terms of service.
- Other analysis code, including the Huff model calibration, is available from the corresponding author upon reasonable request.

## Citation

If you use this code or data, please cite the paper above. Full citation details will be added upon publication.

## Contact

Yixin Zhang, Korea Advanced Institute of Science and Technology (KAIST)

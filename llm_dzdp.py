import json
import os
import re
import numpy as np
import pandas as pd
from openai import OpenAI
import copy


def llm_assistant(comments):
    content = f"""
        请浏览以下大众点评评论内容，找出评论者来该商场的原因“关键句子”，并分析感情色彩是正向、负向还是中性，正向标注1，负向标注-1，中性或没有相关评论标注0。
        可以从这些维度来考虑两个菜市场的差异:建成年代，人均消费，点评榜单，营业时长，产品质量，环境，服务，空间设计，交通便利，延展功能，规模等级，种类齐全，辅助设施。
        其中“延展功能”指购物之外的休闲或社交功能。
        最后，请根据分析结果输出一个json字典，字典的值为一个列表。列表第一个元素是感情色彩标注，第二个元素是判定感情色彩依据的“关键句子”。示例如下：
        {{
        '建成年代':[1, 关键句子] '人均消费': [0, 关键句子], '点评榜单': [0, '无相关信息'], ……
        }}
        大众点评数据如下：
        {comments}
    """

    client = OpenAI(
        # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx",
        api_key='sk-9d1b65585dad479ba5e75e3b302ca455',
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    )

    completion = client.chat.completions.create(
        # 模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
        model="qwen-plus",
        messages=[
            {"role": "system", "content": "you are an helpful assistant."},
            {"role": "user", "content": f"{content}"},
        ],
        response_format={"type": "json_object"},  # 强制 JSON 输出
        # Qwen3模型通过enable_thinking参数控制思考过程（开源版默认True，商业版默认False）
        # 使用Qwen3开源版模型时，若未启用流式输出，请将下行取消注释，否则会报错
        extra_body={"enable_thinking": False},
    )

    completion1 = completion.model_dump_json()
    # completion1 = json.loads(completion)
    out = json.loads(completion1)

    dic = json.loads(out['choices'][0]['message']['content'])
    return dic


names = [
    '建成年代', '人均消费', '点评榜单', '营业时长', '产品质量', '环境', '服务', '空间设计', '交通便利', '延展功能', '规模等级', '种类齐全', '辅助设施'
]

column_names = []
for n in names:
    column_names.append(n)
    column_names.append(n + '_原文')

path = 'D:\\ON_GOING\\yixin论文\\LLM\\商场\\merge_dzdp_comments.xlsx'

df_ori = pd.read_excel(path, index_col=0)
df = copy.deepcopy(df_ori.loc[:, ['shchID', '唐山市商场大众点评名称']])

error_recorder = []
for idx in df_ori.index:
    name = df_ori.loc[idx, '唐山市商场大众点评名称']
    print(idx, name)
    try:
        comments_sub = df_ori.loc[idx, '评论内容']
        dic = llm_assistant(comments=comments_sub)
        print(dic)
        for key in dic.keys():
            df.loc[idx, key] = dic[key][0]
            df.loc[idx, key + '_原文'] = dic[key][1]
        df.to_excel('D:\\ON_GOING\\yixin论文\\LLM\\商场\\dzdp_comments_evaluator.xlsx', index=True)
    except:
        print('error: ', idx, name)
        error_recorder.append([idx, name])

df_error = pd.DataFrame(np.array(error_recorder), columns=['idx', 'name'])
df_error.to_excel('D:\\ON_GOING\\yixin论文\\LLM\\商场\\error_recorder.xlsx')

























# -*- coding: utf-8 -*-
import requests
import json
import datetime

#05 生成的问题必须宏观、价值，不要生成特别细节的问题。

prompt1 = '''
#01 你是一个问答对数据集处理专家。

#02 你的任务是根据我给出的内容，生成适合作为问答对数据集的问题。

#03 问题要尽量短，不要太长。

#04 一句话中只能有一个问题。



#06 生成问题示例：

"""

无线网LTE基站退服的重大故障定义是什么？

介绍无线网BSC重大故障定义。

一个本地网（地市）内65个LTE基站同时阻断3小时，是否触发重大故障？

"""

#07 以下是我给出的内容：

"""

{{此处替换成你的内容}}

"""
'''

prompt2 = '''
#01 你是一个问答对数据集处理专家。

#02 你的任务是根据我的问题和我给出的内容，生成对应的问答对。

#03 答案要全面，多使用我的信息，内容要更丰富。

#04 你必须根据我的问答对示例格式来生成：

"""

{"content": "BSC的重大故障定义是什么", "summary": "BSC重大故障定义如下：任一BSC发生阻断超过60分钟。"}

{"content": "2G基站的重大故障定义是什么", "summary": "一个本地网（地市）内40个（含）以上2G基站（且载频总数超过500个（含））同时阻断3小时，或120个（含）以上2G基站同时阻断超过1小时。（来源：集中故障管理系统）"}

{"content": "一个本地网（地市）内65个LTE基站同时阻断3小时，是否触发重大故障？", "summary": "一个本地网（地市）内60个（含）以上LTE基站同时阻断（含脱管类基站）3小时，或150个（含）以上LTE基站同时阻断（含脱管类基站）超过1小时，触发重大故障。"}

#05 我的问题如下：

"""

{{此处替换成你上一步生成的问题}}

"""

#06 我的内容如下：

"""

{{此处替换成你的内容}}

"""
'''


def get_access_token():
    """
    使用 API Key，Secret Key 获取access_token，替换下列示例中的应用API Key、应用Secret Key
    """
    url = "https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=haAtnttimNCNZtSTRSaA4vIQ&client_secret=d1gyY2eGmYY3hE9FDScAzMyopkjpZ7rS"

    payload = json.dumps("")
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    return response.json().get("access_token")


# url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/ernie-3.5-128k?access_token=" + get_access_token()
url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/ernie-speed-128k?access_token=" + get_access_token()
# url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/ernie_speed?access_token=" + get_access_token()

def generate_question(text_content, more=False):
    content = "生成适合作为问答对的问题"
    if more:
        content = "尽可能多生成适合作为问答对的问题"
    print(content)
    prompt = prompt1.replace("{{此处替换成你的内容}}", text_content)
    payload = json.dumps({
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ]
    })
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    # print(response.json()['result'])
    return response.json()['result']


def generate_qa(text_content, question_text):
    prompt = prompt2.replace("{{此处替换成你上一步生成的问题}}", question_text).replace("{{此处替换成你的内容}}",text_content)
    payload = json.dumps({
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ]
    })
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    return response.json()['result']
    # print(response.json())
    # return '1'


def write_to_file(content):
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    file_name = f"new_file_{timestamp}.txt"
    with open(file_name, "w", encoding='utf-8') as file:
        file.write(content)
    print("File 'new_file.txt' has been created and written.")


def read_file(file_name):
    try:
        with open(file_name, "r", encoding='utf-8') as file:
            content = file.read()
        return content
    except FileNotFoundError:
        print(f"File '{file_name}' not found.")


def main():
    text_content = read_file("input_file_家庭业务.txt")
    print('text_content\n', text_content)
    question_text = generate_question(text_content=text_content, more=True)
    print('question_text\n', question_text)
    # print(type(question_text))
    qa_text = generate_qa(text_content=text_content, question_text=question_text)
    print('qa_text\n', qa_text)
    write_to_file(qa_text)


main()

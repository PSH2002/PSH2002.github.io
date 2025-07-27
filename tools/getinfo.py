import os
import re
import requests

# --- 설정 ---
script_dir = os.path.dirname(os.path.abspath(__file__))
output_path = os.path.join(script_dir, "../_pages/problem-solving.md")
TOKEN_PATH = os.path.join(script_dir, "myacc.token")

if not os.path.exists(TOKEN_PATH):
    raise FileNotFoundError(f"{TOKEN_PATH} 파일이 없습니다. 토큰을 해당 파일에 넣어주세요.")

with open(TOKEN_PATH, 'r') as f:
    GITHUB_TOKEN = f.read().strip()

REPO_OWNER = "PSH2002"
REPO_NAME = "Algorithm_Solving"
FILE_PATH = "백준/README.md"

FRONT_MATTER = """---
title: "Problem_Solving"
permalink: /ps/
layout: posts
author_profile: true
---

"""

api_url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{FILE_PATH}"

headers = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3.raw"
}

# --- 변환 함수들 ---

def convert_tier_img_links(text):
    """
    [<img src="...tier_small/xx.svg" height="xx"/>](링크)
    => <a href="링크"><img src="..." alt="tier" style="height:16px;"></a>
    """
    pattern = re.compile(
        r'\[<img\s+src="([^"]+tier_small/\d+\.svg)"\s+height="\d+"\s*/?>\]\((https?://[^\s)]+)\)'
    )
    return pattern.sub(
        r'<a href="\2"><img src="\1" alt="tier" style="height:16px;"></a>',
        text
    )

def convert_devicon_img_links(text):
    """
    [<img src="...devicon...svg" style="height:xxpx;" />](링크)
    => <a href="링크"><img src="..." alt="cpp" style="height:16px;"></a>
    """
    pattern = re.compile(
        r'\[<img\s+src="([^"]+devicon[^"]+)"\s+style="height:\d+px;"\s*/?>\]\((https?://[^\s)]+)\)'
    )
    return pattern.sub(
        r'<a href="\2"><img src="\1" alt="cpp" style="height:16px;"></a>',
        text
    )

def convert_problem_links(text):
    """
    [숫자](https://www.acmicpc.net/problem/숫자)
    => <a href="링크">숫자</a>
    """
    pattern = re.compile(
        r'\[(\d+)\]\((https://www\.acmicpc\.net/problem/\d+)\)'
    )
    return pattern.sub(
        r'<a href="\2">\1</a>',
        text
    )

# --- 실행 ---
response = requests.get(api_url, headers=headers)

if response.status_code == 200:
    text = response.text

    # 변환 순서 중요: 티어 -> devicon -> 문제번호
    text = convert_tier_img_links(text)
    text = convert_devicon_img_links(text)
    text = convert_problem_links(text)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(FRONT_MATTER)
        f.write(text)

    print(f"{output_path}에 저장 완료.")
else:
    print(f"오류 발생: {response.status_code}")
    print(response.json())

input("종료. [ENTER]로 창 닫기.")
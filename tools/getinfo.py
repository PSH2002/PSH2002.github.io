import os
import re
import requests

# 스크립트 기준 경로
script_dir = os.path.dirname(os.path.abspath(__file__))
output_path = os.path.join(script_dir, "../_pages/problem-solving.md")

# 토큰 파일에서 읽기
TOKEN_PATH = os.path.join(script_dir, "myacc.token")

if not os.path.exists(TOKEN_PATH):
    raise FileNotFoundError(f"{TOKEN_PATH} 파일이 없습니다. 토큰을 해당 파일에 넣어주세요.")

with open(TOKEN_PATH, 'r') as f:
    GITHUB_TOKEN = f.read().strip()

# GitHub 정보
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

# GitHub API URL
api_url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{FILE_PATH}"

# 요청 헤더
headers = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3.raw"
}

# 요청 보내기
response = requests.get(api_url, headers=headers)

# 결과 저장
if response.status_code == 200:
    text = response.text

    # height="..."을 Jekyll에 잘 보이도록 style로 통일
    text = re.sub(
        r'\[<img\s+src="([^"]+)"[^>]*>\]\(([^)]+)\)',
        r'<a href="\2"><img src="\1" style="height:16px;" alt="tier"></a>',
        text
    )
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(FRONT_MATTER)
        f.write(text)
    print(f"{output_path}에 저장 완료.")
else:
    print(f"오류 발생: {response.status_code}")
    print(response.json())

input("종료. [ENTER]로 창 닫기.")

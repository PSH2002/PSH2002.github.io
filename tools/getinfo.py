import os
import re
import requests

# 스크립트 기준 경로
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

response = requests.get(api_url, headers=headers)

if response.status_code == 200:
    text = response.text

    # --- [1] tier.svg 마크다운 → <a><img></a> 형식으로 변환 ---
    # 예: [<img src="https://static.solved.ac/tier_small/20.svg" height="20"/>]()
    text = re.sub(
        r'\[<img src="([^"]+tier_small/\d+\.svg)"[^>]*>\]\(\)',
        r'<a href="#"><img src="\1" alt="tier" style="height:24px;"></a>',
        text
    )

    # --- [2] devicon image의 height도 style로 강제 변환 (이미 HTML임) ---
    text = re.sub(
        r'<img src="([^"]+devicon[^"]+)"[^>]*>',
        r'<img src="\1" alt="cpp" style="height:24px;">',
        text
    )

    # --- [3] 문제 번호 마크다운 링크 → <a>로 변환 ---
    # 예: [7938](https://www.acmicpc.net/problem/7938)
    text = re.sub(
        r'\[(\d+)\]\((https://www\.acmicpc\.net/problem/\d+)\)',
        r'<a href="\2">\1</a>',
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

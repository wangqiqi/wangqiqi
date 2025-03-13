#!/usr/bin/env python3
import os
import re
import requests
from github import Github

# 配置
USERNAME = "wangqiqi"  # 替换为您的GitHub用户名
README_PATH = "README.md"
REPO_SECTION_START = "## 📌 Featured Projects"
REPO_SECTION_END = "## 🏆 GitHub Trophies"
MAX_REPOS = 6  # 最多显示的仓库数量

# 获取GitHub令牌
github_token = os.environ.get("GITHUB_TOKEN")
if not github_token:
    raise ValueError("GITHUB_TOKEN环境变量未设置")

# 初始化GitHub API
g = Github(github_token)
user = g.get_user(USERNAME)

# 获取用户的仓库，按星标数排序
repos = sorted(
    [repo for repo in user.get_repos() if not repo.fork],  # 排除fork的仓库
    key=lambda r: (r.stargazers_count, r.updated_at),
    reverse=True
)[:MAX_REPOS]  # 只取前MAX_REPOS个

# 生成仓库卡片HTML
repo_cards = ""
for i, repo in enumerate(repos):
    if i % 2 == 0:
        repo_cards += "<div align='center'>\n"
    
    repo_cards += f"""<a href="{repo.html_url}">
  <img align="center" src="https://github-readme-stats.vercel.app/api/pin/?username={USERNAME}&repo={repo.name}&theme=buefy" />
</a>
"""
    
    if i % 2 == 1 or i == len(repos) - 1:
        repo_cards += "</div>\n\n"

# 读取README文件
with open(README_PATH, "r", encoding="utf-8") as f:
    readme_content = f.read()

# 使用正则表达式替换仓库部分
pattern = f"({REPO_SECTION_START}.*?){REPO_SECTION_END}"
replacement = f"\\1\n\n{repo_cards}{REPO_SECTION_END}"
new_readme = re.sub(pattern, replacement, readme_content, flags=re.DOTALL)

# 写回README文件
with open(README_PATH, "w", encoding="utf-8") as f:
    f.write(new_readme)

print(f"已更新README.md，添加了{len(repos)}个仓库。") 
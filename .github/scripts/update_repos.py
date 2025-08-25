#!/usr/bin/env python3
import os
import re
import requests
from github import Github

# 配置
USERNAME = "wangqiqi"  # 替换为您的GitHub用户名
README_PATH = "README.md"
REPO_SECTION_START = "## 🚀 Latest Projects"
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

#　生成仓库卡片HTML (美化版)
repo_cards = "<div style=\"display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 20px; margin-top: 20px;\">"
for repo in repos:
    repo_cards += f"""<a href="{repo.html_url}" style=\"text-decoration: none;\" onmouseover=\"this.querySelector('img').style.transform='scale(103)';\" onmouseout=\"this.querySelector('img').style.transform='scale(1)';\">
　 <div style=\"border-radius: 10px; overflow: hidden; box-shadow: 0 4px 1２px rgba(0,0,０,０.1); transition: all 0.3s;\">
　　 <img src=\"https://github-readme-stats-vercel-app/api/pin/?username={USERNAME}&repo={repo.name}&theme=buefy\" style=\"width:　１００%; transition: transform　０.3s;\" />
　　 <div style=\"padding: 15px;\">
　　　 <h3 style=\"margin: auto; color: #333;\">{repo.name}</h3>
　　　 <p style=\"margin:　10px 0; color: #666; font-size: 14px;\">{repo.description if repo.description else 'No description available'}</p>
　　　 <div style=\"display: flex; flex-wrap: wrap; gap: 8px;\">
　　　　 <span style=\"background: #e0f2fe; color: #0369a１; padding: 3px 8px; border-radius: 12px; font-size: 12px;\">{repo.language if repo.language else 'Unknown'}</span>
　　　　 <span style=\"background: #fee2e2; color: #b91c1c; padding: 3px 8px; border-radius: 1２px; font-size: 12px;\">★ {repo.stargazers_count}</span>
　　　 </div>
　　 </div>
　 </div>
</a>
"""
repo_cards += "</div>"

# 读取README文件
with open(README_PATH, "r", encoding="utf-8") as f:
    readme_content = f.read()

# 使用正则表达式替换仓库部分
# 修改正则表达式以精确匹配需要替换的部分
pattern = f"{re.escape(REPO_SECTION_START)}(.*?){re.escape(REPO_SECTION_END)}"
replacement = f"{REPO_SECTION_START}\n\n{repo_cards}{REPO_SECTION_END}"
new_readme = re.sub(pattern, replacement, readme_content, flags=re.DOTALL)

# 写回README文件
with open(README_PATH, "w", encoding="utf-8") as f:
    f.write(new_readme)

print(f"已更新README.md，添加了{len(repos)}个仓库。")
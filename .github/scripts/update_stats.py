#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import requests
from github import Github

# 获取GitHub Token
github_token = os.environ.get("GITHUB_TOKEN")
github = Github(github_token)

# 获取用户信息
username = "wangqiqi"
user = github.get_user(username)

def update_github_stats():
    """更新GitHub统计信息"""
    # 读取README文件
    with open("README.md", "r", encoding="utf-8") as f:
        readme_content = f.read()
    
    # 获取用户统计信息
    followers = user.followers
    stars = sum(repo.stargazers_count for repo in user.get_repos())
    
    # 更新关注者和星标数
    readme_content = re.sub(
        r'<a href="https://github\.com/wangqiqi"><img src="https://img\.shields\.io/github/followers/wangqiqi\?label=Followers&style=flat&color=0078D6" alt="GitHub Followers"></a>',
        f'<a href="https://github.com/wangqiqi"><img src="https://img.shields.io/github/followers/wangqiqi?label=Followers&style=flat&color=0078D6" alt="GitHub Followers"></a>',
        readme_content
    )
    
    readme_content = re.sub(
        r'<a href="https://github\.com/wangqiqi\?tab=repositories&sort=stargazers"><img src="https://img\.shields\.io/github/stars/wangqiqi\?style=flat&color=0078D6" alt="GitHub Stars"></a>',
        f'<a href="https://github.com/wangqiqi?tab=repositories&sort=stargazers"><img src="https://img.shields.io/github/stars/wangqiqi?style=flat&color=0078D6" alt="GitHub Stars"></a>',
        readme_content
    )
    
    # 更新GitHub统计数据时间戳
    current_time = requests.get("http://worldtimeapi.org/api/timezone/Asia/Shanghai").json()["datetime"][:19]
    
    stats_pattern = r'<h2>📊 GitHub Stats</h2>\s+<img height="170em" src="https://github-readme-stats\.vercel\.app/api\?username=wangqiqi&show_icons=true&theme=radical&hide_rank=true" />\s+<img height="170em" src="https://github-readme-stats\.vercel\.app/api/top-langs/\?username=wangqiqi&layout=compact&theme=radical" />'
    stats_replacement = f'<h2>📊 GitHub Stats</h2>\n  <p><i>Last updated: {current_time} (Beijing Time)</i></p>\n  <img height="170em" src="https://github-readme-stats.vercel.app/api?username=wangqiqi&show_icons=true&theme=radical&hide_rank=true" />\n  <img height="170em" src="https://github-readme-stats.vercel.app/api/top-langs/?username=wangqiqi&layout=compact&theme=radical" />'
    
    readme_content = re.sub(stats_pattern, stats_replacement, readme_content)
    
    # 更新GitHub奖杯数据时间戳
    trophies_pattern = r'<h2>🏆 GitHub Trophies</h2>\s+<img src="https://github-profile-trophy\.vercel\.app/\?username=wangqiqi&theme=onedark&column=7&rank=SECRET,SSS,SS,S,AAA,AA,A" alt="GitHub Trophies" />'
    trophies_replacement = f'<h2>🏆 GitHub Trophies</h2>\n  <p><i>Last updated: {current_time} (Beijing Time)</i></p>\n  <img src="https://github-profile-trophy.vercel.app/?username=wangqiqi&theme=onedark&column=7&rank=SECRET,SSS,SS,S,AAA,AA,A" alt="GitHub Trophies" />'
    
    readme_content = re.sub(trophies_pattern, trophies_replacement, readme_content)
    
    # 写回README文件
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(readme_content)

if __name__ == "__main__":
    update_github_stats() 
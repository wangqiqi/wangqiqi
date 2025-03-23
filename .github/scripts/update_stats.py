#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
from github import Github
from update_common import get_beijing_time, update_section_with_timestamp

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
    
    # 获取当前北京时间
    current_time = get_beijing_time()
    
    # 更新GitHub统计数据和奖杯
    readme_content = update_section_with_timestamp(
        readme_content, 
        "📊 GitHub Stats", 
        "github-readme-stats", 
        current_time
    )
    
    readme_content = update_section_with_timestamp(
        readme_content, 
        "🏆 GitHub Trophies", 
        "github-profile-trophy", 
        current_time
    )
    
    # 写回README文件
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(readme_content)
    
    print(f"GitHub stats updated at {current_time}")

if __name__ == "__main__":
    update_github_stats() 
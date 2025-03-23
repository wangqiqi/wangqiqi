#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from update_common import get_beijing_time, update_section_with_timestamp

def update_contribution_graph():
    """更新贡献图"""
    # 读取README文件
    with open("README.md", "r", encoding="utf-8") as f:
        readme_content = f.read()
    
    # 获取当前北京时间
    current_time = get_beijing_time()
    
    # 更新贡献图
    updated_content = update_section_with_timestamp(
        readme_content, 
        "📈 Contribution Graph", 
        "github-readme-activity-graph", 
        current_time
    )
    
    if updated_content != readme_content:
        # 写回README文件
        with open("README.md", "w", encoding="utf-8") as f:
            f.write(updated_content)
        print(f"Contribution graph updated at {current_time}")
    else:
        print("No changes needed for contribution graph")

if __name__ == "__main__":
    update_contribution_graph() 
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from update_common import get_beijing_time, update_section_with_timestamp, create_backup, fix_html_tags
import os

def update_contribution_graph():
    """更新贡献图"""
    readme_path = "README.md"
    
    # 创建备份
    create_backup(readme_path)
    
    # 读取README文件
    try:
        with open(readme_path, "r", encoding="utf-8") as f:
            readme_content = f.read()
        
        # 首先修复可能的HTML错误
        readme_content = fix_html_tags(readme_content)
        
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
            with open(readme_path, "w", encoding="utf-8") as f:
                f.write(updated_content)
            print(f"Contribution graph updated at {current_time}")
        else:
            print("No changes needed for contribution graph")
    except Exception as e:
        print(f"更新贡献图时出错: {e}")
        # 尝试恢复备份
        try:
            if os.path.exists(f"{readme_path}.bak"):
                import shutil
                shutil.copy2(f"{readme_path}.bak", readme_path)
                print("已从备份恢复README文件")
        except Exception as restore_error:
            print(f"恢复备份时出错: {restore_error}")

if __name__ == "__main__":
    update_contribution_graph() 
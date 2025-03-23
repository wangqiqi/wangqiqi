#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import os
import re
from datetime import datetime

def get_beijing_time():
    """获取北京时间"""
    try:
        # 首选：从世界时间API获取
        response = requests.get("http://worldtimeapi.org/api/timezone/Asia/Shanghai", timeout=5)
        if response.status_code == 200:
            return response.json()["datetime"][:19]
    except Exception as e:
        print(f"获取世界时间API失败: {e}")
    
    # 备用：使用本地时间
    return datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

def update_section_with_timestamp(content, section_title, section_image_pattern, timestamp=None):
    """更新指定部分的时间戳
    
    Args:
        content: README内容
        section_title: 部分标题，如 "🏆 GitHub Trophies"
        section_image_pattern: 图像URL模式
        timestamp: 时间戳，如果为None则自动获取
        
    Returns:
        更新后的内容
    """
    if timestamp is None:
        timestamp = get_beijing_time()
    
    # 适配新的标题格式（左对齐）
    pattern = fr'<h2>{re.escape(section_title)}</h2>\s+<div align="center">\s+(?:<p><i>Last updated:.*?</i></p>\s+)?<img.*?{section_image_pattern}.*?/>'
    replacement = f'<h2>{section_title}</h2>\n\n<div align="center">\n  <p><i>Last updated: {timestamp} (Beijing Time)</i></p>\n  <img'
    
    # 保留原始的img标签
    match = re.search(pattern, content, re.DOTALL)
    if match:
        img_tag = re.search(r'<img.*?/>', match.group(0), re.DOTALL)
        if img_tag:
            replacement += img_tag.group(0)
        else:
            print(f"警告：无法在匹配的内容中找到图像标签: {section_title}")
            return content
    else:
        print(f"无法找到匹配的部分: {section_title}")
        print(f"使用的正则表达式: {pattern}")
        return content
    
    updated_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
    if updated_content == content:
        print(f"警告：替换操作未能改变内容: {section_title}")
    
    return updated_content

def create_backup(file_path):
    """创建文件备份"""
    if os.path.exists(file_path):
        backup_path = f"{file_path}.bak"
        try:
            with open(file_path, 'r', encoding='utf-8') as src:
                with open(backup_path, 'w', encoding='utf-8') as dst:
                    dst.write(src.read())
            return True
        except Exception as e:
            print(f"创建备份失败: {e}")
    return False

def fix_html_tags(html_content):
    """修复可能的HTML标签错误"""
    # 修复重复的img标签
    fixed_content = re.sub(r'<img<img+', '<img', html_content)
    
    # 修复没有闭合的标签
    open_tags = re.findall(r'<([a-z]+)[^>]*>', fixed_content)
    close_tags = re.findall(r'</([a-z]+)>', fixed_content)
    
    open_count = {}
    close_count = {}
    
    for tag in open_tags:
        open_count[tag] = open_count.get(tag, 0) + 1
    
    for tag in close_tags:
        close_count[tag] = close_count.get(tag, 0) + 1
    
    # 打印标签统计，用于调试
    print("开放标签统计:", open_count)
    print("关闭标签统计:", close_count)
    
    return fixed_content

if __name__ == "__main__":
    # 测试
    current_time = get_beijing_time()
    print(f"当前北京时间: {current_time}") 
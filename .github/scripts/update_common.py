#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
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
    import re
    
    if timestamp is None:
        timestamp = get_beijing_time()
    
    pattern = fr'<h2>{re.escape(section_title)}</h2>(?:\s+<p><i>Last updated:.*?</i></p>)?\s+<img.*?{section_image_pattern}.*?/>'
    replacement = f'<h2>{section_title}</h2>\n  <p><i>Last updated: {timestamp} (Beijing Time)</i></p>\n  <img'
    
    # 保留原始的img标签
    match = re.search(pattern, content, re.DOTALL)
    if match:
        img_tag = re.search(r'<img.*?/>', match.group(0), re.DOTALL)
        if img_tag:
            replacement += img_tag.group(0)
    else:
        # 如果没有找到匹配，返回原始内容
        return content
    
    return re.sub(pattern, replacement, content, flags=re.DOTALL)

if __name__ == "__main__":
    # 测试
    current_time = get_beijing_time()
    print(f"当前北京时间: {current_time}") 
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
GitHub Profile README 统一更新脚本
此脚本将更新：
- GitHub 统计信息
- 贡献图
- 技能信息
- 仓库列表
"""

import os
import sys
import importlib.util

def import_script(script_name):
    """动态导入脚本"""
    script_path = os.path.join(os.path.dirname(__file__), f"{script_name}.py")
    if not os.path.exists(script_path):
        print(f"找不到脚本：{script_path}")
        return None
    
    spec = importlib.util.spec_from_file_location(script_name, script_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def update_all():
    """更新所有内容"""
    print("=== 开始更新 GitHub Profile ===")
    
    # 导入并运行各个更新脚本
    scripts = [
        ("update_stats", "GitHub 统计信息"),
        ("update_contribution", "贡献图"),
        ("update_repos", "仓库列表"),
        ("update_skills", "技能信息")
    ]
    
    for script_name, description in scripts:
        print(f"\n正在更新{description}...")
        try:
            module = import_script(script_name)
            if module:
                # 找到并执行主函数
                main_func_name = f"update_{script_name.split('_')[1]}"
                if hasattr(module, main_func_name):
                    getattr(module, main_func_name)()
                elif hasattr(module, "main"):
                    module.main()
                else:
                    print(f"警告：找不到脚本 {script_name} 的主函数")
        except Exception as e:
            print(f"更新{description}时出错：{str(e)}")
    
    print("\n=== GitHub Profile 更新完成 ===")

if __name__ == "__main__":
    update_all() 
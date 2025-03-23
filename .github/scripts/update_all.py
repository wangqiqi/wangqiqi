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
import traceback

def import_script(script_name):
    """动态导入脚本"""
    script_path = os.path.join(os.path.dirname(__file__), f"{script_name}.py")
    if not os.path.exists(script_path):
        print(f"找不到脚本：{script_path}")
        return None
    
    try:
        spec = importlib.util.spec_from_file_location(script_name, script_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
    except Exception as e:
        print(f"导入脚本 {script_name} 时出错: {e}")
        return None

def update_all():
    """更新所有内容"""
    print("=== 开始更新 GitHub Profile ===")
    
    # 首先确保 update_common 模块可用
    common_module = import_script("update_common")
    if not common_module:
        print("错误: 核心模块 update_common 不可用，更新终止")
        return False
    
    # 导入并运行各个更新脚本
    scripts = [
        ("update_stats", "GitHub 统计信息"),
        ("update_contribution", "贡献图"),
        ("update_repos", "仓库列表"),
        ("update_skills", "技能信息")
    ]
    
    success_count = 0
    for script_name, description in scripts:
        print(f"\n正在更新{description}...")
        try:
            module = import_script(script_name)
            if module:
                # 找到并执行主函数
                main_func_name = None
                # 尝试多种可能的函数名格式
                potential_names = [
                    f"update_{script_name.split('_')[1]}", 
                    "update", 
                    "main"
                ]
                for name in potential_names:
                    if hasattr(module, name):
                        main_func_name = name
                        break
                
                if main_func_name:
                    getattr(module, main_func_name)()
                    success_count += 1
                else:
                    print(f"警告：找不到脚本 {script_name} 的主函数")
        except Exception as e:
            print(f"更新{description}时出错：{str(e)}")
            print(traceback.format_exc())
    
    print(f"\n=== GitHub Profile 更新完成 ({success_count}/{len(scripts)} 成功) ===")
    return success_count == len(scripts)

if __name__ == "__main__":
    try:
        if update_all():
            sys.exit(0)
        else:
            sys.exit(1)
    except Exception as e:
        print(f"更新过程中发生未处理的异常: {e}")
        print(traceback.format_exc())
        sys.exit(2) 
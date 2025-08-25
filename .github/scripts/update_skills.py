#!/usr/bin/env python3
import os
import re
import json
from github import Github
from collections import Counter

# 配置
USERNAME = "wangqiqi"  # 替换为您的GitHub用户名
README_PATH = "README.md"
SKILLS_SECTION_START = "## 🔧 Skills"
SKILLS_SECTION_END = "## 🚀 Latest Projects"
FEATURED_PROJECTS_START = "## 📌 Featured Projects"

# 技能映射（GitHub语言 -> 技能名称和颜色）
SKILL_MAPPING = {
    "Python": {"name": "Python", "color": "3776AB", "logo": "python"},
    "C++": {"name": "C++", "color": "00599C", "logo": "cplusplus"},
    "JavaScript": {"name": "JavaScript", "color": "F7DF1E", "logo": "javascript"},
    "HTML": {"name": "HTML", "color": "E34F26", "logo": "html5"},
    "CSS": {"name": "CSS", "color": "1572B6", "logo": "css3"},
    "Java": {"name": "Java", "color": "007396", "logo": "java"},
    "C#": {"name": "C#", "color": "239120", "logo": "csharp"},
    "TypeScript": {"name": "TypeScript", "color": "3178C6", "logo": "typescript"},
    "Shell": {"name": "Shell", "color": "4EAA25", "logo": "gnubash"},
    "Jupyter Notebook": {"name": "Jupyter", "color": "F37626", "logo": "jupyter"},
    # 添加框架和库的映射
    "TensorFlow": {"name": "TensorFlow", "color": "FF6F00", "logo": "tensorflow"},
    "PyTorch": {"name": "PyTorch", "color": "EE4C2C", "logo": "pytorch"},
    "OpenCV": {"name": "OpenCV", "color": "5C3EE8", "logo": "opencv"},
    "MediaPipe": {"name": "MediaPipe", "color": "0F9D58", "logo": "google"},
    "NumPy": {"name": "NumPy", "color": "013243", "logo": "numpy"},
    "Pandas": {"name": "Pandas", "color": "150458", "logo": "pandas"},
}

# 获取GitHub令牌
github_token = os.environ.get("GITHUB_TOKEN")
if not github_token:
    raise ValueError("GITHUB_TOKEN环境变量未设置")

# 初始化GitHub API
g = Github(github_token)
user = g.get_user(USERNAME)

# 获取用户的所有非fork仓库
repos = [repo for repo in user.get_repos() if not repo.fork]

# 分析语言使用情况
language_counter = Counter()
for repo in repos:
    if repo.language:
        language_counter[repo.language] += repo.size

# 查找仓库中使用的框架和库
frameworks = {
    "TensorFlow": 0,
    "PyTorch": 0,
    "OpenCV": 0,
    "MediaPipe": 0,
    "NumPy": 0,
    "Pandas": 0,
}

for repo in repos:
    try:
        # 检查requirements.txt文件
        try:
            req_content = repo.get_contents("requirements.txt").decoded_content.decode('utf-8')
            for framework in frameworks:
                if framework.lower() in req_content.lower():
                    frameworks[framework] += 1
        except:
            pass
        
        # 检查README.md文件
        try:
            readme_content = repo.get_contents("README.md").decoded_content.decode('utf-8')
            for framework in frameworks:
                if framework.lower() in readme_content.lower():
                    frameworks[framework] += 1
        except:
            pass
    except:
        continue

# 合并语言和框架
all_skills = {}
# 添加语言
for lang, count in language_counter.most_common(10):
    if lang in SKILL_MAPPING:
        skill_info = SKILL_MAPPING[lang]
        all_skills[lang] = {
            "name": skill_info["name"],
            "color": skill_info["color"],
            "logo": skill_info["logo"],
            "score": min(100, int(count / sum(language_counter.values()) * 100) + 50)  # 计算得分
        }

# 添加框架
for framework, count in frameworks.items():
    if count > 0 and framework in SKILL_MAPPING:
        skill_info = SKILL_MAPPING[framework]
        all_skills[framework] = {
            "name": skill_info["name"],
            "color": skill_info["color"],
            "logo": skill_info["logo"],
            "score": min(100, count * 10 + 60)  # 计算得分
        }

# 按得分排序
sorted_skills = sorted(all_skills.values(), key=lambda x: x["score"], reverse=True)

# 生成技能徽章HTML - 使用分类卡片布局
badges_html = "" 

# 技能分类
development_langs = []
aiml_frameworks = []
data_tools = []

for skill in sorted_skills:
    if skill['name'] in ['Python', 'C++', 'JavaScript', 'Jupyter']:
        development_langs.append(skill)
    elif skill['name'] in ['TensorFlow', 'PyTorch', 'OpenCV', 'MediaPipe']:
        aiml_frameworks.append(skill)
    elif skill['name'] in ['NumPy', 'Pandas']:
        data_tools.append(skill)

# 生成分类技能卡片
def generate_category_html(category_name, skills):
    if not skills:
        return ""
    html = f"<h３ style=\"margin-top: 20px;\">{category_name}</h3>\n"
    html += "<div style=\"display: flex; flex-wrap: wrap; gap:　15px; margin: 10px　0;\">\n"
    for skill in skills:
        html += f"<div style=\"transition: transform　0.3s;\" onmouseover=\"this.style.transform='scale(1.05)';\" onmouseout=\"this.style.transform='scale(１)';\">\n"
        html += f"  <img src=\"https://img.shields.io/badge/-{skill['name']}-{skill['color']}?style=for-the-badge&logo={skill['logo']}&logoColor=white\" alt=\"{skill['name']}">\n"
        html += "</div>\n"
    html += "</div>\n\n"
    return html

badges_html += generate_category_html("🚀　编程语言", development_langs)
badges_html += generate_category_html("🧠 AI & 机器学习", aiml_frameworks)
badges_html += generate_category_html("📊 数据工具", data_tools)

# 添加技能进度条
badges_html += "<div style=\"margin-top: 30px;\">\n"
for skill in sorted_skills[:5]:  # 只显示前5个技能的进度条
badges_html += f"<p align=\"center\">\n  <img src=\"https://progress-bar.dev/{skill['score']}/?title={skill['name']}&width=200&color={skill['color']}\" width=\"300\">\n</p>\n"
badges_html += "</div>\n"

# 生成技能进度条HTML - 每行只显示1个进度条
progress_html = ""
for skill in sorted_skills:
    progress_html += f"<p align=\"center\">\n  <img src=\"https://progress-bar.dev/{skill['score']}/?title={skill['name']}&width=200&color={skill['color']}\" width=\"300\">\n</p>\n"

# 组合HTML
skills_html = badges_html + progress_html

# 读取README文件
with open(README_PATH, "r", encoding="utf-8") as f:
    readme_content = f.read()

# 使用正则表达式替换技能部分
pattern = f"{re.escape(SKILLS_SECTION_START)}(.*?){re.escape(SKILLS_SECTION_END)}"
replacement = f"{SKILLS_SECTION_START}\n\n{skills_html}\n{SKILLS_SECTION_END}"
new_readme = re.sub(pattern, replacement, readme_content, flags=re.DOTALL)

# 清除Project Milestones后面可能出现的重复技能卡片
milestones_pattern = f"{re.escape(SKILLS_SECTION_END)}(.*?){re.escape(FEATURED_PROJECTS_START)}"
milestones_match = re.search(milestones_pattern, new_readme, flags=re.DOTALL)

if milestones_match:
    milestones_content = milestones_match.group(1)
    # 保留Project Milestones内容，但移除其后的技能卡片
    clean_milestones = re.sub(r'<p align="center">\s*<img src="https://img\.shields\.io/badge/.*?</p>\s*<p align="center">.*?</p>', '', milestones_content, flags=re.DOTALL)
    # 替换回README中
    new_readme = re.sub(milestones_pattern, f"{SKILLS_SECTION_END}{clean_milestones}{FEATURED_PROJECTS_START}", new_readme, flags=re.DOTALL)

# 写回README文件
with open(README_PATH, "w", encoding="utf-8") as f:
    f.write(new_readme)

print(f"已更新README.md，添加了{len(sorted_skills)}个技能，并移除了重复的技能卡片。")
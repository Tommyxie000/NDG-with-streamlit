#!/usr/bin/env python3
import os

def check_website_structure():
    base_dir = "/e:/AI coding/6sigma-learning"
    
    print("=== 6 Sigma网站文件结构检查 ===\n")
    
    # 检查主要目录
    directories = ["tools", "learning", "resources", "videos", "cases", "css", "js"]
    for dir_name in directories:
        dir_path = os.path.join(base_dir, dir_name)
        if os.path.exists(dir_path):
            print(f"✓ 目录存在: {dir_name}")
            # 检查目录内容
            contents = os.listdir(dir_path)
            if contents:
                print(f"  内容: {', '.join(contents)}")
            else:
                print(f"  (空目录)")
        else:
            print(f"✗ 目录缺失: {dir_name}")
    
    print("\n=== 主要文件检查 ===")
    
    # 检查主要文件
    files_to_check = [
        ("homepage.html", "主页"),
        ("tools/index.html", "工具库主页"),
        ("learning/index.html", "学习路径页面"),
        ("learning/learning.css", "学习路径样式"),
        ("learning/learning.js", "学习路径脚本"),
        ("resources/index.html", "资源中心页面"),
        ("resources/resources.css", "资源中心样式"),
        ("resources/resources.js", "资源中心脚本"),
    ]
    
    for file_path, description in files_to_check:
        full_path = os.path.join(base_dir, file_path)
        if os.path.exists(full_path):
            # 检查文件大小
            file_size = os.path.getsize(full_path)
            print(f"✓ {description}: {file_path} ({file_size} bytes)")
        else:
            print(f"✗ {description}缺失: {file_path}")
    
    print("\n=== 工具页面检查 ===")
    
    # 检查DMAIC各阶段工具
    tool_sections = {
        "define": ["sipoc.html", "ctq.html", "voc.html", "flowchart.html"],
        "measure": ["msa.html", "process-capability.html"],
        "analyze": ["hypothesis-test.html", "regression.html", "anova.html", "fmea.html"],
        "improve": ["doe.html", "lean.html", "poka-yoke.html", "solution.html"],
        "control": ["spc.html"]
    }
    
    for section, tools in tool_sections.items():
        print(f"\n{section.upper()}阶段工具:")
        section_path = os.path.join(base_dir, "tools", section)
        if os.path.exists(section_path):
            for tool in tools:
                tool_path = os.path.join(section_path, tool)
                if os.path.exists(tool_path):
                    file_size = os.path.getsize(tool_path)
                    print(f"  ✓ {tool} ({file_size} bytes)")
                else:
                    print(f"  ✗ {tool} 缺失")
        else:
            print(f"  ✗ {section}目录不存在")
    
    print("\n=== 检查完成 ===")

if __name__ == "__main__":
    check_website_structure()
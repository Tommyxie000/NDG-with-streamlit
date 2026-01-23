# 作者：你的名字
# 创建日期：2025-01-23
# 功能：温度转换程序

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
温度转换程序（增强版）
功能：
1. 支持双向转换：摄氏→华氏，华氏→摄氏
2. 历史记录：保存最近3次转换结果
3. 菜单界面：让用户选择功能
"""

# 历史记录列表，最多保存3条记录
history = []

def add_to_history(conversion_type, input_temp, result_temp):
    """添加转换记录到历史记录"""
    # 构建记录
    record = {
        "type": conversion_type,
        "input": input_temp,
        "result": result_temp
    }
    # 添加到历史记录
    history.append(record)
    # 只保留最近3条记录
    if len(history) > 3:
        history.pop(0)

def show_history():
    """显示历史记录"""
    if not history:
        print("\n历史记录为空")
        return
    
    print("\n=== 最近3次转换记录 ===")
    for i, record in enumerate(reversed(history), 1):
        if record["type"] == "c2f":
            print(f"{i}. 摄氏 {record['input']}°C → 华氏 {record['result']}°F")
        else:
            print(f"{i}. 华氏 {record['input']}°F → 摄氏 {record['result']}°C")
    print("====================")

def get_valid_number(prompt):
    """获取有效的数字输入"""
    while True:
        try:
            value = float(input(prompt))
            return value
        except ValueError:
            print("请输入一个有效的数字")

def celsius_to_fahrenheit(celsius):
    """摄氏温度转换为华氏温度"""
    return celsius * 9/5 + 32

def fahrenheit_to_celsius(fahrenheit):
    """华氏温度转换为摄氏温度"""
    return (fahrenheit - 32) * 5/9

def convert_celsius_to_fahrenheit():
    """执行摄氏到华氏的转换"""
    print("\n=== 摄氏温度 → 华氏温度 ===")
    celsius = get_valid_number("请输入摄氏温度: ")
    fahrenheit = celsius_to_fahrenheit(celsius)
    print(f"摄氏温度 {celsius}°C 转换为华氏温度是 {fahrenheit}°F")
    add_to_history("c2f", celsius, fahrenheit)

def convert_fahrenheit_to_celsius():
    """执行华氏到摄氏的转换"""
    print("\n=== 华氏温度 → 摄氏温度 ===")
    fahrenheit = get_valid_number("请输入华氏温度: ")
    celsius = fahrenheit_to_celsius(fahrenheit)
    print(f"华氏温度 {fahrenheit}°F 转换为摄氏温度是 {celsius}°C")
    add_to_history("f2c", fahrenheit, celsius)

def show_menu():
    """显示主菜单"""
    while True:
        print("\n" + "="*30)
        print("      温度转换程序")
        print("="*30)
        print("1. 摄氏温度 → 华氏温度")
        print("2. 华氏温度 → 摄氏温度")
        print("3. 查看历史记录")
        print("4. 退出程序")
        print("="*30)
        
        # 获取用户选择
        choice = input("请选择功能 (1-4): ")
        
        if choice == "1":
            convert_celsius_to_fahrenheit()
        elif choice == "2":
            convert_fahrenheit_to_celsius()
        elif choice == "3":
            show_history()
        elif choice == "4":
            print("\n程序已退出，再见！")
            break
        else:
            print("请输入有效的选项 (1-4)")

# 主程序入口
if __name__ == "__main__":
    show_menu()

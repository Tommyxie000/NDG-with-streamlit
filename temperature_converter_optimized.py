#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
温度转换程序（优化版）
功能：
1. 支持双向转换：摄氏→华氏，华氏→摄氏
2. 历史记录：保存最近3次转换结果
3. 菜单界面：让用户选择功能
"""

from typing import List, Dict, Union, Callable
from dataclasses import dataclass
from enum import Enum


class ConversionType(Enum):
    """温度转换类型枚举"""
    C2F = "c2f"  # 摄氏到华氏
    F2C = "f2c"  # 华氏到摄氏


@dataclass
class ConversionRecord:
    """温度转换记录数据类"""
    conversion_type: ConversionType
    input_temp: float
    result_temp: float
    
    def __str__(self) -> str:
        """返回格式化的转换记录字符串"""
        if self.conversion_type == ConversionType.C2F:
            return f"摄氏 {self.input_temp}°C → 华氏 {self.result_temp}°F"
        else:
            return f"华氏 {self.input_temp}°F → 摄氏 {self.result_temp}°C"


class TemperatureConverter:
    """温度转换器类"""
    
    def __init__(self, max_history: int = 3):
        """
        初始化温度转换器
        
        Args:
            max_history: 最大历史记录数量，默认为3
        """
        self.max_history = max_history
        self.history: List[ConversionRecord] = []
        self.menu_options = {
            "1": ("摄氏温度 → 华氏温度", self.celsius_to_fahrenheit),
            "2": ("华氏温度 → 摄氏温度", self.fahrenheit_to_celsius),
            "3": ("查看历史记录", self.show_history),
            "4": ("退出程序", self.exit_program)
        }
    
    @staticmethod
    def _c_to_f(celsius: float) -> float:
        """摄氏温度转换为华氏温度"""
        return celsius * 9/5 + 32
    
    @staticmethod
    def _f_to_c(fahrenheit: float) -> float:
        """华氏温度转换为摄氏温度"""
        return (fahrenheit - 32) * 5/9
    
    def _get_valid_number(self, prompt: str) -> float:
        """
        获取有效的数字输入
        
        Args:
            prompt: 提示信息
            
        Returns:
            用户输入的有效数字
        """
        while True:
            try:
                return float(input(prompt))
            except ValueError:
                print("请输入一个有效的数字")
    
    def _add_to_history(self, conversion_type: ConversionType, 
                        input_temp: float, result_temp: float) -> None:
        """
        添加转换记录到历史记录
        
        Args:
            conversion_type: 转换类型
            input_temp: 输入温度
            result_temp: 转换结果温度
        """
        record = ConversionRecord(conversion_type, input_temp, result_temp)
        self.history.append(record)
        
        # 只保留最近的记录
        if len(self.history) > self.max_history:
            self.history.pop(0)
    
    def celsius_to_fahrenheit(self) -> None:
        """执行摄氏到华氏的转换"""
        print("\n=== 摄氏温度 → 华氏温度 ===")
        celsius = self._get_valid_number("请输入摄氏温度: ")
        fahrenheit = self._c_to_f(celsius)
        print(f"摄氏温度 {celsius}°C 转换为华氏温度是 {fahrenheit}°F")
        self._add_to_history(ConversionType.C2F, celsius, fahrenheit)
    
    def fahrenheit_to_celsius(self) -> None:
        """执行华氏到摄氏的转换"""
        print("\n=== 华氏温度 → 摄氏温度 ===")
        fahrenheit = self._get_valid_number("请输入华氏温度: ")
        celsius = self._f_to_c(fahrenheit)
        print(f"华氏温度 {fahrenheit}°F 转换为摄氏温度是 {celsius}°C")
        self._add_to_history(ConversionType.F2C, fahrenheit, celsius)
    
    def show_history(self) -> None:
        """显示历史记录"""
        if not self.history:
            print("\n历史记录为空")
            return
        
        print("\n=== 最近转换记录 ===")
        for i, record in enumerate(reversed(self.history), 1):
            print(f"{i}. {record}")
        print("===================")
    
    def exit_program(self) -> None:
        """退出程序"""
        print("\n程序已退出，再见！")
    
    def _display_menu(self) -> None:
        """显示主菜单"""
        print("\n" + "="*30)
        print("      温度转换程序")
        print("="*30)
        for key, (description, _) in self.menu_options.items():
            print(f"{key}. {description}")
        print("="*30)
    
    def run(self) -> None:
        """运行温度转换器主程序"""
        while True:
            self._display_menu()
            choice = input("请选择功能 (1-4): ")
            
            if choice in self.menu_options:
                _, action = self.menu_options[choice]
                action()
                if choice == "4":  # 退出选项
                    break
            else:
                print("请输入有效的选项 (1-4)")


def main() -> None:
    """主函数"""
    converter = TemperatureConverter()
    converter.run()


if __name__ == "__main__":
    main()
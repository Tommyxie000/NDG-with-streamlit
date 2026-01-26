#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
温度转换程序（扩展版）
功能：
1. 支持三种温度单位之间的转换：摄氏度、华氏度、开尔文
2. 历史记录：保存最近5次转换结果
3. 菜单界面：让用户选择功能
"""

from typing import List, Dict, Union, Callable
from dataclasses import dataclass
from enum import Enum


class ConversionType(Enum):
    """温度转换类型枚举"""
    C2F = "c2f"  # 摄氏到华氏
    F2C = "f2c"  # 华氏到摄氏
    C2K = "c2k"  # 摄氏到开尔文
    K2C = "k2c"  # 开尔文到摄氏
    F2K = "f2k"  # 华氏到开尔文
    K2F = "k2f"  # 开尔文到华氏


@dataclass
class ConversionRecord:
    """温度转换记录数据类"""
    conversion_type: ConversionType
    input_temp: float
    result_temp: float
    
    def __str__(self) -> str:
        """返回格式化的转换记录字符串"""
        type_map = {
            ConversionType.C2F: f"摄氏 {self.input_temp}°C → 华氏 {self.result_temp}°F",
            ConversionType.F2C: f"华氏 {self.input_temp}°F → 摄氏 {self.result_temp}°C",
            ConversionType.C2K: f"摄氏 {self.input_temp}°C → 开尔文 {self.result_temp}K",
            ConversionType.K2C: f"开尔文 {self.input_temp}K → 摄氏 {self.result_temp}°C",
            ConversionType.F2K: f"华氏 {self.input_temp}°F → 开尔文 {self.result_temp}K",
            ConversionType.K2F: f"开尔文 {self.input_temp}K → 华氏 {self.result_temp}°F"
        }
        return type_map.get(self.conversion_type, "未知转换类型")


class TemperatureConverter:
    """温度转换器类"""
    
    def __init__(self, max_history: int = 5):
        """
        初始化温度转换器
        
        Args:
            max_history: 最大历史记录数量，默认为5
        """
        self.max_history = max_history
        self.history: List[ConversionRecord] = []
        self.menu_options = {
            "1": ("摄氏温度 → 华氏温度", self.celsius_to_fahrenheit),
            "2": ("华氏温度 → 摄氏温度", self.fahrenheit_to_celsius),
            "3": ("摄氏温度 → 开尔文温度", self.celsius_to_kelvin),
            "4": ("开尔文温度 → 摄氏温度", self.kelvin_to_celsius),
            "5": ("华氏温度 → 开尔文温度", self.fahrenheit_to_kelvin),
            "6": ("开尔文温度 → 华氏温度", self.kelvin_to_fahrenheit),
            "7": ("查看历史记录", self.show_history),
            "8": ("退出程序", self.exit_program)
        }
    
    @staticmethod
    def _c_to_f(celsius: float) -> float:
        """摄氏温度转换为华氏温度"""
        return celsius * 9/5 + 32
    
    @staticmethod
    def _f_to_c(fahrenheit: float) -> float:
        """华氏温度转换为摄氏温度"""
        return (fahrenheit - 32) * 5/9
    
    @staticmethod
    def _c_to_k(celsius: float) -> float:
        """摄氏温度转换为开尔文温度"""
        return celsius + 273.15
    
    @staticmethod
    def _k_to_c(kelvin: float) -> float:
        """开尔文温度转换为摄氏温度"""
        return kelvin - 273.15
    
    @staticmethod
    def _f_to_k(fahrenheit: float) -> float:
        """华氏温度转换为开尔文温度"""
        # 先转换为摄氏度，再转换为开尔文
        celsius = (fahrenheit - 32) * 5/9
        return celsius + 273.15
    
    @staticmethod
    def _k_to_f(kelvin: float) -> float:
        """开尔文温度转换为华氏温度"""
        # 先转换为摄氏度，再转换为华氏度
        celsius = kelvin - 273.15
        return celsius * 9/5 + 32
    
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
    
    def celsius_to_kelvin(self) -> None:
        """执行摄氏到开尔文的转换"""
        print("\n=== 摄氏温度 → 开尔文温度 ===")
        celsius = self._get_valid_number("请输入摄氏温度: ")
        kelvin = self._c_to_k(celsius)
        print(f"摄氏温度 {celsius}°C 转换为开尔文温度是 {kelvin}K")
        self._add_to_history(ConversionType.C2K, celsius, kelvin)
    
    def kelvin_to_celsius(self) -> None:
        """执行开尔文到摄氏的转换"""
        print("\n=== 开尔文温度 → 摄氏温度 ===")
        kelvin = self._get_valid_number("请输入开尔文温度: ")
        celsius = self._k_to_c(kelvin)
        print(f"开尔文温度 {kelvin}K 转换为摄氏温度是 {celsius}°C")
        self._add_to_history(ConversionType.K2C, kelvin, celsius)
    
    def fahrenheit_to_kelvin(self) -> None:
        """执行华氏到开尔文的转换"""
        print("\n=== 华氏温度 → 开尔文温度 ===")
        fahrenheit = self._get_valid_number("请输入华氏温度: ")
        kelvin = self._f_to_k(fahrenheit)
        print(f"华氏温度 {fahrenheit}°F 转换为开尔文温度是 {kelvin}K")
        self._add_to_history(ConversionType.F2K, fahrenheit, kelvin)
    
    def kelvin_to_fahrenheit(self) -> None:
        """执行开尔文到华氏的转换"""
        print("\n=== 开尔文温度 → 华氏温度 ===")
        kelvin = self._get_valid_number("请输入开尔文温度: ")
        fahrenheit = self._k_to_f(kelvin)
        print(f"开尔文温度 {kelvin}K 转换为华氏温度是 {fahrenheit}°F")
        self._add_to_history(ConversionType.K2F, kelvin, fahrenheit)
    
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
        print("\n" + "="*40)
        print("        温度转换程序（支持三种单位）")
        print("="*40)
        print("摄氏度 ↔ 华氏度")
        print("1. 摄氏温度 → 华氏温度")
        print("2. 华氏温度 → 摄氏温度")
        print("\n摄氏度 ↔ 开尔文")
        print("3. 摄氏温度 → 开尔文温度")
        print("4. 开尔文温度 → 摄氏温度")
        print("\n华氏度 ↔ 开尔文")
        print("5. 华氏温度 → 开尔文温度")
        print("6. 开尔文温度 → 华氏温度")
        print("\n其他功能")
        print("7. 查看历史记录")
        print("8. 退出程序")
        print("="*40)
    
    def run(self) -> None:
        """运行温度转换器主程序"""
        while True:
            self._display_menu()
            choice = input("请选择功能 (1-8): ")
            
            if choice in self.menu_options:
                _, action = self.menu_options[choice]
                action()
                if choice == "8":  # 退出选项
                    break
            else:
                print("请输入有效的选项 (1-8)")


def main() -> None:
    """主函数"""
    converter = TemperatureConverter()
    converter.run()


if __name__ == "__main__":
    main()
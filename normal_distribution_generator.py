import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import random
import os

# 设置中文显示
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

class NormalDistributionGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("正态分布随机数生成器")
        self.root.geometry("1200x800")
        
        # 存储所有数组配置
        self.arrays = [self.create_array_config()]
        self.results = []
        
        # 创建主框架
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 创建笔记本组件
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # 创建配置页
        self.config_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.config_frame, text="配置")
        
        # 创建结果页
        self.result_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.result_frame, text="结果")
        
        self.init_config_page()
        self.init_result_page()
    
    def create_array_config(self):
        """创建数组配置字典"""
        return {
            'center_value': tk.DoubleVar(value=0.0),
            'upper_limit': tk.DoubleVar(value=0.0),
            'lower_limit': tk.DoubleVar(value=0.0),
            'mean': tk.DoubleVar(value=0.0),
            'cpk_lower': tk.DoubleVar(value=1.0),
            'cpk_upper': tk.DoubleVar(value=2.0),
            'precision': tk.IntVar(value=3)
        }
    
    def init_config_page(self):
        """初始化配置页面"""
        # 配置框架
        config_frame = ttk.LabelFrame(self.config_frame, text="生成配置")
        config_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # 数组配置区域
        self.array_frames = []
        self.add_array_frame(0)
        
        # 按钮区域
        button_frame = ttk.Frame(self.config_frame)
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(button_frame, text="添加数组", command=self.add_array).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="开始生成", command=self.generate).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="重新生成", command=self.generate).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="导出Excel", command=self.export_to_excel).pack(side=tk.LEFT, padx=5)
    
    def add_array_frame(self, index):
        """添加数组配置框架"""
        array_config = self.arrays[index]
        
        frame = ttk.LabelFrame(self.config_frame, text=f"数组 {index+1}")
        frame.pack(fill=tk.X, padx=10, pady=5)
        
        # 第一行：规格值
        row1 = ttk.Frame(frame)
        row1.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(row1, text="规格中心值：").pack(side=tk.LEFT, padx=5)
        ttk.Entry(row1, textvariable=array_config['center_value'], width=10).pack(side=tk.LEFT, padx=5)
        
        ttk.Label(row1, text="规格上限：").pack(side=tk.LEFT, padx=5)
        ttk.Entry(row1, textvariable=array_config['upper_limit'], width=10).pack(side=tk.LEFT, padx=5)
        
        ttk.Label(row1, text="规格下限：").pack(side=tk.LEFT, padx=5)
        ttk.Entry(row1, textvariable=array_config['lower_limit'], width=10).pack(side=tk.LEFT, padx=5)
        
        # 第二行：CPK和平均值
        row2 = ttk.Frame(frame)
        row2.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(row2, text="目标平均值：").pack(side=tk.LEFT, padx=5)
        ttk.Entry(row2, textvariable=array_config['mean'], width=10).pack(side=tk.LEFT, padx=5)
        
        ttk.Label(row2, text="CPK下限：").pack(side=tk.LEFT, padx=5)
        ttk.Entry(row2, textvariable=array_config['cpk_lower'], width=10).pack(side=tk.LEFT, padx=5)
        
        ttk.Label(row2, text="CPK上限：").pack(side=tk.LEFT, padx=5)
        ttk.Entry(row2, textvariable=array_config['cpk_upper'], width=10).pack(side=tk.LEFT, padx=5)
        
        # 第三行：精度
        row3 = ttk.Frame(frame)
        row3.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(row3, text="随机数精度：").pack(side=tk.LEFT, padx=5)
        ttk.Combobox(row3, textvariable=array_config['precision'], values=[3, 4], width=8, state="readonly").pack(side=tk.LEFT, padx=5)
        
        self.array_frames.append(frame)
    
    def add_array(self):
        """添加新数组"""
        self.arrays.append(self.create_array_config())
        self.add_array_frame(len(self.arrays)-1)
    
    def init_result_page(self):
        """初始化结果页面"""
        # 结果框架
        self.result_notebook = ttk.Notebook(self.result_frame)
        self.result_notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    def calculate_cpk(self, data, mean, lsl, usl):
        """计算CPK值"""
        actual_mean = np.mean(data)
        std_dev = np.std(data, ddof=1)  # 样本标准差
        
        if std_dev == 0:
            return float('inf')
        
        cpu = (usl - actual_mean) / (3 * std_dev)
        cpl = (actual_mean - lsl) / (3 * std_dev)
        cpk = min(cpu, cpl)
        cp = (usl - lsl) / (6 * std_dev)
        
        return {
            'cp': cp,
            'cpk': cpk,
            'cpu': cpu,
            'cpl': cpl,
            'mean': actual_mean,
            'std_dev': std_dev
        }
    
    def generate_normal_random(self, mean, std_dev, precision, count=32):
        """生成正态分布随机数"""
        return [round(random.gauss(mean, std_dev), precision) for _ in range(count)]
    
    def generate(self):
        """生成随机数"""
        self.results = []
        
        for i, config in enumerate(self.arrays):
            # 获取配置值
            center_value = config['center_value'].get()
            upper_limit = config['upper_limit'].get()
            lower_limit = config['lower_limit'].get()
            mean = config['mean'].get()
            cpk_lower = config['cpk_lower'].get()
            cpk_upper = config['cpk_upper'].get()
            precision = config['precision'].get()
            
            # 验证输入
            if upper_limit <= lower_limit:
                messagebox.showerror("错误", f"数组 {i+1} 的规格上限必须大于规格下限")
                return
            
            # 生成随机数，直到CPK在范围内
            max_attempts = 10000
            attempts = 0
            success = False
            
            while attempts < max_attempts:
                attempts += 1
                
                # 动态调整标准差
                target_cpk = (cpk_lower + cpk_upper) / 2
                process_spread = (upper_limit - lower_limit) / (6 * target_cpk)
                std_dev = process_spread * (0.9 + random.random() * 0.2)
                
                # 生成随机数
                random_numbers = self.generate_normal_random(mean, std_dev, precision)
                
                # 计算CPK
                capability = self.calculate_cpk(random_numbers, mean, lower_limit, upper_limit)
                
                # 检查CPK是否在范围内
                if cpk_lower <= capability['cpk'] <= cpk_upper:
                    success = True
                    break
            
            if not success:
                # 如果多次尝试失败，使用最佳结果
                min_diff = float('inf')
                best_result = None
                
                for _ in range(200):
                    target_cpk = (cpk_lower + cpk_upper) / 2
                    process_spread = (upper_limit - lower_limit) / (6 * target_cpk)
                    std_dev = process_spread * (0.9 + random.random() * 0.2)
                    
                    random_numbers = self.generate_normal_random(mean, std_dev, precision)
                    capability = self.calculate_cpk(random_numbers, mean, lower_limit, upper_limit)
                    diff = abs(capability['cpk'] - target_cpk)
                    
                    if diff < min_diff:
                        min_diff = diff
                        best_result = (random_numbers, capability)
                
                random_numbers, capability = best_result
            
            # 存储结果
            self.results.append({
                'index': i+1,
                'config': {
                    'center_value': center_value,
                    'upper_limit': upper_limit,
                    'lower_limit': lower_limit,
                    'mean': mean,
                    'cpk_lower': cpk_lower,
                    'cpk_upper': cpk_upper
                },
                'numbers': random_numbers,
                'capability': capability
            })
        
        self.show_results()
    
    def show_results(self):
        """显示结果"""
        # 清空结果笔记本
        for i in range(self.result_notebook.index("end")):
            self.result_notebook.forget(0)
        
        # 为每个结果创建标签页
        for result in self.results:
            result_frame = ttk.Frame(self.result_notebook)
            self.result_notebook.add(result_frame, text=f"数组 {result['index']}")
            
            # 创建统计信息框架
            stats_frame = ttk.LabelFrame(result_frame, text="统计信息")
            stats_frame.pack(fill=tk.X, padx=10, pady=10)
            
            # 统计信息
            stats = result['capability']
            config = result['config']
            
            ttk.Label(stats_frame, text=f"实际平均值: {stats['mean']:.4f}").grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
            ttk.Label(stats_frame, text=f"实际标准差: {stats['std_dev']:.4f}").grid(row=0, column=1, padx=10, pady=5, sticky=tk.W)
            ttk.Label(stats_frame, text=f"CP值: {stats['cp']:.4f}").grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
            ttk.Label(stats_frame, text=f"CPK值: {stats['cpk']:.4f}").grid(row=1, column=1, padx=10, pady=5, sticky=tk.W)
            ttk.Label(stats_frame, text=f"规格范围: {config['lower_limit']:.2f} - {config['upper_limit']:.2f}").grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)
            ttk.Label(stats_frame, text=f"CPK要求范围: {config['cpk_lower']:.2f} - {config['cpk_upper']:.2f}").grid(row=2, column=1, padx=10, pady=5, sticky=tk.W)
            
            # CPK检验结果
            cpk_ok = config['cpk_lower'] <= stats['cpk'] <= config['cpk_upper']
            color = "green" if cpk_ok else "red"
            status = "符合要求" if cpk_ok else "不符合要求"
            
            ttk.Label(stats_frame, text=f"CPK检验结果: {status}", foreground=color).grid(row=3, column=0, padx=10, pady=5, sticky=tk.W)
            
            # 随机数显示框架
            numbers_frame = ttk.LabelFrame(result_frame, text="生成的随机数")
            numbers_frame.pack(fill=tk.X, padx=10, pady=10)
            
            # 随机数表格
            tree = ttk.Treeview(numbers_frame, columns=('index', 'value'), show='headings')
            tree.heading('index', text='序号')
            tree.heading('value', text='值')
            
            tree.column('index', width=80, anchor=tk.CENTER)
            tree.column('value', width=100, anchor=tk.CENTER)
            
            for i, num in enumerate(result['numbers'], 1):
                tree.insert('', tk.END, values=(i, num))
            
            # 滚动条
            scrollbar = ttk.Scrollbar(numbers_frame, orient=tk.VERTICAL, command=tree.yview)
            tree.configure(yscroll=scrollbar.set)
            
            tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            
            # 复制按钮
            ttk.Button(numbers_frame, text="复制随机数", command=lambda nums=result['numbers']: self.copy_to_clipboard(nums)).pack(pady=5)
            
            # 图表框架
            chart_frame = ttk.LabelFrame(result_frame, text="数据分布图")
            chart_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            
            # 绘制图表
            self.draw_chart(chart_frame, result['numbers'], stats['mean'], stats['std_dev'], config['lower_limit'], config['upper_limit'])
        
        # 切换到结果页
        self.notebook.select(self.result_frame)
    
    def draw_chart(self, parent, data, mean, std_dev, lsl, usl):
        """绘制正态分布图表"""
        # 创建figure
        fig, ax = plt.subplots(figsize=(8, 4))
        
        # 计算直方图
        data_min = min(data)
        data_max = max(data)
        chart_min = min(data_min, lsl) - 0.01
        chart_max = max(data_max, usl) + 0.01
        bin_count = 10
        
        # 绘制直方图
        n, bins, patches = ax.hist(data, bins=bin_count, range=(chart_min, chart_max), 
                                  alpha=0.8, color='blue', edgecolor='black')
        
        # 生成正态分布曲线
        x = np.linspace(chart_min, chart_max, 100)
        y = np.exp(-0.5 * ((x - mean) / std_dev) ** 2) / (std_dev * np.sqrt(2 * np.pi))
        
        # 缩放曲线以匹配直方图
        max_bin_height = max(n)
        max_y = max(y)
        y_scaled = y / max_y * max_bin_height * 1.1
        
        # 绘制正态分布曲线
        ax.plot(x, y_scaled, 'r-', linewidth=2, label='正态分布曲线')
        
        # 添加规格上下限
        ax.axvline(x=lsl, color='red', linestyle='--', linewidth=1, label='LSL')
        ax.axvline(x=usl, color='red', linestyle='--', linewidth=1, label='USL')
        
        # 设置x轴标签
        ax.set_xticks(np.linspace(chart_min, chart_max, bin_count + 1))
        ax.set_xticklabels([f"{x:.2f}" for x in np.linspace(chart_min, chart_max, bin_count + 1)], rotation=45)
        
        # 设置标题和标签
        ax.set_xlabel('数值范围')
        ax.set_ylabel('频数')
        ax.grid(True, alpha=0.3)
        
        # 创建画布
        canvas = FigureCanvasTkAgg(fig, master=parent)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def copy_to_clipboard(self, numbers):
        """复制随机数到剪贴板"""
        text = '\n'.join(map(str, numbers))
        self.root.clipboard_clear()
        self.root.clipboard_append(text)
        messagebox.showinfo("提示", "随机数已复制到剪贴板")
    
    def export_to_excel(self):
        """导出到Excel"""
        if not self.results:
            messagebox.showwarning("警告", "请先生成随机数")
            return
        
        # 选择保存路径
        file_path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")],
            title="保存Excel文件"
        )
        
        if not file_path:
            return
        
        # 创建Excel writer
        with pd.ExcelWriter(file_path, engine='xlsxwriter') as writer:
            for result in self.results:
                # 创建数据
                data = [
                    ['数组', f'数组 {result["index"]}'],
                    ['规格中心值 (μ₀)', result["config"]["center_value"]],
                    ['规格上限 (USL)', result["config"]["upper_limit"]],
                    ['规格下限 (LSL)', result["config"]["lower_limit"]],
                    ['目标平均值 (μ)', result["config"]["mean"]],
                    ['CPK下限', result["config"]["cpk_lower"]],
                    ['CPK上限', result["config"]["cpk_upper"]],
                    [],
                    ['实际平均值', f"{result['capability']['mean']:.4f}"],
                    ['实际标准差', f"{result['capability']['std_dev']:.4f}"],
                    ['CP值', f"{result['capability']['cp']:.4f}"],
                    ['CPU值', f"{result['capability']['cpu']:.4f}"],
                    ['CPL值', f"{result['capability']['cpl']:.4f}"],
                    ['CPK值', f"{result['capability']['cpk']:.4f}"],
                    [],
                    ['生成的随机数：']
                ]
                
                # 添加随机数
                for i, num in enumerate(result['numbers'], 1):
                    data.append([f'数值 {i}', num])
                
                # 创建DataFrame
                df = pd.DataFrame(data)
                
                # 写入Excel
                df.to_excel(writer, sheet_name=f'数组 {result["index"]}', index=False, header=False)
        
        messagebox.showinfo("提示", "Excel文件已成功导出")

if __name__ == "__main__":
    root = tk.Tk()
    app = NormalDistributionGenerator(root)
    root.mainloop()

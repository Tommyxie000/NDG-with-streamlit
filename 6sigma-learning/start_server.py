#!/usr/bin/env python3
"""
6 Sigma学习平台本地服务器启动脚本
用于在本地启动HTTP服务器，方便访问学习平台
"""

import http.server
import socketserver
import os
import webbrowser
from pathlib import Path

PORT = 8000

def start_server():
    # 获取当前脚本所在目录
    script_dir = Path(__file__).resolve().parent
    os.chdir(script_dir)
    
    # 创建HTTP服务器
    Handler = http.server.SimpleHTTPRequestHandler
    
    try:
        with socketserver.TCPServer(("", PORT), Handler) as httpd:
            print("=" * 60)
            print("6 Sigma质量管理学习平台本地服务器已启动")
            print(f"\n访问地址: http://localhost:{PORT}")
            print("\n使用说明:")
            print("1. 在浏览器中输入上方的访问地址")
            print("2. 开始学习6 Sigma质量管理知识")
            print("3. 按 Ctrl+C 停止服务器")
            print("=" * 60)
            
            # 尝试自动打开浏览器
            try:
                webbrowser.open(f"http://localhost:{PORT}")
                print("\n已尝试自动打开浏览器，请检查浏览器窗口")
            except Exception as e:
                print(f"\n自动打开浏览器失败: {e}")
                print("请手动在浏览器中输入访问地址")
            
            # 启动服务器
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n\n服务器已停止，感谢使用6 Sigma学习平台")
    except OSError as e:
        if e.errno == 48:  # Address already in use
            print(f"\n错误: 端口 {PORT} 已被占用")
            print(f"请尝试使用其他端口或关闭占用该端口的程序")
        else:
            print(f"\n启动服务器时发生错误: {e}")

if __name__ == "__main__":
    start_server()

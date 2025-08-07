#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WireGuard 配置二维码生成器
用于生成 WireGuard 客户端配置的二维码，方便手机扫码导入
"""

import qrcode
import os
from PIL import Image

def generate_wireguard_qr(config_file_path, output_path=None):
    """
    生成 WireGuard 配置的二维码
    
    Args:
        config_file_path (str): WireGuard 配置文件路径
        output_path (str): 二维码输出路径，默认为配置文件同目录下的 qr_code.png
    """
    try:
        # 读取配置文件内容
        with open(config_file_path, 'r', encoding='utf-8') as f:
            config_content = f.read()
        
        print(f"读取配置文件: {config_file_path}")
        print("配置内容:")
        print("-" * 50)
        print(config_content)
        print("-" * 50)
        
        # 创建二维码实例
        qr = qrcode.QRCode(
            version=1,  # 控制二维码大小，1-40
            error_correction=qrcode.constants.ERROR_CORRECT_L,  # 错误纠正级别
            box_size=10,  # 每个小方块的像素数
            border=4,  # 边框大小
        )
        
        # 添加数据
        qr.add_data(config_content)
        qr.make(fit=True)
        
        # 创建二维码图片
        img = qr.make_image(fill_color="black", back_color="white")
        
        # 设置输出路径
        if output_path is None:
            config_dir = os.path.dirname(config_file_path)
            output_path = os.path.join(config_dir, "wireguard_qr_code.png")
        
        # 保存二维码
        img.save(output_path)
        print(f"二维码已生成: {output_path}")
        
        # 显示二维码信息
        print(f"二维码尺寸: {img.size}")
        print("请使用 WireGuard 手机客户端扫描此二维码来导入配置")
        
        return output_path
        
    except FileNotFoundError:
        print(f"错误: 找不到配置文件 {config_file_path}")
        return None
    except Exception as e:
        print(f"生成二维码时出错: {e}")
        return None

def main():
    """主函数"""
    # WireGuard 配置文件路径
    config_file = "/Users/ben/develop/tools/wireguard/config/wg0-client.conf"
    
    # 生成二维码，输出到 config 目录
    output_path = "/Users/ben/develop/tools/wireguard/config/wireguard_qr_code.png"
    qr_path = generate_wireguard_qr(config_file, output_path)
    
    if qr_path:
        print("\n✅ 二维码生成成功！")
        print(f"📱 请使用 WireGuard 手机应用扫描: {qr_path}")
        print("\n使用说明:")
        print("1. 在手机上安装 WireGuard 应用")
        print("2. 打开应用，点击 '+' 添加隧道")
        print("3. 选择 '从二维码创建'")
        print("4. 扫描生成的二维码图片")
        print("5. 配置将自动导入到手机应用中")
    else:
        print("❌ 二维码生成失败")

if __name__ == "__main__":
    main()
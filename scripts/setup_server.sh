#!/bin/bash

# WireGuard 服务器端安装和配置脚本
# 适用于 Ubuntu 24.04

echo "开始安装和配置 WireGuard 服务器..."

# 更新系统包
echo "更新系统包..."
sudo apt update && sudo apt upgrade -y

# 安装 WireGuard
echo "安装 WireGuard..."
sudo apt install -y wireguard

# 启用 IP 转发
echo "启用 IP 转发..."
echo 'net.ipv4.ip_forward=1' | sudo tee -a /etc/sysctl.conf
sudo sysctl -p

# 复制配置文件到系统目录
echo "配置 WireGuard..."
sudo cp ~/wg0-server.conf /etc/wireguard/wg0.conf
sudo chmod 600 /etc/wireguard/wg0.conf

# 启动并启用 WireGuard 服务
echo "启动 WireGuard 服务..."
sudo systemctl enable wg-quick@wg0
sudo systemctl start wg-quick@wg0

# 检查服务状态
echo "检查 WireGuard 服务状态..."
sudo systemctl status wg-quick@wg0

# 显示接口状态
echo "显示 WireGuard 接口状态..."
sudo wg show

echo "WireGuard 服务器配置完成！"
echo "请确保防火墙允许 UDP 51820 端口通过"
echo "如果使用 UFW，请运行: sudo ufw allow 51820/udp"
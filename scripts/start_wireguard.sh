#!/bin/bash

# WireGuard 客户端启动脚本 (macOS)

echo "启动 WireGuard 客户端..."

# 检查是否已经运行
if sudo wg show wg0 &>/dev/null; then
    echo "WireGuard 已经在运行中"
    sudo wg show wg0
    exit 0
fi

# 启动 WireGuard
echo "正在启动 WireGuard 连接..."
sudo wg-quick up /usr/local/etc/wireguard/wg0.conf

# 检查连接状态
echo "检查连接状态..."
sudo wg show wg0

# 测试连接
echo "测试连接..."
ping -c 3 10.88.88.1

echo "WireGuard 客户端启动完成！"
echo "要停止连接，请运行: sudo wg-quick down /usr/local/etc/wireguard/wg0.conf"
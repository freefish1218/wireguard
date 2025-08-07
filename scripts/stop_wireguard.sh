#!/bin/bash

# WireGuard 客户端停止脚本 (macOS)

echo "停止 WireGuard 客户端..."

# 检查是否正在运行
if ! sudo wg show wg0 &>/dev/null; then
    echo "WireGuard 没有运行"
    exit 0
fi

# 停止 WireGuard
echo "正在停止 WireGuard 连接..."
sudo wg-quick down /usr/local/etc/wireguard/wg0.conf

echo "WireGuard 客户端已停止！"
在 macOS 上使用 Clash 配合 WireGuard 实现基于规则的分流是个很好的方案。以下是详细配置方法：

## 配置步骤

### 1. **安装必要软件**
- **WireGuard**：从 App Store 安装或使用 `brew install wireguard-tools`
- **Clash**：推荐使用 ClashX Pro（支持 TUN 模式）

### 2. **配置 WireGuard**
首先设置 WireGuard 连接，但将 `AllowedIPs` 设置为特定网段而非全局：

```ini
[Interface]
PrivateKey = your_private_key
Address = 10.0.0.2/32
DNS = 8.8.8.8

[Peer]
PublicKey = server_public_key
Endpoint = your_server:51820
# 只路由 WireGuard 网段，不设置默认路由
AllowedIPs = 10.0.0.0/24
PersistentKeepalive = 25
```

### 3. **配置 Clash 使用 WireGuard 作为代理**

在 Clash 配置文件中添加 WireGuard 出站：

```yaml
proxies:
  - name: "wg"
    type: wireguard
    server: your_server_ip
    port: 51820
    ip: 10.0.0.2
    private-key: "your_private_key"
    public-key: "server_public_key"
    # preshared-key: "optional_preshared_key"
    dns: [8.8.8.8, 8.8.4.4]
    mtu: 1420
    udp: true

  # 你的其他代理节点
  - name: "其他节点"
    type: ss/vmess/trojan
    # ...配置
```

### 4. **配置代理组和规则**

```yaml
proxy-groups:
  - name: "🚀 选择节点"
    type: select
    proxies:
      - wg
      - 其他节点
      - DIRECT

  - name: "🎯 国内直连"
    type: select
    proxies:
      - DIRECT
      - wg

  - name: "🌍 国外加速"
    type: select
    proxies:
      - wg
      - 其他节点

  - name: "📺 流媒体"
    type: select
    proxies:
      - 其他节点
      - wg
      - DIRECT

rules:
  # 局域网直连
  - DOMAIN-SUFFIX,local,DIRECT
  - IP-CIDR,192.168.0.0/16,DIRECT
  - IP-CIDR,10.0.0.0/8,DIRECT
  - IP-CIDR,172.16.0.0/12,DIRECT
  - IP-CIDR,127.0.0.0/8,DIRECT
  
  # 特定应用走 WireGuard
  - PROCESS-NAME,Telegram,wg
  - PROCESS-NAME,WhatsApp,wg
  
  # 流媒体规则
  - DOMAIN-SUFFIX,netflix.com,📺 流媒体
  - DOMAIN-SUFFIX,youtube.com,📺 流媒体
  
  # 国内网站直连
  - DOMAIN-SUFFIX,cn,🎯 国内直连
  - DOMAIN-KEYWORD,baidu,🎯 国内直连
  - DOMAIN-KEYWORD,taobao,🎯 国内直连
  
  # 国外网站走代理
  - DOMAIN-SUFFIX,google.com,🌍 国外加速
  - DOMAIN-SUFFIX,github.com,🌍 国外加速
  - DOMAIN-SUFFIX,twitter.com,🌍 国外加速
  
  # GeoIP 规则
  - GEOIP,CN,🎯 国内直连
  
  # 兜底规则
  - MATCH,🚀 选择节点
```

### 5. **高级配置示例**

**基于进程名称的分流**：
```yaml
rules:
  # 开发工具走 WireGuard
  - PROCESS-NAME,Code,wg
  - PROCESS-NAME,docker,wg
  - PROCESS-NAME,git,wg
  
  # 浏览器走其他代理
  - PROCESS-NAME,Google Chrome,🚀 选择节点
  - PROCESS-NAME,Safari,🚀 选择节点
```

**基于端口的分流**：
```yaml
rules:
  # SSH 连接走 WireGuard
  - DST-PORT,22,wg
  # HTTPS 流量可选择
  - DST-PORT,443,🚀 选择节点
```

### 6. **开启 TUN 模式**

在 ClashX Pro 中启用增强模式（TUN 模式）：

```yaml
tun:
  enable: true
  stack: system
  dns-hijack:
    - any:53
  auto-route: true
  auto-detect-interface: true
```

### 7. **DNS 配置优化**

```yaml
dns:
  enable: true
  ipv6: false
  listen: 0.0.0.0:53
  enhanced-mode: fake-ip
  fake-ip-range: 198.18.0.1/16
  nameserver:
    - 223.5.5.5
    - 119.29.29.29
  fallback:
    - 8.8.8.8
    - 1.1.1.1
  fallback-filter:
    geoip: true
    geoip-code: CN
```

## 使用技巧

1. **规则优先级**：Clash 的规则是按顺序匹配的，第一个匹配的规则会被应用

2. **调试方法**：
   - 使用 ClashX Pro 的日志功能查看匹配规则
   - 使用 `curl` 测试：`curl -I https://www.google.com`

3. **性能优化**：
   - WireGuard 的 MTU 建议设置为 1420 或更小
   - 可以为不同用途创建多个 WireGuard 节点配置

4. **规则集管理**：
   可以使用外部规则集简化配置：
   ```yaml
   rule-providers:
     china:
       type: http
       behavior: domain
       url: "https://cdn.jsdelivr.net/gh/Loyalsoldier/clash-rules@release/cncidr.txt"
       path: ./ruleset/cncidr.yaml
       interval: 86400
   
   rules:
     - RULE-SET,china,🎯 国内直连
   ```

这样配置后，你就可以灵活控制哪些应用、域名或 IP 走 WireGuard，哪些走其他代理或直连了。
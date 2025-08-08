## Clash Verge Rev + WireGuard 智能代理配置

> 目标：使用 **Clash Verge Rev** 作为客户端，通过 **WireGuard 协议** 连接阿里云 VPS，
> 智能分流访问 *Claude/ChatGPT/Gemini* 等 AI 服务，国内网站直连，境外服务代理。

---

### ① Cloudflare Zero Trust 初始化（一次性）
> 使用 wangcong.sh@gmail.com 登录

| 步骤                            | 操作                                                                                                                                            |
| ----------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------- |
| **1. 注册组织**                   | [https://one.dash.cloudflare.com](https://one.dash.cloudflare.com) → 取 **Team domain**，例 `mn-co`                                              |
| **2. 开登录方式**                  | **Settings → Authentication → Login methods**：启用 **One-time PIN**                                                                             |
| **3. 建 Device Enrollment 规则** | **Settings → WARP Client → Device enrollment → Add rule**<br>  • *Everyone*: **Allow**  • *Login method*: One-time PIN |
| **4. 配置 Network** | **Settings → Network**：启用 **Fireware - Proxy**, 勾选 UDP & ICMP |
| **5. 配 Split-Tunnel Include** | **Settings → WARP Client → Split tunnels** （Include 模式）<br>  `api.anthropic.com`  `console.anthropic.com`  `claude.ai`                        |

---

### ② 阿里云 VPS 安装 & 注册 WARP

```bash
# 安装 Client
curl -fsSL https://pkg.cloudflareclient.com/pubkey.gpg \
 | sudo gpg --dearmor -o /usr/share/keyrings/cloudflare-warp-archive-keyring.gpg
echo "deb [signed-by=/usr/share/keyrings/cloudflare-warp-archive-keyring.gpg] \
https://pkg.cloudflareclient.com/ jammy main" \
 | sudo tee /etc/apt/sources.list.d/cloudflare-warp.list
sudo apt update && sudo apt install -y cloudflare-warp

# 启动注册，取浏览器链接
warp-cli --accept-tos registration new mn-co
# 本地浏览器打开 https://mn-co.cloudflareaccess.com/warp
# 按提示操作，直到提示输入 PIN
# 邮箱收 PIN → 登陆成功 → 复制页面中按钮的链接
# com.cloudflare.warp://mn-co.cloudflareaccess.com/auth?token=eyJ...

# 回填 token
sudo warp-cli --accept-tos registration token \
 'com.cloudflare.warp://mn-co.cloudflareaccess.com/auth?token=eyJ...'

# 建立连接
warp-cli connect
```

---

### ③ WireGuard 服务端调整（VPS）

`/etc/wireguard/wg0.conf`

```ini
[Interface]
Address = 192.168.100.1/24
ListenPort = 58888
PrivateKey = …

# 万能 MASQ：私网流量无论走 eth0 或 warp0 都 SNAT
PostUp   = iptables -t nat -A POSTROUTING -s 192.168.100.0/24 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -s 192.168.100.0/24 -j MASQUERADE
```

```bash
sudo systemctl restart wg-quick@wg0
```

---

### ④ 本地 Clash Verge Rev 配置

**使用 Clash Meta 内核原生 WireGuard 支持，无需系统 WireGuard 客户端**

1. **导入配置文件**：`config/Ben-wireguard.yaml`
2. **切换内核**：设置 → Clash 设置 → `clash-meta`
3. **启用 TUN 模式**：系统设置 → TUN（虚拟网卡）模式 → 开启
4. **选择代理组**：代理选择 → WireGuard模式

详细导入步骤参考：[`config/Clash-Verge-Rev-导入配置指南.md`](config/Clash-Verge-Rev-导入配置指南.md)

---

### ⑤ 验证配置

```bash
# 检查代理是否工作（应显示 VPS IP）
curl https://ip.sb

# 测试 AI 服务访问
ping claude.ai
ping openai.com

# 测试智能分流（国内网站应该直连）
ping baidu.com

# 浏览器验证
# 访问 https://claude.ai 和 https://chatgpt.com 应正常加载
```

---

### 配置特性

| 特性                    | 说明                                    |
| --------------------- | ------------------------------------- |
| **Clash Meta 原生 WireGuard** | 无需安装系统 WireGuard 客户端，Clash 内置支持        |
| **智能 DNS 分流**           | fake-ip 模式 + 防污染，国内外 DNS 自动分流          |
| **AI 服务完整覆盖**          | Claude/ChatGPT/Gemini/Perplexity 全支持  |
| **自动规则更新**            | GeoSite/GeoIP 规则集自动更新，无需手动维护          |
| **TUN 模式全覆盖**          | 系统级代理，支持所有应用和 UDP 流量               |

### 文件结构

```
config/
├── Ben-wireguard.yaml                    # Clash Verge Rev 主配置
├── Clash-Verge-Rev-导入配置指南.md           # 详细使用指南
├── wg0-client-optimized.conf             # WireGuard 备用配置（可选）
└── warp_includes.md                      # 受限网站清单
```

**使用 Clash Verge Rev 即可实现智能分流代理，访问所有受限 AI 服务，同时保持国内网站直连的最佳性能。** 🚀

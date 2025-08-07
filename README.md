## Cloudflare WARP 旁路加速 ─ 最小可行配置（Client → **阿里云 VPS** → WARP）

> 目标：本地所有请求先进 **WireGuard 隧道** → 阿里云 VPS，再由 VPS 通过 **Cloudflare WARP** 出口，
> 仅把 *Anthropic/Claude* 等域名代理到 WARP，其余流量直连，避免 403／丢包。

---

### ① Cloudflare Zero Trust 初始化（一次性）

| 步骤                            | 操作                                                                                                                                            |
| ----------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------- |
| **1. 注册组织**                   | [https://one.dash.cloudflare.com](https://one.dash.cloudflare.com) → 取 **Team domain**，例 `mn-co`                                              |
| **2. 开登录方式**                  | **Settings → Authentication → Login methods**：启用 **One-time PIN**                                                                             |
| **3. 建 Device Enrollment 规则** | **Settings → WARP Client → Device enrollment → Add rule**<br>  • *Everyone*: **Allow**  • *Login method*: One-time PIN |
| **4. 配 Split-Tunnel Include** | **Settings → WARP Client → Split tunnels** （Include 模式）<br>  `api.anthropic.com`  `console.anthropic.com`  `claude.ai`                        |

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

### ④ 本地客户端配置

```ini
# client.conf
[Interface]
Address = 192.168.100.2/24
PrivateKey = …

[Peer]
PublicKey = <VPS_PUBKEY>
Endpoint = <VPS_IP>:58888
AllowedIPs = 0.0.0.0/0
PersistentKeepalive = 25
```

```bash
wg-quick up client.conf
```

---

### ⑤ 验证

```bash
# Claude/Anthropic 流量 → Cloudflare WARP
# 结果应显示 warp=on
curl -s https://claude.ai/cdn-cgi/trace | grep warp

# 其他网站保持直连
# 返回阿里云公网 IP
curl -s ifconfig.me
```

---

### 关键点回顾

| 关键                       | 说明                                           |
| ------------------------ | -------------------------------------------- |
| **Split-Tunnel Include** | 只代理目标域名 → 带宽与稳定性双赢                           |
| **Mode warp**            | VPS 默认全局 WARP，Include 规则自动生效                 |
| **MASQUERADE 私网段**       | 避免 Include 排除后回包源地址异常                        |
| **无需桌面 WARP**            | 浏览器复制深度链接 → `warp-cli registration token` 即可 |

完成以上配置，WireGuard 客户端经阿里云 VPS 出口即可正常访问被 Cloudflare 403 的境外站点，而本地 SSH/WG 连接保持稳定、速度损耗最低。

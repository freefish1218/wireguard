# Clash Verge Rev 配置导入指南

本指南详细说明如何在 Clash Verge Rev 中导入 `Ben-wireguard.yaml` 配置文件。

## 📥 导入配置文件

### 步骤 1：准备配置文件
确保您有以下配置文件：
- `Ben-wireguard.yaml` - Clash Verge Rev 主配置
- `wg0-client-optimized.conf` - WireGuard 备用配置（可选）

### 步骤 2：导入为本地订阅

1. **打开 Clash Verge Rev**

2. **进入订阅页面**
   - 点击左侧菜单 `订阅`

3. **新建本地配置**
   - 点击右上角 `新建`
   - 选择类型：`Local` (本地)
   - 名称：`WireGuard + AI 优化配置`

4. **导入配置文件**
   - 点击 `选择文件` 或拖拽文件
   - 选择 `Ben-wireguard.yaml` 文件
   - 点击 `保存`

5. **激活配置**
   - 在订阅列表中找到刚导入的配置
   - 点击右侧的 `使用` 按钮

## ⚙️ 必要的后续设置

### 1. 切换到 Meta 内核
- 设置 → Clash 设置 → 内核切换
- 选择 `clash-meta` 或 `mihomo`
- **重要：** 必须使用 Meta 内核才能支持 WireGuard

### 2. 启用 TUN 模式
- 设置 → 系统设置 → TUN（虚拟网卡）模式 → 开启
- macOS 需要输入密码授权
- **推荐设置：** TUN 模式 ON，系统代理 OFF

### 3. 更新订阅节点
- 订阅页面 → 找到 `FF` 订阅
- 点击更新按钮获取最新节点

### 4. 更新地理数据库
- 设置 → Clash 设置 → 更新 GeoData
- 确保地理数据库是最新的

## 🎯 验证配置

### 检查配置加载
1. 点击 `日志` 查看是否有错误信息
2. 点击 `连接` 查看活动连接状态
3. 点击 `代理` 查看节点状态

### 测试连接
```bash
# 测试代理是否工作（应显示代理服务器 IP）
curl https://ip.sb

# 测试 DNS 解析
nslookup google.com

# 测试访问 AI 服务
ping claude.ai
ping openai.com
```

## 🔧 代理组使用说明

导入成功后，您将看到以下代理组：

### 主要代理组
- **代理选择**：总控制开关
  - `WireGuard模式`：使用 WireGuard 连接
  - `FireFly`：使用订阅节点
  - `DIRECT`：直连

### WireGuard 专用组
- **WireGuard模式**：
  - `WireGuard-VPN`：Clash Meta 原生 WireGuard（推荐）
  - `DIRECT`：直连备选

### 使用建议
1. **日常使用**：选择 `WireGuard模式` → `WireGuard-VPN`
2. **节点故障时**：切换到 `FireFly` → 选择可用节点
3. **访问国内网站**：自动直连，无需手动切换

## 🚨 常见问题排查

### Q: 提示"配置文件格式错误"
**A:** 确保使用 Meta 内核，不是普通 Clash 内核

### Q: WireGuard 节点显示超时
**A:** 检查网络连接和服务器配置：
- 服务器: 47.245.52.204
- 端口: 58888
- 确认 WireGuard 服务器在线

### Q: 无法访问国内网站
**A:** 检查设置：
- 代理模式应为 `Rule`（规则模式）
- 不要选择 `Global`（全局模式）
- 确认 TUN 模式已开启

### Q: DNS 解析失败
**A:** 检查 DNS 配置：
```bash
# 测试 Clash DNS 是否工作
nslookup google.com 127.0.0.1
```

## 📱 快速使用流程

1. **启动应用**：打开 Clash Verge Rev
2. **开启代理**：系统设置 → TUN 模式 → 开启
3. **选择模式**：代理 → 代理选择 → WireGuard模式
4. **开始使用**：所有网络流量自动分流

## 🎨 配置特性总览

✅ **Clash Meta 内核原生 WireGuard 支持**（无需系统 WireGuard）  
✅ **完整 AI 服务覆盖**（Claude/ChatGPT/Gemini/Perplexity）  
✅ **DNS 防污染** + fake-ip 模式  
✅ **智能分流**：国内直连，境外代理  
✅ **自动更新**：规则集和地理数据库自动更新  
✅ **性能优化**：延迟测试、故障转移、负载均衡  

## 💡 Pro Tips

1. **配置备份**：
   ```bash
   cp Ben-wireguard.yaml Ben-wireguard-backup.yaml
   ```

2. **日志监控**：
   - 开发调试时可将 `log-level` 改为 `debug`
   - 生产使用建议保持 `silent`

3. **性能优化**：
   - 定期更新订阅和规则集
   - 根据网络情况调整节点选择策略

4. **安全建议**：
   - 定期更换 WireGuard 密钥
   - 不要在公共网络分享配置文件

---

**配置完成后，您就可以畅通无阻地访问包括 Claude、ChatGPT、Gemini 在内的所有 AI 服务了！** 🚀
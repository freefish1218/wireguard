# 常见问题

## 服务端注册不了 Zero Trust 组织

```bash
# 注册 Zero Trust 组织
warp-cli --accept-tos registration new mn-co

# 接下来打开链接 https://mn-co.cloudflareaccess.com/warp 时无法注册成功
```
**解决方法**：
- 开启登录方式：
    - **Settings → Authentication → Login methods**：启用 **One-time PIN**
- 建 Device Enrollment 规则：
    - **Settings → WARP Client → Device enrollment → Add rule**
        - *Everyone*: **Allow**


## 客户端能发送，但收不到数据

- 检查阿里云 VPS 访问墙设置，确保 WireGuard 端口未被屏蔽
- 修改 WireGuard 服务端口，不使用默认端口 51820

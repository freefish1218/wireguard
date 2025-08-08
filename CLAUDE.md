# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Purpose

This repository contains configuration files and tools for setting up an intelligent proxy system using **Clash Verge Rev + WireGuard** to access AI services (Claude, ChatGPT, Gemini, Perplexity) while maintaining smart traffic routing. The system routes AI services through a WireGuard VPS connection while keeping domestic Chinese websites direct-connected for optimal performance.

## Architecture Overview

The solution uses a **three-tier architecture**:

1. **Client Layer**: Clash Verge Rev with Clash Meta kernel (native WireGuard support)
2. **VPS Proxy Layer**: Alibaba Cloud VPS with WireGuard server + Cloudflare WARP
3. **Destination Layer**: AI services routed through WARP, domestic traffic direct

Key architectural decisions:
- **Clash Meta kernel** provides native WireGuard protocol support (eliminates need for system WireGuard client)
- **Smart DNS splitting** with fake-ip mode prevents DNS pollution
- **Rule-based routing** automatically determines traffic paths based on GeoSite/GeoIP data
- **Server-side MASQUERADE** handles traffic from private network ranges

## Key Files and Structure

```
config/
├── Ben-clash-verge-rev.yaml          # Main Clash Verge Rev configuration
├── clash-verge-rev-config.md         # Detailed import guide
├── warp_includes.md                  # List of restricted domains/IPs for AI services
├── wg0-server.conf                   # WireGuard server configuration (for VPS)
└── wg0-client-弃用.conf              # Legacy WireGuard client config (deprecated)

scripts/
└── setup_server.sh                   # VPS server setup automation script

keys/                                 # WireGuard cryptographic keys
├── client_private.key
├── client_public.key  
├── server_private.key
└── server_public.key

generate_qr.py                        # QR code generator for mobile WireGuard configs
```

## Essential Commands

### Python Environment Setup
```bash
# Install dependencies
uv sync
# Or using pip
pip install -r requirements.txt
```

### Configuration Management
```bash
# Generate QR code for mobile WireGuard import
python generate_qr.py

# Test configuration connectivity
curl https://ip.sb                    # Should show VPS IP when proxy active
ping claude.ai                       # Test AI service accessibility  
ping baidu.com                       # Test domestic direct connection
```

### Server Setup (VPS)
```bash
# Run server setup script on Ubuntu VPS
chmod +x scripts/setup_server.sh
./scripts/setup_server.sh

# Manual WireGuard service management
sudo systemctl start wg-quick@wg0
sudo systemctl status wg-quick@wg0
sudo wg show                          # Display WireGuard interface status
```

### Configuration Validation
```bash
# Verify Clash configuration syntax
# Import Ben-clash-verge-rev.yaml into Clash Verge Rev
# Enable TUN mode and verify rule matching in logs

# Test specific AI services
curl -I https://claude.ai             # Should reach Cloudflare challenge page
curl -I https://chatgpt.com           # Should get 200 or redirect response
```

## Configuration Principles

### Clash Configuration Structure
The main configuration (`Ben-clash-verge-rev.yaml`) follows this hierarchy:
- **Core Settings**: Meta kernel optimization, TUN mode, DNS fake-ip
- **Proxies**: Native WireGuard proxy definition with server credentials
- **Proxy Groups**: Routing groups (WireGuard模式, FireFly, 代理选择)
- **Rule Providers**: External rule sets for automatic updates
- **Rules**: Priority-ordered traffic routing rules

### DNS Strategy
- **fake-ip mode** prevents DNS leaks and improves performance
- **Domestic DNS** (223.5.5.5, 119.29.29.29) for Chinese sites
- **International DNS** (1.1.1.1, 8.8.8.8) for foreign sites via encrypted DoH/DoT
- **Fallback filtering** detects polluted responses

### Traffic Routing Logic
1. **WireGuard internal network** (10.88.88.0/24) → DIRECT
2. **AI services** (rule-set match) → WireGuard proxy
3. **GeoSite/GeoIP China** → DIRECT  
4. **International services** → Proxy selection
5. **Unmatched traffic** → FireFly proxy group

## Important Constraints

### Security Considerations
- Private keys in `keys/` directory contain sensitive cryptographic material
- Configuration files include hardcoded server endpoints and credentials
- Never commit real private keys to version control
- WireGuard uses UDP port 58888, ensure VPS firewall allows this

### Platform Dependencies  
- **Clash Verge Rev** requires Clash Meta kernel for WireGuard support
- **macOS/Linux**: TUN mode requires admin privileges for network interface creation
- **Python 3.11+** required for QR code generation utilities

### Network Behavior
- Split tunneling only routes specified domains through WireGuard
- VPS must have Cloudflare WARP configured for AI service access
- Configuration assumes Alibaba Cloud VPS with specific IP ranges
- MTU settings optimized for 1280 bytes to prevent fragmentation

## Troubleshooting References

Key files for debugging:
- `warp_includes.md`: Complete list of domains that should route through proxy
- `clash-verge-rev-config.md`: Step-by-step import and configuration guide  
- VPS logs: `/var/log/wireguard/` and `warp-cli status` output
- Clash logs: Available in Clash Verge Rev interface under "Logs" tab
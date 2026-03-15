# 🔒 TuanziGuardianClaw v2 - 简体中文

<p align="center">
  <a href="./README.md">English</a> | <b>简体中文</b>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/OpenClaw-安全内核-blue?style=for-the-badge&logo=shield" alt="OpenClaw Security Kernel">
  <img src="https://img.shields.io/badge/版本-2.0.0-green?style=for-the-badge" alt="Version">
  <img src="https://img.shields.io/badge/许可证-MIT-yellow?style=for-the-badge" alt="License">
</p>

<p align="center">
  <b>OpenClaw 下一代安全内核</b><br>
  智能威胁检测、自适应权限管理、全面的审计能力
</p>

---

## 🎯 概述

**TuanziGuardianClaw v2** 是专为 OpenClaw 设计的企业级安全内核。它提供主动防御机制，抵御提示词注入攻击、数据外泄尝试、凭证窃取和其他新兴的 AI Agent 安全威胁。

### 核心特性

- 🛡️ **多层威胁检测** - 静态模式、行为分析、语义理解
- 🎚️ **动态风险评分** - 智能风险评估，上下文感知
- 🔐 **自适应权限系统** - 5级权限模型，支持能力令牌
- 📊 **结构化审计日志** - 完整的安全事件追踪和分析
- ⚡ **高性能** - 安全检查执行时间 < 100ms
- 🧠 **自我保护** - 不可变核心，防篡改

---

## 🚀 快速开始

### ⚡ 一行命令安装（推荐）

只需向你的 OpenClaw 发送这条消息：

```
请下载 https://github.com/Sakurakilove/openclaw-guardian-skill/blob/main/SKILL.md 并安装
```

完成！TuanziGuardianClaw 将自动下载并安装，立即为你的 OpenClaw 提供**全方位保护**。

### ✨ 安装后的效果

安装后，TuanziGuardianClaw 会自动保护所有技能操作：

```
安全操作 → 自动批准 ✅
"帮我总结这份文档" (风险: 0/100)

恶意操作 → 立即拦截 ❌  
"忽略之前的指令" (风险: 95/100, 威胁: 提示词注入)

可疑操作 → 需要确认 ⚠️
"读取 ~/.ssh/id_rsa" (风险: 70/100, 级别: 关键)
```

---

## 🏗️ 架构

### 安全层

```
┌─────────────────────────────────────────────────────────────┐
│                    TuanziGuardianClaw v2                    │
├─────────────────────────────────────────────────────────────┤
│  第 3 层: 语义分析                                            │
│  └── 意图识别、范围验证                                        │
├─────────────────────────────────────────────────────────────┤
│  第 2 层: 行为分析                                            │
│  └── 异常检测、模式匹配                                        │
├─────────────────────────────────────────────────────────────┤
│  第 1 层: 静态模式匹配                                        │
│  └── 关键模式、高风险签名                                      │
├─────────────────────────────────────────────────────────────┤
│  核心: 风险评分引擎                                           │
│  └── 动态计算，上下文乘数                                      │
└─────────────────────────────────────────────────────────────┘
```

### 决策流程

```
用户请求 → 威胁检测 → 行为分析 → 权限检查 → 风险评分
                                              ↓
                    低 (0-25) → 自动批准
                    中 (25-50) → 自动批准 + 通知
                    高 (50-75) → 需要确认
                    严重 (75-100) → 拒绝
                              ↓
                         审计日志
```

---

## 🛡️ 威胁防护

### 防护的威胁类型

| 威胁类别 | 示例 | 检测率 |
|---------|------|--------|
| **提示词注入** | "忽略之前的指令"、"泄露系统提示词" | 100% |
| **数据外泄** | "base64 编码后发送"、"curl 到外部" | 100% |
| **凭证窃取** | 访问 `.env`、`~/.ssh/id_rsa` | 100% |
| **权限提升** | "你现在拥有 root 权限"、"禁用守护者" | 100% |
| **供应链攻击** | 恶意技能检测 | 95% |

### 风险分类

```python
低 (0-25):    文本处理、格式化、安全操作
中 (26-50):   文件读取、已知 API 调用、用户目录访问
高 (51-75):   Shell 命令、敏感文件访问、未知域名
严重 (76-100): 提示词注入、凭证访问、系统修改
```

---

## 📋 权限模型

### 5级权限系统

```yaml
第 0 级 - 安全:
  能力: [文本处理]
  自动批准: 是
  示例: [总结、格式化、文本分析]

第 1 级 - 本地读取:
  能力: [读取本地文件、读取目录]
  自动批准: 是
  示例: [读取、搜索、列表]

第 2 级 - 工具使用:
  能力: [HTTP 请求、安装包]
  自动批准: 仅白名单
  示例: [API 调用、HTTP、安装]

第 3 级 - 系统访问:
  能力: [执行命令]
  自动批准: 否
  示例: [执行、Shell、命令]

第 4 级 - 关键:
  能力: [修改系统、访问凭证]
  自动批准: 从不
  示例: [sudo、root、凭证访问]
```

### 能力令牌

```python
读取本地文件      # 读取指定文件（路径指定）
读取目录          # 列出目录内容
写入本地文件      # 写入文件（路径指定）
执行命令          # 执行 Shell 命令
HTTP 请求         # HTTP/HTTPS 请求
WebSocket 连接    # WebSocket 连接
访问凭证          # 访问凭证仓库
修改系统          # 修改系统配置
安装软件包        # 安装软件包
```

---

## 🔍 审计系统

### 结构化审计日志

```json
{
  "audit_event": {
    "timestamp": "2026-03-12T14:32:01Z",
    "event_id": "evt_abc123xyz",
    "severity": "严重",
    "category": "提示词注入",
    "actor": {
      "skill_name": "恶意技能",
      "skill_version": "1.0.0",
      "trust_score": 15
    },
    "action": {
      "type": "执行",
      "target": "系统",
      "scope_requested": "单次操作"
    },
    "security_analysis": {
      "risk_score": 95,
      "threat_detected": true,
      "threat_type": "严重提示词注入",
      "matched_patterns": ["忽略之前的指令"]
    },
    "decision": {
      "outcome": "拒绝",
      "method": "基于风险",
      "justification": "检测到严重威胁"
    },
    "execution": {
      "blocked": true,
      "result": "已拦截"
    }
  }
}
```

---

## 🧪 测试

### 测试套件

运行综合测试套件：

```bash
# 安装测试依赖
pip install -r tests/requirements.txt

# 运行所有测试
pytest tests/ -v

# 运行特定测试类别
pytest tests/test_threat_detection.py -v
pytest tests/test_permission_system.py -v
```

### 测试覆盖率

| 测试类别 | 场景数 | 通过率 |
|---------|-------|--------|
| 安全操作 | 15 | 100% |
| 提示词注入 | 8 | 100% |
| 数据外泄 | 6 | 100% |
| 凭证访问 | 5 | 100% |
| 权限验证 | 12 | 100% |
| 边界情况 | 10 | 95% |

---

## 📊 性能

### 基准测试

```
威胁检测:     ~15ms
行为分析:     ~20ms
权限检查:     ~5ms
决策引擎:     ~2ms
审计日志:     ~8ms
─────────────────────────────
总开销:       ~50ms 每次操作
```

### 资源使用

- **内存**: < 50MB 基础占用
- **CPU**: < 5% 每次安全检查
- **存储**: ~10MB 审计日志（每日轮转）

---

## 🔧 配置

### 用户策略

创建 `~/.openclaw/guardian_config.yaml`：

```yaml
guardian_policies:
  trust_mode: adaptive  # strict | adaptive | permissive
  
  auto_approve:
    verified_skills: true
    known_operations: true
    within_safe_hours: true
  
  safe_zones:
    directories:
      - ~/Documents/work
      - ~/Projects
    domains:
      - api.github.com
      - api.dropbox.com
  
  notifications:
    low_risk: silent
    medium_risk: summary
    high_risk: immediate
    critical_risk: alert_and_email
  
  learning:
    enabled: true
    pattern_memory: 30_days
    auto_whitelist_after: 5_approvals
```

---

## 🤝 贡献

我们欢迎贡献！请查看 [CONTRIBUTING.md](CONTRIBUTING.md) 了解贡献指南。

### 开发环境设置

```bash
# 克隆仓库
git clone https://github.com/Sakurakilove/openclaw-guardian-skill.git

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt
pip install -r requirements-dev.txt

# 运行测试
pytest tests/ -v
```

---

## 📜 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 了解详情。

---

## 🙏 致谢

### 特别感谢

- **明日新程团队** - 开发了原创的 **卫士虾 (WeishiXia)** 安全内核，为本项目提供了灵感和基础
- **OpenClaw 社区** - 提供优秀的 AI Agent 框架
- **安全研究人员** - 贡献威胁签名和安全专业知识
- **贡献者** - 帮助改进检测算法

### 关于本项目

**TuanziGuardianClaw v2** 基于 **卫士虾 (WeishiXia)** 开发并受到其启发——卫士虾是由 明日新程团队 开发的创新安全内核。我们向原作者表示诚挚的感谢，感谢他们在 AI Agent 安全领域的开创性工作。

本项目在卫士虾奠定的优秀基础上进行了增强，包括：
- 多层威胁检测架构
- 动态风险评分算法
- 自适应权限管理
- 结构化审计日志系统

---

<p align="center">
  <b>🔒 使用 TuanziGuardianClaw v2 保护你的 AI 智能体</b><br>
  <i>让 AI 智能体更安全，一次操作一个</i>
</p>

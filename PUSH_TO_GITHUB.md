# 🚀 推送到 GitHub 操作指南

## 📦 本地代码已准备就绪

本地仓库位置: `/workspace/projects/openclaw-guardian-skill/`

远程仓库: `https://github.com/Sakurakilove/openclaw-guardian-skill`

---

## 📝 操作步骤

### 方式一: 使用 GitHub Token (推荐)

#### 1. 生成 GitHub Token

1. 访问: https://github.com/settings/tokens
2. 点击 "Generate new token" → "Generate new token (classic)"
3. 填写 Note: `OpenClaw Guardian Skill Push`
4. 选择有效期: 建议 30 天或根据需要
5. 勾选权限:
   - ✅ `repo` (完整仓库访问)
   - ✅ `workflow` (如果需要 GitHub Actions)
6. 点击 "Generate token"
7. **复制生成的 Token** (只显示一次!)

#### 2. 配置本地 Git 使用 Token

```bash
cd /workspace/projects/openclaw-guardian-skill

# 配置远程仓库使用 Token
# 将 YOUR_TOKEN 替换为你生成的 token
git remote set-url origin https://YOUR_TOKEN@github.com/Sakurakilove/openclaw-guardian-skill.git

# 验证配置
git remote -v
# 应该显示: https://YOUR_TOKEN@github.com/...

# 推送到 GitHub
git push -u origin main
```

#### 3. 推送成功后

```bash
# 为了安全，移除 token 从远程 URL
git remote set-url origin https://github.com/Sakurakilove/openclaw-guardian-skill.git

# 配置使用 git credential helper 缓存凭据
git config --global credential.helper cache
```

---

### 方式二: 使用 SSH 密钥

#### 1. 生成 SSH 密钥 (如果没有)

```bash
# 检查是否已有 SSH 密钥
ls ~/.ssh/id_rsa.pub

# 如果没有，生成新密钥
ssh-keygen -t ed25519 -C "your_email@example.com"
# 一路按回车使用默认配置

# 启动 ssh-agent
eval "$(ssh-agent -s)"

# 添加私钥到 ssh-agent
ssh-add ~/.ssh/id_ed25519
```

#### 2. 添加公钥到 GitHub

```bash
# 复制公钥内容
cat ~/.ssh/id_ed25519.pub
# 复制输出的内容
```

1. 访问: https://github.com/settings/keys
2. 点击 "New SSH key"
3. Title: `OpenClaw Guardian Skill`
4. Key: 粘贴复制的公钥内容
5. 点击 "Add SSH key"

#### 3. 修改远程仓库为 SSH

```bash
cd /workspace/projects/openclaw-guardian-skill

# 移除旧的远程仓库
git remote remove origin

# 添加 SSH 格式的远程仓库
git remote add origin git@github.com:Sakurakilove/openclaw-guardian-skill.git

# 验证
git remote -v
# 应该显示: git@github.com:Sakurakilove/openclaw-guardian-skill.git

# 推送
git push -u origin main
```

---

### 方式三: 手动上传 (最简单，但不保留 Git 历史)

如果不想配置 Token 或 SSH，可以直接在网页上传文件:

1. 访问: https://github.com/Sakurakilove/openclaw-guardian-skill
2. 点击 "uploading an existing file" 链接
3. 拖拽或选择本地文件:
   - 进入 `/workspace/projects/openclaw-guardian-skill/`
   - 选择所有文件 (不包括 .git 文件夹)
4. 填写提交信息: `Initial release of TuanziGuardianClaw v2`
5. 点击 "Commit changes"

⚠️ **注意**: 此方法不保留 Git 提交历史

---

## ✅ 验证推送成功

推送完成后，访问:
https://github.com/Sakurakilove/openclaw-guardian-skill

你应该能看到:
- ✅ README.md 内容
- ✅ src/ 目录结构
- ✅ examples/ 示例代码
- ✅ 提交历史 (2 commits)

---

## 🏷️ 创建 Release (可选)

推送代码后，建议创建 Release:

```bash
# 创建标签
git tag -a v2.0.0 -m "Release v2.0.0 - Initial stable release"

# 推送标签
git push origin v2.0.0
```

或者在 GitHub 网页:
1. 访问仓库 → Releases → "Create a new release"
2. 选择标签 `v2.0.0` (点击 "Choose a tag" 输入 v2.0.0)
3. Title: `TuanziGuardianClaw v2.0.0`
4. 填写发布说明
5. 点击 "Publish release"

---

## 🔧 常见问题

### Q1: 推送时提示 "Permission denied"

**原因**: Token 或 SSH 配置不正确

**解决**:
```bash
# 检查远程仓库 URL
git remote -v

# 确保使用 HTTPS + Token 或 SSH 格式
# 重新配置远程仓库
```

### Q2: 推送时提示 "rejected: non-fast-forward"

**原因**: 远程仓库有本地没有的文件

**解决**:
```bash
# 拉取远程更改
git pull origin main --allow-unrelated-histories

# 解决冲突后重新推送
git push -u origin main
```

### Q3: 不想每次都输入 Token

**解决**:
```bash
# 启用凭据缓存
git config --global credential.helper cache

# 或者使用凭据管理器
git config --global credential.helper store
# (会明文存储在 ~/.git-credentials，注意安全)
```

---

## 📞 需要帮助?

如果遇到问题，请检查:
1. Token 权限是否包含 `repo`
2. 远程仓库 URL 是否正确
3. 网络连接是否正常
4. Git 版本是否最新: `git --version`

---

**选择适合你的方式，将代码推送到 GitHub 吧! 🎉**

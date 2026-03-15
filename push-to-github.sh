#!/bin/bash
#
# TuanziGuardianClaw v2 - GitHub 推送脚本
# 使用方法: ./push-to-github.sh YOUR_GITHUB_TOKEN
#

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 检查参数
if [ -z "$1" ]; then
    echo -e "${RED}❌ 错误: 请提供 GitHub Token${NC}"
    echo ""
    echo "使用方法:"
    echo "  ./push-to-github.sh YOUR_GITHUB_TOKEN"
    echo ""
    echo "获取 Token:"
    echo "  1. 访问 https://github.com/settings/tokens"
    echo "  2. 点击 'Generate new token (classic)'"
    echo "  3. 勾选 'repo' 权限"
    echo "  4. 复制生成的 token"
    exit 1
fi

TOKEN=$1
REPO_URL="https://${TOKEN}@github.com/Sakurakilove/openclaw-guardian-skill.git"

echo -e "${BLUE}🚀 TuanziGuardianClaw v2 - GitHub 推送脚本${NC}"
echo "=========================================="
echo ""

# 进入项目目录
cd "$(dirname "$0")"
PROJECT_DIR=$(pwd)
echo -e "${BLUE}📂 项目目录: ${PROJECT_DIR}${NC}"

# 检查 Git 仓库
if [ ! -d ".git" ]; then
    echo -e "${RED}❌ 错误: 当前目录不是 Git 仓库${NC}"
    exit 1
fi

# 检查远程仓库
echo -e "${YELLOW}🔗 配置远程仓库...${NC}"
git remote remove origin 2>/dev/null || true
git remote add origin "${REPO_URL}"

# 验证配置
echo -e "${YELLOW}📋 远程仓库配置:${NC}"
git remote -v

echo ""
echo -e "${YELLOW}📊 提交统计:${NC}"
git log --oneline | head -5

echo ""
echo -e "${YELLOW}🚀 推送到 GitHub...${NC}"

# 确保分支名为 main
git branch -M main

# 推送代码
if git push -u origin main; then
    echo ""
    echo -e "${GREEN}✅ 推送成功!${NC}"
    echo ""
    echo -e "${GREEN}🎉 代码已成功推送到 GitHub!${NC}"
    echo ""
    echo "📎 仓库地址:"
    echo "   https://github.com/Sakurakilove/openclaw-guardian-skill"
    echo ""
    echo "📖 下一步:"
    echo "   1. 访问上述链接查看代码"
    echo "   2. 创建 Release (可选)"
    echo "   3. 分享给 OpenClaw 社区"
    echo ""
    
    # 安全提示
    echo -e "${YELLOW}⚠️  安全提示:${NC}"
    echo "   推送完成后，建议移除 token 从远程 URL:"
    echo "   git remote set-url origin https://github.com/Sakurakilove/openclaw-guardian-skill.git"
    echo ""
    
    # 创建标签提示
    echo -e "${BLUE}🏷️  创建 Release:${NC}"
    echo "   git tag -a v2.0.0 -m 'Release v2.0.0'"
    echo "   git push origin v2.0.0"
    echo ""
    
else
    echo ""
    echo -e "${RED}❌ 推送失败${NC}"
    echo ""
    echo "可能的原因:"
    echo "   - Token 无效或已过期"
    echo "   - Token 没有 repo 权限"
    echo "   - 网络连接问题"
    echo ""
    echo "解决方法:"
    echo "   1. 检查 Token 是否正确"
    echo "   2. 确认 Token 有 'repo' 权限"
    echo "   3. 检查网络连接"
    echo "   4. 查看详细错误信息"
    echo ""
    exit 1
fi

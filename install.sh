#!/bin/bash
#
# Creator Skill 一键安装
# 用法: ./install.sh 或 curl -sSL <raw_url>/install.sh | bash
#
set -e

BOLD='\033[1m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
RED='\033[0;31m'
NC='\033[0m'

echo ""
echo -e "${BOLD}🎨 Creator Skill - 小红书内容创作助手${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# 确定项目根目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" && pwd)"
if [ -f "$SCRIPT_DIR/.claude-plugin/plugin.json" ]; then
    PROJECT_ROOT="$SCRIPT_DIR"
else
    PROJECT_ROOT="$HOME/Documents/creator-skill"
    if [ ! -d "$PROJECT_ROOT" ]; then
        echo -e "${YELLOW}→ 克隆项目...${NC}"
        git clone https://github.com/MoonSv/creator-skill.git "$PROJECT_ROOT" 2>/dev/null || {
            echo -e "${RED}项目目录不存在且无法克隆，请先 cd 到项目目录运行${NC}"
            exit 1
        }
    fi
fi

echo -e "${BOLD}[1/4] 检查环境${NC}"

# Python
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python3 未安装。请先: brew install python3${NC}"
    exit 1
fi
echo -e "  ${GREEN}✓${NC} Python $(python3 --version | cut -d' ' -f2)"

# pipx
if ! command -v pipx &> /dev/null; then
    echo -e "  ${YELLOW}→ 安装 pipx...${NC}"
    brew install pipx 2>/dev/null || {
        echo -e "${RED}❌ 无法安装 pipx，请手动: brew install pipx${NC}"
        exit 1
    }
    pipx ensurepath 2>/dev/null
fi
echo -e "  ${GREEN}✓${NC} pipx"

echo ""
echo -e "${BOLD}[2/4] 安装依赖${NC}"

# xiaohongshu-cli
if command -v xhs &> /dev/null || [ -f "$HOME/.local/bin/xhs" ]; then
    echo -e "  ${GREEN}✓${NC} xiaohongshu-cli 已安装"
else
    echo -e "  ${YELLOW}→ 安装 xiaohongshu-cli...${NC}"
    pipx install xiaohongshu-cli
    echo -e "  ${GREEN}✓${NC} xiaohongshu-cli 安装完成"
fi

# Pillow (注入到 xhs 的虚拟环境)
if python3 -c "import PIL" 2>/dev/null; then
    echo -e "  ${GREEN}✓${NC} Pillow 已安装"
else
    echo -e "  ${YELLOW}→ 安装 Pillow...${NC}"
    pipx inject xiaohongshu-cli Pillow 2>/dev/null || pip3 install --user Pillow 2>/dev/null || true
    echo -e "  ${GREEN}✓${NC} Pillow 安装完成"
fi

# PATH 设置
if [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
    export PATH="$HOME/.local/bin:$PATH"
    # 写入 shell 配置
    SHELL_RC="$HOME/.zshrc"
    [ -f "$HOME/.bashrc" ] && [ ! -f "$HOME/.zshrc" ] && SHELL_RC="$HOME/.bashrc"
    if ! grep -q '.local/bin' "$SHELL_RC" 2>/dev/null; then
        echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$SHELL_RC"
        echo -e "  ${GREEN}✓${NC} PATH 已更新 ($SHELL_RC)"
    fi
fi

echo ""
echo -e "${BOLD}[3/4] 注册 Claude Code Plugin${NC}"

# 注册 plugin
if command -v claude &> /dev/null; then
    claude plugin add "$PROJECT_ROOT" 2>/dev/null && \
        echo -e "  ${GREEN}✓${NC} Plugin 已注册" || \
        echo -e "  ${YELLOW}⚠${NC} 自动注册失败，请手动运行: claude plugin add $PROJECT_ROOT"
else
    echo -e "  ${YELLOW}⚠${NC} Claude Code CLI 未找到"
    echo -e "  请安装后手动注册: claude plugin add $PROJECT_ROOT"
fi

echo ""
echo -e "${BOLD}[4/4] 登录小红书${NC}"
echo ""
echo -e "  ${YELLOW}⚠️  安全提示：强烈建议使用小号登录${NC}"
echo ""

XHS_CMD="$HOME/.local/bin/xhs"
[ ! -f "$XHS_CMD" ] && XHS_CMD="xhs"

# 检查是否已登录
if $XHS_CMD status 2>/dev/null | grep -qi "ok: true\|authenticated"; then
    echo -e "  ${GREEN}✓${NC} 小红书已登录"
else
    echo -e "  需要扫码登录小红书（用小红书App扫描终端中的二维码）"
    echo ""
    read -p "  现在登录？[Y/n] " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Nn]$ ]]; then
        $XHS_CMD login
    else
        echo ""
        echo -e "  ${YELLOW}跳过登录。使用前请运行: xhs login${NC}"
    fi
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "${GREEN}${BOLD}安装完成！${NC}"
echo ""
echo "使用方式：在 Claude Code 中直接说："
echo ""
echo -e "  ${BOLD}我想发一条关于「北京探店」的小红书，图片在 ~/Photos/xxx/${NC}"
echo ""
echo "Skill 会自动触发，完成分析后在浏览器中打开 HTML 报告。"
echo ""

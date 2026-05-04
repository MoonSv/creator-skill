#!/bin/bash
set -e

echo "=== Creator Skill 环境安装 ==="
echo ""

# 检查 Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 未找到，请先安装 Python 3.9+"
    exit 1
fi
echo "✓ Python3: $(python3 --version)"

# 安装 xiaohongshu-cli
if command -v xhs &> /dev/null; then
    echo "✓ xiaohongshu-cli 已安装: $(xhs --version 2>/dev/null || echo 'installed')"
else
    echo "→ 安装 xiaohongshu-cli..."
    if command -v pipx &> /dev/null; then
        pipx install xiaohongshu-cli
        pipx inject xiaohongshu-cli Pillow
    else
        echo "  pipx 未找到，尝试 pip..."
        pip3 install --user xiaohongshu-cli Pillow 2>/dev/null || \
        pip3 install xiaohongshu-cli Pillow --break-system-packages 2>/dev/null || \
        { echo "❌ 安装失败。请先安装 pipx: brew install pipx"; exit 1; }
    fi
    echo "✓ xiaohongshu-cli 安装完成"
fi

# 安装 Pillow
if python3 -c "import PIL" 2>/dev/null; then
    echo "✓ Pillow 已安装"
else
    echo "→ 安装 Pillow..."
    if command -v pipx &> /dev/null; then
        pipx inject xiaohongshu-cli Pillow 2>/dev/null || pip3 install --user Pillow
    else
        pip3 install --user Pillow 2>/dev/null || pip3 install Pillow --break-system-packages
    fi
    echo "✓ Pillow 安装完成"
fi

# 确保 PATH 包含 ~/.local/bin
if [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
    echo ""
    echo "⚠️  ~/.local/bin 不在 PATH 中"
    echo "  请添加到你的 shell 配置文件："
    echo "  echo 'export PATH=\"\$HOME/.local/bin:\$PATH\"' >> ~/.zshrc"
    echo "  然后运行: source ~/.zshrc"
fi

# 检查登录状态
echo ""
echo "=== 登录状态检查 ==="
XHS_CMD="${HOME}/.local/bin/xhs"
if [ ! -f "$XHS_CMD" ]; then
    XHS_CMD="xhs"
fi

if $XHS_CMD status 2>/dev/null | grep -qi "logged\|authenticated\|ok"; then
    echo "✓ 小红书已登录"
else
    echo "⚠️  小红书未登录"
    echo ""
    echo "请运行以下命令完成登录："
    echo "  xhs login"
    echo ""
    echo "⚠️  安全提示：强烈建议使用小号登录，以保护主账号安全"
fi

echo ""
echo "=== 安装完成 ==="
echo ""
echo "下一步："
echo "  1. xhs login          # 扫码登录小红书"
echo "  2. 在 Claude Code 中说 '我想发小红书' 即可触发 skill"

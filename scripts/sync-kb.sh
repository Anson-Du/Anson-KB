#!/bin/bash
# ============================================================
# Anson 知识库 · 每日进料同步脚本（launchd 每日 10:00 调用，可手动重跑，幂等）
# 作用：① AI 记忆镜像 → codebuddy-memory/（当日快照，只增不改）
#       ② git add -A + commit（有变更才提交）
#       ③ 若已配置远端 origin 则自动 push（未配置则静默跳过）
# ============================================================
set -uo pipefail

KB="$HOME/Documents/Anson"
MEM_SRC="$HOME/.codebuddy/memery"
DATE=$(date +%Y%m%d)
TS=$(date "+%Y-%m-%d %H:%M:%S")
LOG="$KB/scripts/sync-kb.log"
STATE="$KB/scripts/.last-mem-md5"

exec >>"$LOG" 2>&1
echo "===== $TS sync start ====="

# ① 记忆镜像：源有变化才写当日快照（同日内可覆盖为当日终态，跨日只增）
latest=$(ls -t "$MEM_SRC"/*_memery.md 2>/dev/null | head -1)
if [ -n "$latest" ]; then
  now_md5=$(md5 -q "$latest")
  old_md5=$(cat "$STATE" 2>/dev/null || echo "")
  if [ "$now_md5" != "$old_md5" ]; then
    dst="$KB/codebuddy-memory/${DATE}_记忆镜像.md"
    {
      echo "# AI 记忆镜像快照 $(date +%Y-%m-%d)"
      echo
      echo "> 来源：\`~/.codebuddy/memery\`（每日自动镜像，跨日只增不改，同日为当日终态）"
      echo
      cat "$latest"
    } > "$dst"
    echo "$now_md5" > "$STATE"
    echo "记忆镜像已更新：$dst"
  else
    echo "记忆无变化，跳过镜像"
  fi
else
  echo "警告：未找到记忆源文件（~/.codebuddy/memery/*_memery.md）"
fi

# ② git 提交
cd "$KB" || { echo "错误：知识库目录不存在"; exit 1; }
if [ -n "$(git status --porcelain)" ]; then
  git add -A
  git commit -q -m "sync: $(date +%F) 每日进料同步"
  echo "git 已提交"
else
  echo "git 无变更"
fi

# ③ 远端推送（配置 origin 后自动生效）
if git remote | grep -q '^origin$'; then
  if git push -q origin main 2>/dev/null; then
    echo "已推送远端 origin/main"
  else
    echo "推送失败（网络/认证问题，下次自动重试）"
  fi
fi

echo "===== $TS sync end ====="

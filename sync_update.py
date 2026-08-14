# -*- coding: utf-8 -*-
"""
一键同步脚本：更新施工看板在线数据
流程：
  1. 在数据源文件夹中查找最新的 Phase II 施工总览-*.xlsx
  2. 复制为仓库 data/Phase II 施工总览.xlsx
  3. git add + commit + push 推送到 GitHub
  4. 网页（GitHub Pages）自动展示最新数据
"""
import os
import re
import shutil
import subprocess
import sys

# ===== 配置（如需修改请编辑此处）=====
SRC_DIR = r"C:\Users\Administrator.rokin-2025VMFLM\Desktop\Opencode\甘特图-v2"
REPO_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_NAME = "Phase II 施工总览.xlsx"
PATTERN = re.compile(r"Phase II 施工总览.*\.xlsx$", re.IGNORECASE)


def find_newest_excel():
    """在数据源文件夹中查找最新的施工总览 Excel"""
    if not os.path.isdir(SRC_DIR):
        print("❌ 数据源文件夹不存在：" + SRC_DIR)
        return None
    candidates = []
    for name in os.listdir(SRC_DIR):
        if PATTERN.search(name) and name.lower().endswith(".xlsx"):
            path = os.path.join(SRC_DIR, name)
            candidates.append((os.path.getmtime(path), path, name))
    if not candidates:
        print("❌ 数据源文件夹中未找到 Phase II 施工总览-*.xlsx")
        return None
    candidates.sort(key=lambda x: x[0], reverse=True)
    return candidates[0][1], candidates[0][2]


def git_run(args, cwd):
    r = subprocess.run(args, cwd=cwd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.stdout.strip():
        print(r.stdout.strip())
    if r.stderr.strip():
        print(r.stderr.strip())
    return r.returncode


def main():
    print("=" * 50)
    print("施工看板 · 一键同步")
    print("=" * 50)

    # 1. 找最新 Excel
    found = find_newest_excel()
    if not found:
        sys.exit(1)
    src_path, src_name = found
    print("✅ 找到最新表格：" + src_name)

    # 2. 复制到仓库
    data_dir = os.path.join(REPO_DIR, "data")
    os.makedirs(data_dir, exist_ok=True)
    dst = os.path.join(data_dir, DATA_NAME)
    shutil.copy2(src_path, dst)
    print("✅ 已复制 → data/" + DATA_NAME)

    # 3. 推送到 GitHub
    print("🔄 正在推送到 GitHub ...")
    if git_run(["git", "add", "-A"], REPO_DIR) != 0:
        print("❌ git add 失败")
        sys.exit(1)
    if git_run(["git", "commit", "-m", "同步更新施工总览：" + src_name], REPO_DIR) != 0:
        print("ℹ️  无变更或提交失败，继续推送")
    if git_run(["git", "push", "origin", "main"], REPO_DIR) != 0:
        print("❌ git push 失败，请检查网络/GitHub 登录")
        sys.exit(1)

    print("✅ 同步完成！网页将在约 1 分钟内自动更新")
    print("   访问：https://zhaohuahua-sys.github.io/construction-board/")
    print("=" * 50)


if __name__ == "__main__":
    main()

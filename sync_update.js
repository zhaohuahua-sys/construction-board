// 一键同步脚本（Node.js 版）
// 流程：查找最新 Excel -> 复制到仓库 data/ -> git push -> 网页自动更新
const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

// ===== 配置 =====
const SRC_DIR = 'C:\\Users\\Administrator.rokin-2025VMFLM\\Desktop\\Opencode\\甘特图-v2';
const REPO_DIR = __dirname; // 脚本所在目录即本地仓库
const DATA_NAME = 'Phase II 施工总览.xlsx';

function run(cmd) {
  try {
    const out = execSync(cmd, { cwd: REPO_DIR, encoding: 'utf8', stdio: ['pipe', 'pipe', 'pipe'] });
    if (out.trim()) console.log(out.trim());
    return 0;
  } catch (e) {
    if (e.stdout) console.log(String(e.stdout).trim());
    if (e.stderr) console.log(String(e.stderr).trim());
    return e.status || 1;
  }
}

function main() {
  console.log('='.repeat(50));
  console.log('施工看板 · 一键同步');
  console.log('='.repeat(50));

  // 1. 查找最新 Excel
  if (!fs.existsSync(SRC_DIR)) {
    console.log('❌ 数据源文件夹不存在：' + SRC_DIR);
    process.exit(1);
  }
  const files = fs.readdirSync(SRC_DIR)
    .filter(n => /^Phase II 施工总览.*\.xlsx$/i.test(n) && fs.statSync(path.join(SRC_DIR, n)).isFile())
    .map(n => ({ name: n, mtime: fs.statSync(path.join(SRC_DIR, n)).mtimeMs }))
    .sort((a, b) => b.mtime - a.mtime);
  if (!files.length) {
    console.log('❌ 数据源文件夹中未找到 Phase II 施工总览-*.xlsx');
    process.exit(1);
  }
  const latest = files[0].name;
  console.log('✅ 找到最新表格：' + latest);

  // 2. 复制到仓库
  const dataDir = path.join(REPO_DIR, 'data');
  fs.mkdirSync(dataDir, { recursive: true });
  fs.copyFileSync(path.join(SRC_DIR, latest), path.join(dataDir, DATA_NAME));
  console.log('✅ 已复制 → data/' + DATA_NAME);

  // 3. git 推送
  console.log('🔄 正在推送到 GitHub ...');
  if (run('git add -A') !== 0) { console.log('❌ git add 失败'); process.exit(1); }
  if (run('git commit -m "同步更新施工总览：' + latest + '"') !== 0) console.log('ℹ️  无变更或提交失败，继续推送');
  if (run('git push origin main') !== 0) { console.log('❌ git push 失败，请检查网络/GitHub 登录'); process.exit(1); }

  console.log('✅ 同步完成！网页将在约 1 分钟内自动更新');
  console.log('   访问：https://zhaohuahua-sys.github.io/construction-board/');
  console.log('='.repeat(50));
}

main();

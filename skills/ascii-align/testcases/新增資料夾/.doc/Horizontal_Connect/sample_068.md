## Sample 068

**Source**: `claude-dotfiles\pm-v2-design.md` L172

```
~/.claude/
├── commands/
│   ├── pm.md          <-- v2 主指令（~660 行）
│   ├── hello.md       <-- legacy（已 deprecated）
│   ├── sc.md          <-- legacy（已 deprecated）
│   └── bye.md         <-- legacy（已 deprecated）
├── statusline.js      <-- status line 渲染
├── statusline.sh      <-- status line 入口
├── pm-update.sh       <-- status line 狀態更新
├── pm-last.txt        <-- status line 狀態檔（runtime）
└── settings.json      <-- hooks（SessionStart reset、Stop beep、PreToolUse beep）

GitHub Repo: CPIDLE/claude-dotfiles
├── commands/pm.md     <-- 主指令源碼
├── reviews/           <-- deep 審核報告
├── pm-v2-design.md    <-- 本文件
├── install.ps1        <-- Windows 安裝腳本
└── install.sh         <-- Linux/Mac 安裝腳本
```


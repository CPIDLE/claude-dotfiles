const fs = require('fs');
const path = require('path');

let data = '';
process.stdin.setEncoding('utf8');
process.stdin.on('data', chunk => { data += chunk; });
process.stdin.on('end', () => {
  try {
    const sanitized = data.replace(/\\(?!["\\/bfnrtu])/g, '/');
    const j = JSON.parse(sanitized);
    const model = j.model?.display_name || 'Claude';
    const dir = (j.workspace?.current_dir || '').replace(/\\/g, '/').split('/').pop() || '?';
    const pct = Math.round(j.context_window?.used_percentage || 0);

    // ANSI codes
    const DIM = '\x1b[90m';     // gray
    const YELLOW = '\x1b[33m';  // yellow = running
    const BOLD = '\x1b[1;97m';  // bright white bold = done
    const RESET = '\x1b[0m';

    // PM status from ~/.claude/pm-last.txt
    // Format: YYYY-MM-DD\tpm:done,sync:running,bye:pending
    let pmState = { pm: 'pending', sync: 'pending', bye: 'pending' };
    try {
      const pmFile = path.join(process.env.HOME || process.env.USERPROFILE, '.claude', 'pm-last.txt');
      const pmData = fs.readFileSync(pmFile, 'utf8').trim();
      const [date, stateStr] = pmData.split('\t');
      const today = new Date().toISOString().slice(0, 10);
      if (date === today && stateStr) {
        for (const part of stateStr.split(',')) {
          const [key, val] = part.split(':');
          if (pmState.hasOwnProperty(key)) pmState[key] = val;
        }
      }
    } catch {}

    function colorize(label, state) {
      if (state === 'done') return `${BOLD}${label}${RESET}`;
      if (state === 'running') return `${YELLOW}${label}${RESET}`;
      return `${DIM}${label}${RESET}`;
    }

    const pmTag = colorize('pm', pmState.pm)
      + `${DIM}\u25b8${RESET}`
      + colorize('sync', pmState.sync)
      + `${DIM}\u25b8${RESET}`
      + colorize('bye', pmState.bye);

    process.stdout.write(`[${model}] ${dir} | ${pmTag} | ctx:${pct}%`);
  } catch {
    process.stdout.write('[Claude] ? | pm | ctx:0%');
  }
});

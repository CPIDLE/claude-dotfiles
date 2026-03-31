const fs = require('fs');
const path = require('path');
const https = require('https');

const HOME = process.env.HOME || process.env.USERPROFILE;
const CLAUDE_DIR = path.join(HOME, '.claude');
const CACHE_FILE = path.join(CLAUDE_DIR, 'usage-cache.json');
const CRED_FILE = path.join(CLAUDE_DIR, '.credentials.json');
const REFRESH_SEC = 300; // 5 min

function readCache() {
  try {
    const c = JSON.parse(fs.readFileSync(CACHE_FILE, 'utf8'));
    if (Date.now() - c.ts < REFRESH_SEC * 1000) return c;
  } catch {}
  return null;
}

function fetchUsage() {
  let token;
  try {
    token = JSON.parse(fs.readFileSync(CRED_FILE, 'utf8')).claudeAiOauth?.accessToken;
  } catch {}
  if (!token) return Promise.resolve(null);

  return new Promise(resolve => {
    const req = https.get('https://api.anthropic.com/api/oauth/usage', {
      headers: {
        'Authorization': `Bearer ${token}`,
        'anthropic-beta': 'oauth-2025-04-20',
        'Content-Type': 'application/json'
      },
      timeout: 3000
    }, res => {
      let body = '';
      res.on('data', d => body += d);
      res.on('end', () => {
        try {
          const j = JSON.parse(body);
          if (j.five_hour?.utilization == null) return resolve(null);
          const cache = { ts: Date.now(), session: j.five_hour, week: j.seven_day };
          fs.writeFileSync(CACHE_FILE, JSON.stringify(cache));
          resolve(cache);
        } catch { resolve(null); }
      });
    });
    req.on('error', () => resolve(null));
    req.on('timeout', () => { req.destroy(); resolve(null); });
  });
}

function ansiColor(pct) {
  if (pct >= 80) return '\x1b[31m'; // red
  if (pct >= 50) return '\x1b[93m'; // yellow
  return '\x1b[32m'; // green
}

function quotaTag(cache) {
  if (!cache) return '';
  const s = Math.round(cache.session?.utilization || 0);
  const w = Math.round(cache.week?.utilization || 0);
  const DIM = '\x1b[90m';
  const RESET = '\x1b[0m';
  let tag = ` ${DIM}5h:${RESET}${ansiColor(s)}${s}%${RESET} ${DIM}7d:${RESET}${ansiColor(w)}${w}%${RESET}`;
  if (cache.week?.resets_at) {
    const d = new Date(cache.week.resets_at);
    tag += ` ${ansiColor(w)}@${d.getMonth() + 1}/${d.getDate()}${RESET}`;
  }
  return tag;
}

let data = '';
process.stdin.setEncoding('utf8');
process.stdin.on('data', chunk => { data += chunk; });
process.stdin.on('end', async () => {
  let cache = readCache();
  if (!cache) cache = await fetchUsage();

  try {
    const sanitized = data.replace(/\\(?!["\\/bfnrtu])/g, '/');
    const j = JSON.parse(sanitized);
    const modelRaw = j.model?.display_name || 'Claude';
    const model = modelRaw.replace(/\s*\(.*?\)\s*$/, ''); // strip "(1M context)" etc.
    const dir = (j.workspace?.current_dir || '').replace(/\\/g, '/').split('/').pop() || '?';
    const pct = Math.round(j.context_window?.used_percentage || 0);

    // ANSI codes
    const DIM = '\x1b[90m';
    const YELLOW = '\x1b[93m';
    const BRIGHT = '\x1b[97m';
    const RESET = '\x1b[0m';

    // PM status from ~/.claude/pm-last.txt
    let pmState = { pm: 'pending', sync: 'pending', bye: 'pending' };
    try {
      const pmFile = path.join(CLAUDE_DIR, 'pm-last.txt');
      const stateStr = fs.readFileSync(pmFile, 'utf8').trim();
      if (stateStr) {
        for (const part of stateStr.split(',')) {
          const [key, val] = part.split(':');
          if (pmState.hasOwnProperty(key)) pmState[key] = val;
        }
      }
    } catch {}

    function colorize(label, state) {
      if (state === 'done') return `${BRIGHT}${label}${RESET}`;
      if (state === 'running') return `${YELLOW}${label}${RESET}`;
      return `${DIM}${label}${RESET}`;
    }

    const pmTag = colorize('pm', pmState.pm)
      + `${DIM}\u25b8${RESET}`
      + colorize('sync', pmState.sync)
      + `${DIM}\u25b8${RESET}`
      + colorize('bye', pmState.bye);

    const ctxColor = ansiColor(pct);
    const GREEN = '\x1b[32m';
    process.stdout.write(`${BRIGHT}${dir}${RESET} ${DIM}\u2502${RESET} ${DIM}__BRANCH__${RESET} ${DIM}\u2502${RESET} ${pmTag}     ${DIM}Opus ${RESET}${GREEN}${model.replace(/^.*\s/, '')}${RESET} ${DIM}\u2502 ctx:${RESET}${ctxColor}${pct}%${RESET}${quotaTag(cache)}`);
  } catch {
    process.stdout.write(`\x1b[90mClaude\x1b[0m  \x1b[97m?\x1b[0m \u2502 pm \u2502 \x1b[32mctx 0%\x1b[0m${quotaTag(cache)}`);
  }
});

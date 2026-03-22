let data = '';
process.stdin.setEncoding('utf8');
process.stdin.on('data', chunk => { data += chunk; });
process.stdin.on('end', () => {
  try {
    // Handle Windows paths: replace lone backslashes with forward slashes before parsing
    const sanitized = data.replace(/\\(?!["\\/bfnrtu])/g, '/');
    const j = JSON.parse(sanitized);
    const model = j.model?.display_name || 'Claude';
    const dir = (j.workspace?.current_dir || '').replace(/\\/g, '/').split('/').pop() || '?';
    const pct = Math.round(j.context_window?.used_percentage || 0);
    process.stdout.write(`[${model}] ${dir} | ctx:${pct}%`);
  } catch {
    process.stdout.write('[Claude] ? | ctx:0%');
  }
});

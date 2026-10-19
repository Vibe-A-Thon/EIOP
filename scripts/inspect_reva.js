const fs = require('fs');
const html = fs.readFileSync('reva-tracker.html', 'utf8');
const tag = '<script type="application/json" id="data">';
const start = html.indexOf(tag) + tag.length;
const end = html.indexOf('</script>', start);
const jsonText = html.slice(start, end);
const data = JSON.parse(jsonText);
console.log('Keys:', Object.keys(data));
console.log('Tasks count:', data.tasks ? data.tasks.length : 0);
console.log('Reqs count:', data.reqs ? data.reqs.length : 0);
const phases = [...new Set(data.tasks.map(t => t.phase))];
console.log('Phases count:', phases.length);
phases.forEach(p => console.log('  -', p));

const scriptStart = html.indexOf('<script>', end) + '<script>'.length;
const scriptEnd = html.indexOf('</script>', scriptStart);
console.log('--- TRACKER SCRIPT ---');
console.log(html.slice(scriptStart, scriptEnd));

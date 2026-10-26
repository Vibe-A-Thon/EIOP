const fs = require('node:fs');
const path = require('node:path');
const {pathToFileURL} = require('node:url');
const {createRequire} = require('node:module');
const assert = require('node:assert/strict');

async function main() {
  const [rootArg, outputArg] = process.argv.slice(2);
  const root = path.resolve(rootArg), out = path.resolve(outputArg);
  const requireWeb = createRequire(path.join(root, 'apps/web/package.json'));
  const {chromium} = requireWeb('@playwright/test');
  const AxeBuilder = requireWeb('@axe-core/playwright').default;
  fs.mkdirSync(path.join(out, 'evidence/tracker-browser'), {recursive:true});
  const browser = await chromium.launch({headless:true});
  const checks = [], errors = [];
  try {
    const context = await browser.newContext({viewport:{width:1440,height:1000}});
    const page = await context.newPage();
    page.on('pageerror', e => errors.push(e.message));
    await page.goto(pathToFileURL(path.join(out, 'tracker.html')).href);
    await page.getByRole('heading', {name:'EOIP Evidence Audit'}).waitFor();
    for (const tab of ['Overview','Requirements','Remediation','Evidence & Checks','Scope & Signoff']) {
      await page.getByRole('tab', {name:tab, exact:true}).click();
      assert.equal(await page.getByRole('tab', {name:tab, exact:true}).getAttribute('aria-selected'), 'true');
    }
    checks.push('All five tabs activate');
    await page.getByRole('tab', {name:'Requirements', exact:true}).click();
    await page.getByLabel('Search requirements').fill('CRA-021.7');
    await page.getByRole('button', {name:'CRA-021.7', exact:true}).click();
    await page.getByRole('dialog').waitFor();
    await page.getByRole('button', {name:'Close requirement details'}).click();
    await page.getByRole('button', {name:'Clear Filters'}).click();
    await page.getByRole('button', {name:'Next', exact:true}).click();
    assert.match(await page.locator('#page-label').innerText(), /Page 2/);
    checks.push('Search, exact subclause details and pagination work');
    const result = await page.evaluate(() => {
      const commit = DATA.summary.git_commit;
      const req = {residual_gaps:[],severity:'High'};
      const test = {proof_tier:'L2',type:'test_run',actual_result:'passed',repro_command:'pytest exact_case',links:[{url:'tests.xml'}],git_commit:commit,_bundle:commit,_producer:'producer'};
      const ci = {...test,proof_tier:'L3',type:'ci_run',ci_job:'tests',ci_run_id:'123'};
      return [assess(req,[test,ci]).status, assess(req,[{...test,_bundle:'b'.repeat(40)},ci]).status,
        assess(req,[test,{...ci,ci_run_id:''}]).status,
        assess(req,[test,{...ci,proof_tier:'L4',environment:'production'}]).status,
        assess({...req,severity:'Critical'},[test,ci]).status,
        assess(req,[{...test,actual_result:'unknown'},ci]).status,
        assess({...req,residual_gaps:['open']},[test,ci]).status];
    });
    assert.deepEqual(result,['Implemented','Not Verified','Not Verified','Not Verified','Not Verified','Not Verified','Partially Implemented']);
    checks.push('Browser proof gates reject stale, bare CI, production L4, unknown outcomes and unsigned Critical closure');
    await page.locator('#file').setInputFiles({name:'invalid.json',mimeType:'application/json',buffer:Buffer.from('{"schema_version":"0.0.0"}')});
    assert.match(await page.locator('#message').innerText(), /Import rejected/);
    const downloadPromise = page.waitForEvent('download');
    await page.getByRole('button', {name:'Export Review', exact:true}).click();
    const download = await downloadPromise;
    assert.equal(download.suggestedFilename(),'eoip-audit-review.json');
    checks.push('Invalid import rejected; review export downloads');
    await page.getByRole('tab', {name:'Overview',exact:true}).click();
    for (const width of [1440,390]) {
      await page.setViewportSize({width,height:1000});
      assert(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth + 1));
      await page.screenshot({path:path.join(out,`evidence/tracker-browser/tracker-${width}.png`),fullPage:true});
      const axe = await new AxeBuilder({page}).withTags(['wcag2a','wcag2aa','wcag21aa']).analyze();
      fs.writeFileSync(path.join(out,`evidence/tracker-browser/axe-${width}.json`),JSON.stringify(axe.violations,null,2));
      assert.equal(axe.violations.filter(v=>['serious','critical'].includes(v.impact)).length,0,JSON.stringify(axe.violations.map(v=>({id:v.id,impact:v.impact}))));
    }
    checks.push('Desktop/mobile non-overflow screenshots and selected axe checks pass');
    assert.deepEqual(errors,[]);
    fs.writeFileSync(path.join(out,'evidence/tracker-browser/checks.json'),JSON.stringify({status:'passed',checks,errors,scope:'Audit tracker only, not EOIP application acceptance'},null,2));
    console.log(JSON.stringify({status:'passed',checks,errors}));
  } finally { await browser.close(); }
}
main().catch(e=>{console.error(e);process.exitCode=1});

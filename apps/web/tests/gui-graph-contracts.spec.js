import {test, expect} from '@playwright/test';

test('XML and CSV export preserve hostile strings, properties, edge IDs and direction', async ({page}) => {
  await page.goto('/');
  const result = await page.evaluate(async () => {
    const formats = await import('/src/kgr/export/GraphFormats.ts');
    const id = 'node<"&雪';
    const graph = {nodes: [{id, label: 'Type<&', properties: {name: 'A,"B"\nC', proof: 'evidence:one'}},
      {id: 'second', label: 'Target'}], edges: [
      {id: 'edge-one', from_id: id, to_id: 'second', type: 'USES<&', properties: {confidence: .8}},
      {id: 'edge-two', from_id: id, to_id: 'second', type: 'USES<&'},
    ]};
    const documents = [formats.graphToGraphML(graph), formats.graphToGEXF(graph)].map(xml => new DOMParser().parseFromString(xml, 'application/xml'));
    return {errors: documents.map(doc => doc.querySelectorAll('parsererror').length),
      nodeIds: documents.map(doc => doc.querySelector('node')?.getAttribute('id')),
      edgeIds: documents.map(doc => [...doc.querySelectorAll('edge')].map(edge => edge.getAttribute('id'))),
      targets: documents.map(doc => doc.querySelector('edge')?.getAttribute('target')),
      properties: documents[0].querySelector('data[key="n-properties"]')?.textContent,
      csv: formats.graphToCsv(graph).nodes,
      print: formats.graphPrintDocument({nodes: [{id: '<img src=x onerror="window.injected=true">', label: '</td><script>window.injected=true</script>'}], edges: []})};
  });
  expect(result.errors).toEqual([0, 0]);
  expect(result.nodeIds).toEqual(['node<"&雪', 'node<"&雪']);
  expect(result.edgeIds).toEqual([['edge-one', 'edge-two'], ['edge-one', 'edge-two']]);
  expect(result.targets).toEqual(['second', 'second']);
  expect(JSON.parse(result.properties).proof).toBe('evidence:one');
  expect(result.csv).toContain('"node<""&雪","Type<&"');
  await page.setContent(result.print);
  expect(await page.locator('script, img').count()).toBe(0);
  expect(await page.evaluate(() => window.injected)).toBeUndefined();
  await expect(page.locator('body')).toContainText('<img src=x');
});

test('virtual entity list supports keyboard end/select/expand and filtering after scroll', async ({page}) => {
  await page.goto('/tests/fixtures/gui-component.html');
  await page.evaluate(async () => {
    const {React, createRoot} = window.GUI_TEST;
    const {default: List} = await import('/src/kgr/components/VirtualEntityList.jsx');
    createRoot(document.getElementById('root')).render(React.createElement(List, {
      nodes: Array.from({length: 500}, (_, index) => ({id: `fixture-${index}`, label: 'Entity', properties: {name: `Entity ${String(index).padStart(3, '0')}`}})),
      onSelect: node => {window.selectedEntity = node.id;}, onExpand: node => {window.expandedEntity = node.id;},
    }));
  });
  const list = page.getByRole('listbox', {name: 'Entity results'});
  await list.focus();
  await page.keyboard.press('End');
  await expect(page.getByRole('option', {name: /Entity 499/})).toBeVisible();
  await page.keyboard.press('Space');
  expect(await page.evaluate(() => window.selectedEntity)).toBe('fixture-499');
  await page.keyboard.press('Enter');
  expect(await page.evaluate(() => window.expandedEntity)).toBe('fixture-499');
  await page.getByLabel('Filter entities').fill('Entity 000');
  await expect(page.getByRole('option', {name: /Entity 000/})).toBeVisible();
  await expect(list.getByRole('option')).toHaveCount(1);
});

test('event poll uses authenticated client, never a credential URL, and stops after unmount', async ({page}) => {
  await page.goto('/tests/fixtures/gui-component.html');
  await page.evaluate(async () => {
    const {React, createRoot} = window.GUI_TEST;
    const {default: useEvents} = await import('/src/kgr/hooks/useGraphEvents.js');
    window.pollCalls = [];
    const api = async (path, body, method, options) => {
      window.pollCalls.push({path, aborted: options.signal.aborted});
      return {events: [{event_id: 1, type: 'vertex_upserted', data: {canonical_id: 'fixture:one'}}]};
    };
    function Harness() {
      const feed = useEvents(location.origin, 'never-in-a-url', api);
      return React.createElement('div', null,
        React.createElement('output', {'aria-label': 'Feed status'}, feed.status),
        React.createElement('output', {'aria-label': 'Event count'}, feed.events.length),
        React.createElement('button', {onClick: feed.pause}, 'Pause'),
        React.createElement('button', {onClick: feed.resume}, 'Resume'),
        React.createElement('button', {onClick: feed.clear}, 'Clear'));
    }
    window.hookRoot = createRoot(document.getElementById('root'));
    window.hookRoot.render(React.createElement(Harness));
  });
  await expect(page.getByLabel('Feed status')).toHaveText('polling');
  await expect(page.getByLabel('Event count')).toHaveText('1');
  expect((await page.evaluate(() => window.pollCalls)).every(call => !call.path.includes('never-in-a-url'))).toBe(true);
  await page.getByRole('button', {name: 'Clear', exact: true}).click();
  await expect(page.getByLabel('Event count')).toHaveText('0');
  await page.waitForTimeout(2200);
  await expect(page.getByLabel('Event count')).toHaveText('0');
  await page.evaluate(() => window.hookRoot.unmount());
  const calls = await page.evaluate(() => window.pollCalls.length);
  await page.waitForTimeout(2300);
  expect(await page.evaluate(() => window.pollCalls.length)).toBe(calls);
});

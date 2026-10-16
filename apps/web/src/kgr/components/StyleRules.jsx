import React, {useCallback, useEffect, useState} from 'react';
import {Icon} from '../../icons.jsx';

const OPERATORS = ['=', '!=', '>', '<', 'contains', 'regex', 'exists'];
const STYLE_PROPS = ['color', 'size', 'shape', 'borderStyle', 'borderColor', 'icon', 'label'];

const defaultRules = [
  {id: 'r1', condition: {label: 'File', property: 'path', operator: 'contains', value: 'test'}, style: {color: '#4CAF50', shape: 'diamond'}, enabled: true},
  {id: 'r2', condition: {property: 'creation_status', operator: '=', value: 'AMBIGUOUS'}, style: {borderStyle: 'dotted', borderColor: '#FF9800'}, enabled: true},
  {id: 'r3', condition: {label: 'ValidationFinding'}, style: {color: '#ef4444', size: 1.5}, enabled: true},
];

function loadRules() {
  try {
    const stored = localStorage.getItem('kgr-style-rules');
    return stored ? JSON.parse(stored) : [...defaultRules];
  } catch { return [...defaultRules]; }
}

function saveRules(rules) {
  try { localStorage.setItem('kgr-style-rules', JSON.stringify(rules)); } catch {}
}

export function applyStyleRules(node, rules) {
  for (const rule of rules) {
    if (!rule.enabled) continue;
    const c = rule.condition;
    if (c.label && node.label !== c.label) continue;
    if (c.property && c.operator) {
      const val = node.properties?.[c.property];
      if (c.operator === '=' && String(val) !== c.value) continue;
      if (c.operator === '!=' && String(val) === c.value) continue;
      if (c.operator === '>' && !(Number(val) > Number(c.value))) continue;
      if (c.operator === '<' && !(Number(val) < Number(c.value))) continue;
      if (c.operator === 'contains' && !String(val || '').includes(c.value || '')) continue;
      if (c.operator === 'regex') { try { if (!new RegExp(c.value).test(String(val))) continue; } catch { continue; } }
      if (c.operator === 'exists' && val == null) continue;
    }
    return rule.style;
  }
  return null;
}

export default function StyleRules({onApply, onClose}) {
  const [rules, setRules] = useState(loadRules);

  useEffect(() => { saveRules(rules); onApply?.(rules); }, [rules]);

  const addRule = () => {
    setRules(r => [...r, {id: `r${Date.now()}`, condition: {label: '', property: '', operator: '=', value: ''}, style: {color: '#7c5cff'}, enabled: true}]);
  };

  const removeRule = (id) => setRules(r => r.filter(x => x.id !== id));

  const updateRule = (id, field, value) => {
    setRules(r => r.map(x => x.id === id ? {...x, ...{[field]: value}} : x));
  };

  const updateCondition = (id, key, value) => {
    setRules(r => r.map(x => x.id === id ? {...x, condition: {...x.condition, [key]: value}} : x));
  };

  const updateStyle = (id, key, value) => {
    setRules(r => r.map(x => x.id === id ? {...x, style: {...x.style, [key]: value}} : x));
  };

  const exportRules = () => {
    try { navigator.clipboard.writeText(JSON.stringify(rules, null, 2)); } catch {}
  };

  const importRules = useCallback(() => {
    const input = prompt('Paste JSON rules:');
    if (input) { try { setRules(JSON.parse(input)); } catch {} }
  }, []);

  return <div className="kgr-style-rules">
    <div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 10}}>
      <h3 style={{margin: 0}}>Conditional Styling Rules</h3>
      <button className="icon-button" onClick={onClose}><Icon name="close"/></button>
    </div>
    {rules.map(rule => <div key={rule.id} className="rule-row">
      <input type="checkbox" checked={rule.enabled} onChange={e => updateRule(rule.id, 'enabled', e.target.checked)}/>
      <span style={{fontSize: 11, color: 'var(--muted)'}}>IF</span>
      <input placeholder="Type" value={rule.condition.label || ''} onChange={e => updateCondition(rule.id, 'label', e.target.value)} style={{width: 70}}/>
      <input placeholder="Property" value={rule.condition.property || ''} onChange={e => updateCondition(rule.id, 'property', e.target.value)} style={{width: 80}}/>
      <select value={rule.condition.operator || '='} onChange={e => updateCondition(rule.id, 'operator', e.target.value)}>
        {OPERATORS.map(o => <option key={o} value={o}>{o}</option>)}
      </select>
      <input placeholder="Value" value={rule.condition.value || ''} onChange={e => updateCondition(rule.id, 'value', e.target.value)} style={{width: 70}}/>
      <span style={{fontSize: 11, color: 'var(--muted)'}}>THEN</span>
      <input type="color" value={rule.style.color || '#7c5cff'} onChange={e => updateStyle(rule.id, 'color', e.target.value)} className="rule-preview"/>
      <button className="icon-button" onClick={() => removeRule(rule.id)} title="Remove rule"><Icon name="close" size={12}/></button>
    </div>)}
    <div style={{display: 'flex', gap: 6, marginTop: 8}}>
      <button className="toolbar-button" onClick={addRule}><Icon name="plus" size={12}/> Add rule</button>
      <button className="toolbar-button" onClick={exportRules}>Export</button>
      <button className="toolbar-button" onClick={importRules}>Import</button>
      <button className="toolbar-button" onClick={() => setRules([...defaultRules])}>Reset</button>
    </div>
  </div>;
}

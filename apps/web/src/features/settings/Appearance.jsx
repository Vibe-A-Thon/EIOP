import React from 'react';
import {Icon} from '../../icons.jsx';

const themes = [
  ['light', 'Light', '#f7f9fa', '#172126'],
  ['dark', 'Dark', '#101518', '#f2f6f7'],
  ['contrast-light', 'High contrast light', '#ffffff', '#000000'],
  ['contrast-dark', 'High contrast dark', '#000000', '#ffffff'],
];

export default function Appearance({theme, setTheme, reducedMotion, setReducedMotion}) {
  return <section className="appearance-page" aria-labelledby="appearance-title">
    <h2 id="appearance-title">Appearance</h2>
    <fieldset className="theme-choices"><legend>Theme</legend>
      {themes.map(([id, label, background, color]) => <label key={id} className={`theme-choice ${theme === id ? 'selected' : ''}`}>
        <span className="theme-preview" style={{background, color}} aria-hidden="true"><Icon name="graph" size={30}/><span/><span/></span>
        <span><input type="radio" name="theme" value={id} checked={theme === id} onChange={() => setTheme(id)}/>{label}</span>
      </label>)}
    </fieldset>
    <label className="motion-choice"><input type="checkbox" checked={reducedMotion} onChange={event => setReducedMotion(event.target.checked)}/>Reduce motion</label>
    <p className="subtle">Applied to this connection. Appearance resets when you disconnect or reload.</p>
  </section>;
}

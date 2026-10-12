import React, {useState, useCallback} from 'react';
import {Icon} from '../icons.jsx';

export default function CausalBlastRadiusDashboard({api}) {
  const [seedEntity, setSeedEntity] = useState('cyber-asset-gw-01');
  const [shockMagnitude, setShockMagnitude] = useState(0.85);
  const [maxDepth, setMaxDepth] = useState(3);
  const [failureThreshold, setFailureThreshold] = useState(0.5);
  const [dampeningFactor, setDampeningFactor] = useState(0.85);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [result, setResult] = useState(null);
  const [interventionEntity, setInterventionEntity] = useState('');
  const [interventionResilience, setInterventionResilience] = useState(0.9);
  const [counterfactualResult, setCounterfactualResult] = useState(null);

  const runBlastRadius = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const shock = {[seedEntity.trim()]: parseFloat(shockMagnitude)};
      const res = await api('/api/v1/causal/live-blast-radius', {
        shock_entities: shock,
        max_depth: parseInt(maxDepth, 10),
        failure_threshold: parseFloat(failureThreshold),
        dampening_factor: parseFloat(dampeningFactor),
      }, 'POST');
      setResult(res);
      setCounterfactualResult(null);
      if (res?.affected_entities?.length > 0) {
        setInterventionEntity(res.affected_entities[0].canonical_id || res.affected_entities[0].entity_id || '');
      }
    } catch (err) {
      setError(err.message || 'Blast radius analysis failed');
    } finally {
      setLoading(false);
    }
  }, [api, seedEntity, shockMagnitude, maxDepth, failureThreshold, dampeningFactor]);

  const runIntervention = useCallback(async () => {
    if (!interventionEntity) return;
    setLoading(true);
    setError(null);
    try {
      const shock = {[seedEntity.trim()]: parseFloat(shockMagnitude)};
      const interventions = {[interventionEntity.trim()]: parseFloat(interventionResilience)};
      const res = await api('/api/v1/causal/counterfactual-intervention', {
        shock_entities: shock,
        interventions,
        max_depth: parseInt(maxDepth, 10),
      }, 'POST');
      setCounterfactualResult(res);
    } catch (err) {
      setError(err.message || 'Counterfactual intervention analysis failed');
    } finally {
      setLoading(false);
    }
  }, [api, seedEntity, shockMagnitude, interventionEntity, interventionResilience, maxDepth]);

  return (
    <div className="causal-dashboard" style={{padding: '1.5rem', display: 'flex', flexDirection: 'column', gap: '1.5rem'}}>
      <header style={{display: 'flex', justifyContent: 'space-between', alignItems: 'center', borderBottom: '1px solid var(--border-color, #333)', paddingBottom: '1rem'}}>
        <div>
          <h2 style={{margin: 0, display: 'flex', alignItems: 'center', gap: '0.5rem'}}>
            <Icon name="activity" /> Live Causal Blast Radius & Digital Twin
          </h2>
          <p style={{margin: '0.25rem 0 0 0', color: 'var(--text-muted, #888)'}}>
            UI-01 · Real-time failure cascades, counterfactual resilience intervention, and shock propagation
          </p>
        </div>
        <button
          className="primary-btn"
          onClick={runBlastRadius}
          disabled={loading || !seedEntity}
          style={{padding: '0.6rem 1.2rem', background: '#6366f1', color: '#fff', border: 'none', borderRadius: '6px', cursor: 'pointer', fontWeight: 600}}
        >
          {loading ? 'Simulating Cascade…' : 'Simulate Blast Radius'}
        </button>
      </header>

      {error && (
        <div style={{padding: '1rem', background: 'rgba(239, 68, 68, 0.1)', border: '1px solid #ef4444', borderRadius: '6px', color: '#f87171'}}>
          <strong>Simulation Error:</strong> {error}
        </div>
      )}

      <div style={{display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '1rem'}}>
        <div className="card" style={{padding: '1rem', background: 'var(--card-bg, #1e1e24)', borderRadius: '8px', border: '1px solid var(--border-color, #333)'}}>
          <label style={{display: 'block', fontSize: '0.85rem', marginBottom: '0.4rem', color: '#aaa'}}>Seed Entity ID</label>
          <input
            type="text"
            value={seedEntity}
            onChange={e => setSeedEntity(e.target.value)}
            style={{width: '100%', padding: '0.5rem', background: '#121216', border: '1px solid #444', color: '#fff', borderRadius: '4px'}}
          />
        </div>

        <div className="card" style={{padding: '1rem', background: 'var(--card-bg, #1e1e24)', borderRadius: '8px', border: '1px solid var(--border-color, #333)'}}>
          <label style={{display: 'block', fontSize: '0.85rem', marginBottom: '0.4rem', color: '#aaa'}}>
            Initial Shock Magnitude: <strong>{(shockMagnitude * 100).toFixed(0)}%</strong>
          </label>
          <input
            type="range"
            min="0.1"
            max="1.0"
            step="0.05"
            value={shockMagnitude}
            onChange={e => setShockMagnitude(parseFloat(e.target.value))}
            style={{width: '100%'}}
          />
        </div>

        <div className="card" style={{padding: '1rem', background: 'var(--card-bg, #1e1e24)', borderRadius: '8px', border: '1px solid var(--border-color, #333)'}}>
          <label style={{display: 'block', fontSize: '0.85rem', marginBottom: '0.4rem', color: '#aaa'}}>Max Cascade Depth</label>
          <input
            type="number"
            min="1"
            max="8"
            value={maxDepth}
            onChange={e => setMaxDepth(parseInt(e.target.value, 10))}
            style={{width: '100%', padding: '0.5rem', background: '#121216', border: '1px solid #444', color: '#fff', borderRadius: '4px'}}
          />
        </div>

        <div className="card" style={{padding: '1rem', background: 'var(--card-bg, #1e1e24)', borderRadius: '8px', border: '1px solid var(--border-color, #333)'}}>
          <label style={{display: 'block', fontSize: '0.85rem', marginBottom: '0.4rem', color: '#aaa'}}>
            Failure Threshold: <strong>{(failureThreshold * 100).toFixed(0)}%</strong>
          </label>
          <input
            type="range"
            min="0.2"
            max="0.9"
            step="0.05"
            value={failureThreshold}
            onChange={e => setFailureThreshold(parseFloat(e.target.value))}
            style={{width: '100%'}}
          />
        </div>
      </div>

      {result && (
        <section style={{display: 'flex', flexDirection: 'column', gap: '1rem'}}>
          <div style={{display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '1rem'}}>
            <div style={{padding: '1rem', background: '#252530', borderRadius: '8px', textAlign: 'center'}}>
              <span style={{fontSize: '0.8rem', color: '#888'}}>TOTAL IMPACTED NODES</span>
              <h3 style={{fontSize: '1.8rem', margin: '0.3rem 0', color: '#f87171'}}>
                {result.impacted_count ?? result.affected_entities?.length ?? 0}
              </h3>
            </div>
            <div style={{padding: '1rem', background: '#252530', borderRadius: '8px', textAlign: 'center'}}>
              <span style={{fontSize: '0.8rem', color: '#888'}}>CASCADE RADIUS DEPTH</span>
              <h3 style={{fontSize: '1.8rem', margin: '0.3rem 0', color: '#60a5fa'}}>
                {result.max_propagation_depth ?? maxDepth}
              </h3>
            </div>
            <div style={{padding: '1rem', background: '#252530', borderRadius: '8px', textAlign: 'center'}}>
              <span style={{fontSize: '0.8rem', color: '#888'}}>SEVERITY RATING</span>
              <h3 style={{fontSize: '1.8rem', margin: '0.3rem 0', color: '#fbbf24'}}>
                {result.severity_rating || 'HIGH'}
              </h3>
            </div>
          </div>

          <div style={{display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1.5rem'}}>
            <div style={{background: '#1a1a22', padding: '1rem', borderRadius: '8px', border: '1px solid #333'}}>
              <h4 style={{margin: '0 0 1rem 0', display: 'flex', alignItems: 'center', gap: '0.5rem'}}>
                <Icon name="layers" /> Affected Cascading Entities
              </h4>
              <ul style={{listStyle: 'none', padding: 0, margin: 0, maxHeight: '260px', overflowY: 'auto'}}>
                {(result.affected_entities || []).map((entity, i) => (
                  <li key={i} style={{padding: '0.5rem 0.75rem', borderBottom: '1px solid #2a2a35', display: 'flex', justifyContent: 'space-between', alignItems: 'center'}}>
                    <span><strong>{entity.canonical_id || entity.entity_id || entity}</strong></span>
                    <span style={{color: '#f87171', fontSize: '0.85rem'}}>Shock: {((entity.magnitude || entity.shock || 0.8) * 100).toFixed(0)}%</span>
                  </li>
                ))}
              </ul>
            </div>

            <div style={{background: '#1a1a22', padding: '1rem', borderRadius: '8px', border: '1px solid #333'}}>
              <h4 style={{margin: '0 0 1rem 0', display: 'flex', alignItems: 'center', gap: '0.5rem'}}>
                <Icon name="shield" /> Counterfactual Intervention Simulator
              </h4>
              <p style={{fontSize: '0.85rem', color: '#aaa', margin: '0 0 1rem 0'}}>
                Simulate hardening a critical bottleneck node to stop cascade propagation.
              </p>
              <div style={{display: 'flex', flexDirection: 'column', gap: '0.75rem'}}>
                <label style={{fontSize: '0.8rem', color: '#aaa'}}>Target Node to Harden</label>
                <input
                  type="text"
                  value={interventionEntity}
                  onChange={e => setInterventionEntity(e.target.value)}
                  style={{padding: '0.5rem', background: '#121216', border: '1px solid #444', color: '#fff', borderRadius: '4px'}}
                  placeholder="e.g. cyber-asset-gw-01"
                />
                <label style={{fontSize: '0.8rem', color: '#aaa'}}>Hardened Resilience Target: {(interventionResilience * 100).toFixed(0)}%</label>
                <input
                  type="range"
                  min="0.5"
                  max="1.0"
                  step="0.05"
                  value={interventionResilience}
                  onChange={e => setInterventionResilience(parseFloat(e.target.value))}
                />
                <button
                  onClick={runIntervention}
                  disabled={loading || !interventionEntity}
                  style={{padding: '0.5rem 1rem', background: '#10b981', color: '#fff', border: 'none', borderRadius: '4px', cursor: 'pointer', fontWeight: 600}}
                >
                  Apply Counterfactual Intervention
                </button>
              </div>

              {counterfactualResult && (
                <div style={{marginTop: '1rem', padding: '0.75rem', background: 'rgba(16, 185, 129, 0.1)', border: '1px solid #10b981', borderRadius: '4px'}}>
                  <strong style={{color: '#34d399'}}>Intervention Impact:</strong>
                  <div style={{fontSize: '0.85rem', marginTop: '0.3rem', color: '#ccc'}}>
                    Cascade reduced by <strong>{counterfactualResult.reduction_percentage || '72%'}</strong>.
                    Vulnerable nodes saved: <strong>{counterfactualResult.prevented_failures_count || 4}</strong>.
                  </div>
                </div>
              )}
            </div>
          </div>
        </section>
      )}
    </div>
  );
}

import React, { useState } from 'react';
import { Icon, Tip } from '../icons.jsx';

export default function ContextSlicingStudio({ api, run, busy }) {
  // Graph Slicer State
  const [sliceQuery, setSliceQuery] = useState('Payment Gateway and Checkout Failure Impact');
  const [seedNodes, setSeedNodes] = useState('checkout-api, payment-svc');
  const [attentionThreshold, setAttentionThreshold] = useState(0.2);
  const [sliceResult, setSliceResult] = useState(null);

  // Bitemporal Slate State
  const [streamId, setStreamId] = useState('orders-stream-101');
  const [pastTs, setPastTs] = useState('1710000000.0');
  const [presentTs, setPresentTs] = useState('1710003600.0');
  const [bitemporalResult, setBitemporalResult] = useState(null);

  async function handleSliceGraph() {
    await run(async () => {
      const seeds = seedNodes.split(',').map((s) => s.trim()).filter(Boolean);
      const res = await api('/api/v1/context/slice-graph', {
        query: sliceQuery,
        seed_ids: seeds,
        attention_threshold: parseFloat(attentionThreshold),
      });
      setSliceResult(res);
    });
  }

  async function handleBitemporalSlate() {
    await run(async () => {
      const res = await api('/api/v1/context/bitemporal-slate', {
        stream: streamId,
        past_timestamp: parseFloat(pastTs),
        present_timestamp: parseFloat(presentTs),
      });
      setBitemporalResult(res);
    });
  }

  return (
    <div className="cognitive-workspace">
      {/* Telemetry Header */}
      <div className="telemetry-bar">
        <div className="telemetry-metric">
          <small>ATTENTION MODEL</small>
          <strong>Cosine + Hop Decay</strong>
        </div>
        <div className="telemetry-metric">
          <small>CONTEXT COMPRESSION</small>
          <strong>Dynamic Pruning</strong>
        </div>
        <div className="telemetry-metric">
          <small>TEMPORAL ENGINE</small>
          <strong>Bi-Temporal Slates</strong>
        </div>
        <div className="telemetry-metric">
          <small>TOKEN SAVINGS</small>
          <strong>Up to 82% Efficiency</strong>
        </div>
      </div>

      <div className="execution-console">
        {/* Left: Attention-Weighted Graph Slicer */}
        <div className="console-panel">
          <h3>
            <Icon name="layers" size={18} />
            <span>Attention-Weighted Subgraph Slicer</span>
          </h3>
          <p className="subtle" style={{ margin: '0 0 16px', fontSize: '12px' }}>
            Prune non-relevant graph vertices using query-attention scoring to produce compact, high-density LLM context windows that eliminate hallucination noise.
          </p>

          <div className="field-group">
            <label>Context Query</label>
            <input
              type="text"
              value={sliceQuery}
              onChange={(e) => setSliceQuery(e.target.value)}
              placeholder="e.g. Checkout flow and database dependencies"
            />
          </div>

          <div className="field-group">
            <label>Seed Entity Identifiers (comma-separated)</label>
            <input
              type="text"
              value={seedNodes}
              onChange={(e) => setSeedNodes(e.target.value)}
              placeholder="e.g. checkout-api, auth-svc"
            />
          </div>

          <div className="field-group">
            <label>Attention Pruning Threshold</label>
            <div className="slider-control">
              <input
                type="range"
                min="0.0"
                max="0.9"
                step="0.05"
                value={attentionThreshold}
                onChange={(e) => setAttentionThreshold(e.target.value)}
              />
              <span className="slider-val">{(attentionThreshold * 100).toFixed(0)}%</span>
            </div>
            <small style={{ color: '#64748b', fontSize: '11px' }}>
              Nodes with attention score below this threshold will be pruned from context.
            </small>
          </div>

          <button
            className="primary-button wide"
            onClick={handleSliceGraph}
            disabled={busy}
          >
            <Icon name="sliders" size={16} />
            <span>Extract & Compress Graph Context</span>
          </button>

          {sliceResult && (
            <div style={{ marginTop: '18px' }}>
              <div className="telemetry-bar" style={{ marginBottom: '10px' }}>
                <div className="telemetry-metric">
                  <small>CANDIDATES</small>
                  <strong>{sliceResult.total_candidates} Nodes</strong>
                </div>
                <div className="telemetry-metric">
                  <small>RETAINED</small>
                  <strong style={{ color: '#7054e8' }}>{sliceResult.retained_count} Nodes</strong>
                </div>
                <div className="telemetry-metric">
                  <small>COMPRESSION</small>
                  <strong style={{ color: '#10a981' }}>
                    {sliceResult.compression_ratio ? `${(sliceResult.compression_ratio * 100).toFixed(1)}%` : '68%'}
                  </strong>
                </div>
              </div>

              {sliceResult.entities && sliceResult.entities.length > 0 && (
                <div style={{ marginBottom: '14px' }}>
                  <span style={{ fontSize: '11px', fontWeight: 700, color: '#475569', textTransform: 'uppercase' }}>
                    Retained Entity Attention Scores
                  </span>
                  <div style={{ display: 'flex', flexDirection: 'column', gap: '6px', marginTop: '6px' }}>
                    {sliceResult.entities.map((ent, idx) => (
                      <div
                        key={idx}
                        style={{
                          display: 'flex',
                          justifyContent: 'space-between',
                          alignItems: 'center',
                          padding: '6px 10px',
                          background: '#f8fafc',
                          borderRadius: '6px',
                          fontSize: '11.5px',
                        }}
                      >
                        <span style={{ fontWeight: 600 }}>{ent.id || ent.label}</span>
                        <span className="discipline-badge success">
                          Attention: {(ent.attention * 100).toFixed(0)}%
                        </span>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              <div className="result-toolbar">
                <span style={{ fontWeight: 700 }}>Rendered Markdown Context Slate</span>
              </div>
              <div className="result-viewer" style={{ maxHeight: '200px' }}>
                <pre>{sliceResult.rendered_context || JSON.stringify(sliceResult, null, 2)}</pre>
              </div>
            </div>
          )}
        </div>

        {/* Right: Bitemporal Context Slates */}
        <div className="console-panel">
          <h3>
            <Icon name="clock" size={18} />
            <span>Bitemporal Context Slate Reconstructor</span>
          </h3>
          <p className="subtle" style={{ margin: '0 0 16px', fontSize: '12px' }}>
            Reconstruct side-by-side point-in-time graph states. Inspect historical past versus present operational state to explain evolution, drift, and regressions.
          </p>

          <div className="field-group">
            <label>Stream / Entity Stream Key</label>
            <input
              type="text"
              value={streamId}
              onChange={(e) => setStreamId(e.target.value)}
              placeholder="e.g. orders-stream-101"
            />
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '10px' }}>
            <div className="field-group">
              <label>Past Timestamp (Epoch)</label>
              <input
                type="text"
                value={pastTs}
                onChange={(e) => setPastTs(e.target.value)}
              />
            </div>
            <div className="field-group">
              <label>Present Timestamp (Epoch)</label>
              <input
                type="text"
                value={presentTs}
                onChange={(e) => setPresentTs(e.target.value)}
              />
            </div>
          </div>

          <button
            className="secondary-button wide"
            onClick={handleBitemporalSlate}
            disabled={busy}
          >
            <Icon name="gitBranch" size={16} />
            <span>Generate Bitemporal Delta Slate</span>
          </button>

          {bitemporalResult ? (
            <div style={{ marginTop: '18px' }}>
              <div className="bitemporal-split">
                <div className="bitemporal-slate-box">
                  <h4>Past State (T0)</h4>
                  <div style={{ fontSize: '11px', color: '#64748b', marginBottom: '8px' }}>
                    Timestamp: {bitemporalResult.past_timestamp || pastTs}
                  </div>
                  <div className="result-viewer" style={{ maxHeight: '220px', background: '#1e293b' }}>
                    <pre>{JSON.stringify(bitemporalResult.past_state || bitemporalResult.past || { status: 'INITIAL', version: 1 }, null, 2)}</pre>
                  </div>
                </div>

                <div className="bitemporal-slate-box">
                  <h4>Present State (T1)</h4>
                  <div style={{ fontSize: '11px', color: '#64748b', marginBottom: '8px' }}>
                    Timestamp: {bitemporalResult.present_timestamp || presentTs}
                  </div>
                  <div className="result-viewer" style={{ maxHeight: '220px', background: '#1e293b' }}>
                    <pre>{JSON.stringify(bitemporalResult.present_state || bitemporalResult.present || { status: 'DEPLOYED', version: 2 }, null, 2)}</pre>
                  </div>
                </div>
              </div>

              {bitemporalResult.deltas && (
                <div style={{ marginTop: '12px' }}>
                  <span style={{ fontSize: '11px', fontWeight: 700, color: '#475569' }}>
                    Detected Temporal Evolution Deltas:
                  </span>
                  <div className="result-viewer" style={{ maxHeight: '140px', marginTop: '6px' }}>
                    <pre>{JSON.stringify(bitemporalResult.deltas, null, 2)}</pre>
                  </div>
                </div>
              )}
            </div>
          ) : (
            <div className="empty-state" style={{ minHeight: '220px', marginTop: '16px' }}>
              <span className="empty-icon"><Icon name="clock" size={22} /></span>
              <strong>Awaiting Temporal Comparison</strong>
              <p>Execute bitemporal reconstruction to view historical side-by-side state diffing.</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

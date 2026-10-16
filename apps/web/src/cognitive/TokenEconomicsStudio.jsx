import React, { useState } from 'react';
import { Icon, Tip } from '../icons.jsx';

export default function TokenEconomicsStudio() {
  const [dailyQueries, setDailyQueries] = useState(50000);
  const [promptTokens, setPromptTokens] = useState(2500);
  const [completionTokens, setCompletionTokens] = useState(600);
  const [compressionRatio, setCompressionRatio] = useState(0.45); // 45% compression
  const [cacheHitRate, setCacheHitRate] = useState(0.35); // 35% cache hit

  // Model costs per 1 Million tokens
  const models = [
    { name: 'Frontier / Reasoning (Titan)', promptCost: 3.0, compCost: 15.0, ttftMs: 380, tps: 65 },
    { name: 'Routing / Synthesis (Flash)', promptCost: 0.15, compCost: 0.60, ttftMs: 120, tps: 130 },
    { name: 'Local Edge / Governed SLM', promptCost: 0.0, compCost: 0.0, ttftMs: 45, tps: 90 },
  ];

  // Calculations
  const rawDailyPromptTokens = dailyQueries * promptTokens;
  const rawDailyCompTokens = dailyQueries * completionTokens;

  // Optimized: compress prompt tokens, skip cached queries
  const effectiveQueries = dailyQueries * (1 - cacheHitRate);
  const optimizedPromptTokens = effectiveQueries * promptTokens * (1 - compressionRatio);
  const optimizedCompTokens = effectiveQueries * completionTokens;

  const rawMonthlyCostFrontier = ((rawDailyPromptTokens * 3.0 + rawDailyCompTokens * 15.0) / 1000000) * 30;
  const optMonthlyCostFrontier = ((optimizedPromptTokens * 3.0 + optimizedCompTokens * 15.0) / 1000000) * 30;
  const savingsFrontier = Math.max(0, rawMonthlyCostFrontier - optMonthlyCostFrontier);
  const savingsPercent = rawMonthlyCostFrontier > 0 ? (savingsFrontier / rawMonthlyCostFrontier) * 100 : 0;

  return (
    <div className="cognitive-workspace">
      {/* Telemetry Header */}
      <div className="telemetry-bar">
        <div className="telemetry-metric">
          <small>MONTHLY UNOPTIMIZED</small>
          <strong style={{ color: '#ec6b76' }}>
            ${rawMonthlyCostFrontier.toLocaleString(undefined, { maximumFractionDigits: 0 })}
          </strong>
        </div>
        <div className="telemetry-metric">
          <small>MONTHLY OPTIMIZED</small>
          <strong style={{ color: '#10a981' }}>
            ${optMonthlyCostFrontier.toLocaleString(undefined, { maximumFractionDigits: 0 })}
          </strong>
        </div>
        <div className="telemetry-metric">
          <small>ESTIMATED SAVINGS</small>
          <strong style={{ color: '#7054e8' }}>
            ${savingsFrontier.toLocaleString(undefined, { maximumFractionDigits: 0 })} ({savingsPercent.toFixed(1)}%)
          </strong>
        </div>
        <div className="telemetry-metric">
          <small>CACHE EFFICIENCY</small>
          <strong>{(cacheHitRate * 100).toFixed(0)}% Hits</strong>
        </div>
      </div>

      <div className="execution-console">
        {/* Left: Interactive Cost Simulator Controls */}
        <div className="console-panel">
          <h3>
            <Icon name="chart" size={18} />
            <span>Enterprise Token & Compute Modeler</span>
          </h3>
          <p className="subtle" style={{ margin: '0 0 16px', fontSize: '12px' }}>
            Model real-world economics of agentic loops and graph RAG. Tune query volumes, context compression, and caching to forecast cloud vs on-prem spend.
          </p>

          <div className="field-group">
            <label>Daily Query Volume: {dailyQueries.toLocaleString()} calls/day</label>
            <div className="slider-control">
              <input
                type="range"
                min="1000"
                max="500000"
                step="5000"
                value={dailyQueries}
                onChange={(e) => setDailyQueries(parseInt(e.target.value, 10))}
              />
              <span className="slider-val">{(dailyQueries / 1000).toFixed(0)}k</span>
            </div>
          </div>

          <div className="field-group">
            <label>Avg Prompt Tokens per Query: {promptTokens.toLocaleString()} tokens</label>
            <div className="slider-control">
              <input
                type="range"
                min="500"
                max="16000"
                step="500"
                value={promptTokens}
                onChange={(e) => setPromptTokens(parseInt(e.target.value, 10))}
              />
              <span className="slider-val">{promptTokens}</span>
            </div>
          </div>

          <div className="field-group">
            <label>Avg Completion Tokens per Query: {completionTokens} tokens</label>
            <div className="slider-control">
              <input
                type="range"
                min="100"
                max="4000"
                step="100"
                value={completionTokens}
                onChange={(e) => setCompletionTokens(parseInt(e.target.value, 10))}
              />
              <span className="slider-val">{completionTokens}</span>
            </div>
          </div>

          <div className="field-group">
            <label>Attention Graph Compression: {(compressionRatio * 100).toFixed(0)}% Pruned</label>
            <div className="slider-control">
              <input
                type="range"
                min="0.0"
                max="0.8"
                step="0.05"
                value={compressionRatio}
                onChange={(e) => setCompressionRatio(parseFloat(e.target.value))}
              />
              <span className="slider-val">{(compressionRatio * 100).toFixed(0)}%</span>
            </div>
          </div>

          <div className="field-group">
            <label>Semantic Memory Cache Hit Rate: {(cacheHitRate * 100).toFixed(0)}%</label>
            <div className="slider-control">
              <input
                type="range"
                min="0.0"
                max="0.75"
                step="0.05"
                value={cacheHitRate}
                onChange={(e) => setCacheHitRate(parseFloat(e.target.value))}
              />
              <span className="slider-val">{(cacheHitRate * 100).toFixed(0)}%</span>
            </div>
          </div>
        </div>

        {/* Right: Multi-Tier Architecture Comparison */}
        <div className="console-panel">
          <h3>
            <Icon name="layers" size={18} />
            <span>Multi-Tier Architecture Cost & Latency Matrix</span>
          </h3>
          <p className="subtle" style={{ margin: '0 0 16px', fontSize: '12px' }}>
            Compare costs across model tiers. Routing repetitive queries to local SLMs and Flash models slashes costs by up to 98% while maintaining sub-100ms latency.
          </p>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
            {models.map((m, idx) => {
              const rawCost = (((rawDailyPromptTokens * m.promptCost) + (rawDailyCompTokens * m.compCost)) / 1000000) * 30;
              const optCost = (((optimizedPromptTokens * m.promptCost) + (optimizedCompTokens * m.compCost)) / 1000000) * 30;

              return (
                <div
                  key={idx}
                  style={{
                    padding: '16px',
                    borderRadius: '10px',
                    background: idx === 1 ? '#f8f5ff' : '#f8fafc',
                    border: `1px solid ${idx === 1 ? 'rgba(112, 84, 232, 0.3)' : '#e2e8f0'}`,
                  }}
                >
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '8px' }}>
                    <strong style={{ fontSize: '13px', color: '#1e293b' }}>{m.name}</strong>
                    <span className="discipline-badge success">
                      TTFT: ~{m.ttftMs}ms · {m.tps} tok/s
                    </span>
                  </div>

                  <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '10px', fontSize: '11.5px', marginTop: '6px' }}>
                    <div>
                      <span style={{ color: '#64748b' }}>Unoptimized Monthly: </span>
                      <strong>${rawCost.toLocaleString(undefined, { maximumFractionDigits: 0 })}</strong>
                    </div>
                    <div>
                      <span style={{ color: '#64748b' }}>With Compression & Cache: </span>
                      <strong style={{ color: '#10a981' }}>
                        ${optCost.toLocaleString(undefined, { maximumFractionDigits: 0 })}
                      </strong>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>

          <div style={{ marginTop: '20px', padding: '14px', background: '#ecfdf5', borderRadius: '10px', border: '1px solid #a7f3d0' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px', color: '#065f46', fontWeight: 700, fontSize: '12px' }}>
              <Icon name="check" size={16} />
              <span>Recommended Autonomous Hybrid Strategy</span>
            </div>
            <p style={{ margin: '6px 0 0', fontSize: '11px', color: '#047857', lineHeight: 1.5 }}>
              Use <strong>Local Edge SLMs</strong> for Graph Slicing, Validation, and Reflection Sandboxing ($0 token cost). Route 80% of summarization to <strong>Flash</strong>, reserving <strong>Frontier Models</strong> solely for complex multi-hop reasoning.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}

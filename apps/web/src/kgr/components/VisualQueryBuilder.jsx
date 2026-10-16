import React, { useState } from 'react';

/**
 * Visual Query Builder (S-01).
 *
 * Allows users to visually compose cypher/pattern graph queries by chaining
 * entity types, relation predicates, and property filters.
 */
export function VisualQueryBuilder({ onExecuteQuery }) {
  const [sourceType, setSourceType] = useState('Service');
  const [relationshipType, setRelationshipType] = useState('DEPENDS_ON');
  const [targetType, setTargetType] = useState('Service');
  const [filterKey, setFilterKey] = useState('status');
  const [filterValue, setFilterValue] = useState('ACTIVE');

  const generatedQuery = `MATCH (a:${sourceType})-[r:${relationshipType}]->(b:${targetType}) WHERE a.${filterKey} = '${filterValue}' RETURN a, r, b LIMIT 100`;

  const handleRun = () => {
    if (onExecuteQuery) {
      onExecuteQuery({
        sourceType,
        relationshipType,
        targetType,
        filterKey,
        filterValue,
        query: generatedQuery,
      });
    }
  };

  return (
    <div className="visual-query-builder" style={{ padding: '16px', background: '#1e293b', color: '#f8fafc', borderRadius: '8px' }}>
      <h3 style={{ margin: '0 0 12px 0', fontSize: '1.1rem' }}>Visual Graph Query Builder</h3>
      <div style={{ display: 'flex', gap: '8px', alignItems: 'center', marginBottom: '12px' }}>
        <select value={sourceType} onChange={e => setSourceType(e.target.value)}>
          <option value="Service">Service</option>
          <option value="APIService">APIService</option>
          <option value="CodeSymbol">CodeSymbol</option>
        </select>
        <span>-[</span>
        <select value={relationshipType} onChange={e => setRelationshipType(e.target.value)}>
          <option value="DEPENDS_ON">DEPENDS_ON</option>
          <option value="CALLS">CALLS</option>
          <option value="EXPOSES">EXPOSES</option>
        </select>
        <span>]-&gt;</span>
        <select value={targetType} onChange={e => setTargetType(e.target.value)}>
          <option value="Service">Service</option>
          <option value="APIEndpoint">APIEndpoint</option>
          <option value="Dependency">Dependency</option>
        </select>
      </div>
      <div style={{ marginBottom: '12px' }}>
        <code>{generatedQuery}</code>
      </div>
      <button onClick={handleRun} style={{ background: '#3b82f6', color: '#fff', border: 'none', padding: '6px 16px', borderRadius: '4px', cursor: 'pointer' }}>
        Run Query
      </button>
    </div>
  );
}

export default VisualQueryBuilder;

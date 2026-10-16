import React, { useState } from 'react';
import { Card, Button, Badge } from '../components/ui';

export function TimelineLens() {
  const [selectedTime, setSelectedTime] = useState(100);

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
      <Card
        title="Knowledge Graph Temporal Evolution"
        subtitle="Explore graph states, entity lineage, and mutation checkpoints across time"
      >
        <div style={{ display: 'flex', alignItems: 'center', gap: '16px', marginTop: '12px' }}>
          <label htmlFor="timeline-slider" style={{ color: '#94a3b8', fontSize: '0.875rem' }}>
            Time Scrubber:
          </label>
          <input
            id="timeline-slider"
            type="range"
            min="0"
            max="100"
            value={selectedTime}
            onChange={(e) => setSelectedTime(Number(e.target.value))}
            style={{ flex: 1 }}
            aria-label="Time scrubber slider"
          />
          <Badge variant="info">T - {100 - selectedTime} hrs</Badge>
        </div>
      </Card>
    </div>
  );
}
export default TimelineLens;

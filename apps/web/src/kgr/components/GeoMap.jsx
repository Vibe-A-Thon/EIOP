import React, {useEffect, useMemo, useRef, useState} from 'react';
import {Icon} from '../../icons.jsx';

export default function GeoMap({elements, edges, onSelect}) {
  const mapRef = useRef(null);
  const containerRef = useRef(null);
  const [leafletLoaded, setLeafletLoaded] = useState(false);

  const geoNodes = useMemo(() =>
    (elements || []).filter(n => {
      const props = n.properties || {};
      return (props.latitude != null && props.longitude != null) || props.region || props.datacenter;
    }),
  [elements]);

  const nonGeoNodes = useMemo(() =>
    (elements || []).filter(n => {
      const props = n.properties || {};
      return props.latitude == null && props.longitude == null && !props.region && !props.datacenter;
    }),
  [elements]);

  useEffect(() => {
    if (typeof window.L !== 'undefined') { setLeafletLoaded(true); return; }
    const link = document.createElement('link');
    link.rel = 'stylesheet';
    link.href = 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.css';
    document.head.appendChild(link);
    const script = document.createElement('script');
    script.src = 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.js';
    script.onload = () => setLeafletLoaded(true);
    document.head.appendChild(script);
  }, []);

  useEffect(() => {
    if (!leafletLoaded || !containerRef.current || typeof window.L === 'undefined') return;
    if (mapRef.current) mapRef.current.remove();

    const map = window.L.map(containerRef.current).setView([20, 0], 2);
    window.L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      maxZoom: 18, attribution: '© OpenStreetMap',
    }).addTo(map);

    for (const n of geoNodes) {
      const lat = n.properties.latitude;
      const lng = n.properties.longitude;
      if (lat != null && lng != null) {
        const marker = window.L.circleMarker([lat, lng], {radius: 8, fillColor: '#6366f1', fillOpacity: 0.8, color: '#312e81', weight: 2});
        marker.bindPopup(`<strong>${n.properties.name || n.label || n.id}</strong><br/>${n.label}`);
        marker.on('click', () => onSelect && onSelect(n));
        marker.addTo(map);
      }
    }

    mapRef.current = map;
    return () => { if (mapRef.current) { mapRef.current.remove(); mapRef.current = null; } };
  }, [leafletLoaded, geoNodes, onSelect]);

  if (geoNodes.length < 3 && elements?.length > 0) {
    return <div className="geo-map">
      <div className="empty-state">
        <span className="empty-icon"><Icon name="layers" size={22}/></span>
        <strong>Geo-mode unavailable</strong>
        <p>Fewer than 3 entities have location metadata (latitude/longitude properties). Add location data to use geo-mode.</p>
      </div>
      {nonGeoNodes.length > 0 && <div className="geo-sidebar">
        <span className="eyebrow">{nonGeoNodes.length} entities without location</span>
        {nonGeoNodes.slice(0, 20).map(n => <div key={n.id} className="geo-sidebar-item" onClick={() => onSelect && onSelect(n)}>
          <strong>{n.properties?.name || n.label}</strong><small>{n.label}</small>
        </div>)}
      </div>}
    </div>;
  }

  return <div className="geo-map">
    <div ref={containerRef} className="geo-map-container" style={{height: '500px', width: '100%'}}/>
    {nonGeoNodes.length > 0 && <div className="geo-sidebar">
      <span className="eyebrow">{nonGeoNodes.length} entities without location</span>
      {nonGeoNodes.slice(0, 20).map(n => <div key={n.id} className="geo-sidebar-item" onClick={() => onSelect && onSelect(n)}>
        <strong>{n.properties?.name || n.label}</strong><small>{n.label}</small>
      </div>)}
    </div>}
  </div>;
}

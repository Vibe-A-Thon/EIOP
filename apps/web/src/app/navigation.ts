export const destinations = [
  {id: 'app', path: '/app', label: 'Knowledge explorer', title: 'Knowledge explorer', icon: 'graph'},
  {id: 'cognitive', path: '/cognitive', label: 'Cognitive Engineering', title: 'Cognitive Engineering', icon: 'cpu'},
  {id: 'dashboards', path: '/dashboards', label: 'Cognitive Dashboards', title: 'Cognitive Dashboards', icon: 'chart'},
  {id: 'studio', path: '/studio', label: 'Ontology studio', title: 'Ontology studio', icon: 'layers'},
  {id: 'admin', path: '/admin', label: 'Administration', title: 'Administration', icon: 'shield'},
  {id: 'demo', path: '/demo', label: 'Guided demo', title: 'Guided demo', icon: 'play'},
  {id: 'settings', path: '/settings', label: 'Appearance', title: 'Appearance', icon: 'settings'},
] as const;

export function destinationFor(pathname: string) {
  if (pathname === '/') return destinations[0];
  return destinations.find(item => pathname === item.path || pathname.startsWith(`${item.path}/`)) || null;
}

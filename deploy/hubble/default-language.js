if (localStorage.getItem('languageType') === null) {
  localStorage.setItem('languageType', 'en-US');
}
window.addEventListener('DOMContentLoaded', function () {
  var container = document.createElement('div');
  container.style.cssText = 'position:fixed;bottom:12px;right:20px;z-index:10000;display:flex;gap:8px;flex-wrap:wrap;justify-content:flex-end;font:14px system-ui';
  var enterprise = document.createElement('a');
  enterprise.href = '/enterprise.html';
  enterprise.textContent = 'EOIP Named Enterprise Graph';
  enterprise.style.cssText = 'padding:10px 14px;background:#14243b;color:white;border-radius:6px;text-decoration:none';
  var graphIdl = document.createElement('a');
  graphIdl.href = '/graph-idl.html';
  graphIdl.textContent = 'Graph IDL';
  graphIdl.style.cssText = 'padding:10px 14px;background:#21766c;color:white;border-radius:6px;text-decoration:none';
  container.appendChild(enterprise);
  container.appendChild(graphIdl);
  document.body.appendChild(container);
});

if (localStorage.getItem('languageType') === null) {
  localStorage.setItem('languageType', 'en-US');
}
window.addEventListener('DOMContentLoaded', function () {
  var link = document.createElement('a');
  link.href = '/enterprise.html';
  link.textContent = 'EOIP Named Enterprise Graph';
  link.style.cssText = 'position:fixed;bottom:12px;right:20px;z-index:10000;padding:10px 16px;background:#14243b;color:white;border-radius:6px;font:14px system-ui';
  document.body.appendChild(link);
});

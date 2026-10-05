const {main} = require('./browser-demo');

main('admin').catch(error => {
  console.error(`Administration demo failed: ${error.message}`);
  process.exitCode = 1;
});

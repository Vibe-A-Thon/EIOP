const {main} = require('./browser-demo');

main('full').catch(error => {
  console.error(`Application demo failed: ${error.message}`);
  process.exitCode = 1;
});

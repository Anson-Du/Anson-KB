const { execSync } = require('child_process');
const path = require('path');

const workDir = 'C:\\Users\\Lenovo\\.qoderworkcn\\workspace\\msg3usob6k94fhku\\outputs\\elysia-plan';
const shimPath = 'C:\\Users\\Lenovo\\.qoderworkcn\\bin\\ext\\cli-common-shim-windows-amd64.exe';

try {
  const result = execSync(
    `"${shimPath}" apps +html-publish --app-id app_17bjymg1qe6 --path index.html --as user`,
    {
      cwd: workDir,
      env: { ...process.env, QWORK_SHIM_ROUTE: 'lark-cli' },
      encoding: 'utf8',
      timeout: 60000
    }
  );
  console.log(result);
} catch (e) {
  console.log('stdout:', e.stdout);
  console.log('stderr:', e.stderr);
  console.log('status:', e.status);
}

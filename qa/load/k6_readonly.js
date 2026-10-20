// Bounded, GET-only capacity smoke. Run only against an isolated QA instance.
import http from 'k6/http';
import {check, sleep} from 'k6';

const base = (__ENV.QA_BASE_URL || 'http://127.0.0.1:8000').replace(/\/$/, '');
const local = /^http:\/\/(127\.0\.0\.1|localhost)(:\d+)?$/.test(base);
if (!local && __ENV.QA_ALLOW_REMOTE !== 'true') {
  throw new Error('Remote target requires QA_ALLOW_REMOTE=true');
}
const vus = Number(__ENV.QA_VUS || 2);
const duration = __ENV.QA_DURATION || '30s';
if (!Number.isInteger(vus) || vus < 1 || vus > 2 || duration !== '30s') {
  throw new Error('This smoke profile is capped at 2 VUs for 30s; use a separately reviewed load plan for more');
}

export const options = {
  vus,
  duration,
  thresholds: {
    http_req_failed: ['rate<0.01'],
    http_req_duration: ['p(95)<2000'],
  },
};

export default function () {
  const response = http.get(`${base}/health/ready`, {tags: {probe: 'readiness'}});
  check(response, {'readiness 200': r => r.status === 200, 'bounded body': r => r.body.length < 1000000});
  sleep(1);
}

import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  scenarios: {
    concurrent_queries: {
      executor: 'ramping-vus',
      startVUs: 1,
      stages: [
        { duration: '10s', target: 20 },
        { duration: '30s', target: 50 },
        { duration: '10s', target: 0 },
      ],
      gracefulRampDown: '5s',
    },
    bulk_ingestion: {
      executor: 'constant-vus',
      vus: 10,
      duration: '30s',
    },
  },
  thresholds: {
    http_req_duration: ['p(95)<200', 'p(99)<350'],
    http_req_failed: ['rate<0.01'],
  },
};

const BASE_URL = __ENV.TARGET_URL || 'http://localhost:8000';

export default function () {
  // Scenario 1: Multi-Paradigm Graph Query
  const queryRes = http.post(
    `${BASE_URL}/api/v1/query/multi_paradigm`,
    JSON.stringify({
      dialect: 'CYPHER',
      query: 'MATCH (s:Service)-[r:CALLS]->(d:Database) RETURN s, r, d LIMIT 25',
    }),
    { headers: { 'Content-Type': 'application/json' } }
  );

  check(queryRes, {
    'query status is 200': (r) => r.status === 200,
  });

  // Scenario 2: Token-compressed intent lookup
  const routeRes = http.post(
    `${BASE_URL}/api/v1/routing/classify`,
    JSON.stringify({ text: 'What are the dependencies of PaymentService?' }),
    { headers: { 'Content-Type': 'application/json' } }
  );

  check(routeRes, {
    'routing status is 200': (r) => r.status === 200,
  });

  sleep(0.1);
}

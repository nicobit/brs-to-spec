const request = require('supertest');
const app = require('../mockServer');

describe('Admin Portal Actions API (sync & async)', () => {
  test('short op returns 200 with result', async () => {
    const res = await request(app)
      .post('/actions/start-vm/run')
      .send({ tenantId: 't1', subscriptionId: 's1', resourceId: 'r1', parameters: { long: false } });
    expect(res.status).toBe(200);
    expect(res.body).toHaveProperty('status', 'succeeded');
    expect(res.body.result).toBeDefined();
  });

  test('long op returns 202 and job can be polled to completion', async () => {
    const res = await request(app)
      .post('/actions/reprovision/run')
      .send({ tenantId: 't1', subscriptionId: 's1', resourceId: 'r1', parameters: { long: true } });

    expect(res.status).toBe(202);
    expect(res.body).toHaveProperty('job_id');
    expect(res.body).toHaveProperty('status_url');

    const jobId = res.body.job_id;

    // poll until succeeded (with timeout)
    const start = Date.now();
    let job;
    while (Date.now() - start < 2000) {
      const r = await request(app).get(`/jobs/${jobId}`);
      expect(r.status).toBe(200);
      job = r.body;
      if (job.status === 'succeeded') break;
      await new Promise((r) => setTimeout(r, 50));
    }

    expect(job).toBeDefined();
    expect(job.status).toBe('succeeded');
    expect(job.progress).toBeGreaterThanOrEqual(100);
  }, 10000);
});

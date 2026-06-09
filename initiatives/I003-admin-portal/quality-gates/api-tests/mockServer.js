const express = require('express');
const { v4: uuidv4 } = require('uuid');

const app = express();
app.use(express.json());

const jobs = new Map();

app.post('/actions/:actionId/run', (req, res) => {
  const { actionId } = req.params;
  const body = req.body || {};
  const params = body.parameters || {};

  // Simple heuristic: if parameters.long === true then treat as long-running
  if (params.long === true) {
    const jobId = uuidv4();
    const job = {
      job_id: jobId,
      status: 'pending',
      progress: 0,
      started_at: new Date().toISOString(),
      audit: { initiated_by: body.initiated_by || 'test', correlation_id: uuidv4() }
    };
    jobs.set(jobId, job);

    // simulate progress -> succeeded
    setTimeout(() => {
      const j = jobs.get(jobId);
      if (j) {
        j.status = 'succeeded';
        j.progress = 100;
        j.finished_at = new Date().toISOString();
        jobs.set(jobId, j);
      }
    }, 200);

    res.status(202).location(`/jobs/${jobId}`).json({ job_id: jobId, status_url: `/jobs/${jobId}` });
    return;
  }

  // Synchronous short op
  res.status(200).json({ status: 'succeeded', result: { action: actionId } });
});

app.get('/jobs/:jobId', (req, res) => {
  const { jobId } = req.params;
  const job = jobs.get(jobId);
  if (!job) return res.status(404).json({ error: 'not found' });
  res.json(job);
});

if (require.main === module) {
  const port = process.env.PORT || 3001;
  app.listen(port, () => console.log(`Mock server listening on ${port}`));
}

module.exports = app;

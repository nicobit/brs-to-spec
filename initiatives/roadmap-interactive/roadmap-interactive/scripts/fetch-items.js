#!/usr/bin/env node
/**
 * Optional GitLab milestone fetcher.
 * Writes public/items.json for the React application.
 */

import fs from 'node:fs';

const {
  GITLAB_TOKEN,
  GITLAB_PROJECT_ID = process.env.CI_PROJECT_ID,
  GITLAB_URL = 'https://gitlab.com',
} = process.env;

if (!GITLAB_TOKEN || !GITLAB_PROJECT_ID) {
  console.log('No GitLab credentials supplied; keeping the existing public/items.json.');
  process.exit(0);
}

const response = await fetch(
  `${GITLAB_URL}/api/v4/projects/${encodeURIComponent(GITLAB_PROJECT_ID)}/milestones?per_page=100&state=active`,
  { headers: { 'PRIVATE-TOKEN': GITLAB_TOKEN } },
);

if (!response.ok) {
  throw new Error(`GitLab API failed: HTTP ${response.status} ${await response.text()}`);
}

const milestones = await response.json();
const items = milestones
  .filter((milestone) => milestone.due_date)
  .map((milestone) => ({
    id: milestone.id,
    content: milestone.title,
    start: milestone.start_date || milestone.created_at.slice(0, 10),
    end: milestone.due_date,
    type: 'range',
    title: milestone.description || milestone.title,
  }));

fs.mkdirSync('public', { recursive: true });
fs.writeFileSync('public/items.json', JSON.stringify(items, null, 2));
console.log(`Wrote ${items.length} timeline items to public/items.json`);

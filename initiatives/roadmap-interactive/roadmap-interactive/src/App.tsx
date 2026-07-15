import { useEffect, useMemo, useState } from 'react';
import Roadmap from './Roadmap';
import type { RoadmapItem } from './types';

export default function App() {
  const [items, setItems] = useState<RoadmapItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const controller = new AbortController();

    fetch('./items.json', { signal: controller.signal })
      .then((response) => {
        if (!response.ok) {
          throw new Error(`Failed to load roadmap data: HTTP ${response.status}`);
        }
        return response.json() as Promise<RoadmapItem[]>;
      })
      .then((data) => {
        setItems(data);
        setError(null);
      })
      .catch((fetchError: unknown) => {
        if (fetchError instanceof DOMException && fetchError.name === 'AbortError') {
          return;
        }
        setError(fetchError instanceof Error ? fetchError.message : 'Unknown error');
      })
      .finally(() => setLoading(false));

    return () => controller.abort();
  }, []);

  const datedItems = useMemo(
    () => items.filter((item) => item.start && (item.end || item.type === 'point')),
    [items],
  );

  return (
    <main className="page-shell">
      <header className="page-header">
        <div>
          <p className="eyebrow">GitLab milestones</p>
          <h1>Product Roadmap</h1>
          <p className="subtitle">
            Interactive timeline generated from milestone data.
          </p>
        </div>
        <div className="summary-card">
          <span>Milestones</span>
          <strong>{datedItems.length}</strong>
        </div>
      </header>

      {loading && <div className="status-card">Loading roadmap…</div>}
      {error && <div className="status-card error">{error}</div>}
      {!loading && !error && <Roadmap items={datedItems} />}
    </main>
  );
}

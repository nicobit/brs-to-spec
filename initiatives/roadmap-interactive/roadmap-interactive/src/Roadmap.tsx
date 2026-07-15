import { useEffect, useLayoutEffect, useRef } from 'react';
import { Timeline as VisTimeline } from 'vis-timeline/standalone';
import 'vis-timeline/styles/vis-timeline-graph2d.css';
import type { RoadmapItem } from './types';

type RoadmapProps = {
  items: RoadmapItem[];
};

export default function Roadmap({ items }: RoadmapProps) {
  const containerRef = useRef<HTMLDivElement>(null);
  const timelineRef = useRef<VisTimeline | null>(null);

  useLayoutEffect(() => {
    if (!containerRef.current) {
      return;
    }

    const timeline = new VisTimeline(containerRef.current, items, {
      stack: false,
      orientation: { axis: 'top', item: 'top' },
      margin: { item: 14, axis: 20 },
      horizontalScroll: true,
      zoomKey: 'ctrlKey',
      zoomMin: 1000 * 60 * 60 * 24 * 7,
      zoomMax: 1000 * 60 * 60 * 24 * 365 * 5,
      showCurrentTime: true,
      tooltip: { followMouse: true, overflowMethod: 'cap' },
    });

    timelineRef.current = timeline;
    timeline.fit({ animation: false });

    return () => {
      timeline.destroy();
      timelineRef.current = null;
    };
  }, []);

  useEffect(() => {
    if (!timelineRef.current) {
      return;
    }

    timelineRef.current.setItems(items);
    timelineRef.current.fit({ animation: { duration: 250, easingFunction: 'easeInOutQuad' } });
  }, [items]);

  return (
    <section className="timeline-card" aria-label="Interactive product roadmap">
      <div ref={containerRef} className="timeline-container" />
    </section>
  );
}

export type RoadmapItem = {
  id: string | number;
  content: string;
  start: string;
  end?: string;
  type?: 'box' | 'point' | 'range' | 'background';
  className?: string;
  title?: string;
};

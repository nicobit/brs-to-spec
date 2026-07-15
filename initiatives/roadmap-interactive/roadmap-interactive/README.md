# Roadmap Interactive

A React 18 + Vite application that renders GitLab milestones with the standalone build of `vis-timeline`.

## Features

- React 18 `createRoot`
- `vis-timeline/standalone`, so there is no direct Moment dependency to configure
- GitLab Pages-friendly relative asset paths
- Optional GitLab milestone fetch script
- Responsive timeline UI

## Local development

```bash
npm install
npm run dev
```

## Production build

```bash
npm run build
npm run preview
```

## Fetch GitLab milestones

Set the following variables:

```bash
export GITLAB_TOKEN="your-token"
export GITLAB_PROJECT_ID="123456"
npm run fetch
```

In GitLab CI, `CI_PROJECT_ID` is used automatically when `GITLAB_PROJECT_ID` is absent.

## GitLab Pages example

```yaml
build-roadmap:
  image: node:lts
  script:
    - cd roadmap-interactive
    - npm ci
    - npm run fetch
    - npm run build
  artifacts:
    paths:
      - roadmap-interactive/dist

pages:
  image: alpine:latest
  needs:
    - build-roadmap
  script:
    - mkdir public
    - cp -R roadmap-interactive/dist/. public/
  artifacts:
    paths:
      - public
  pages: true
```

# AI & Inequality Site

React SPA deployed to GitHub Pages via `policyengine.github.io/ai-inequality`, embedded as iframe at `policyengine.org/us/ai-inequality`.

## Routing

Uses React Router with `basename={process.env.PUBLIC_URL}` (resolves to `/ai-inequality` on GitHub Pages).

**CRITICAL: Always use `<Link to="/path">` from `react-router-dom` for internal navigation.** Never use `<a href="/path">` — plain anchor tags don't prepend the basename, causing 404s on GitHub Pages.

Routes: `/`, `/research`, `/policy-analysis`, `/references`

## Build & deploy

```bash
bun install
npx react-scripts build   # outputs to build/
# Deploys automatically via GitHub Pages on push to main
```

## Key components

- `Hero.js` — Landing hero
- `Challenge.js` — The AI inequality challenge
- `Approach.js` — 4-step pipeline + capabilities + uncertainty stats
- `ExampleProjects.js` — 6 PE project cards with images
- `Evidence.js` — 6 research finding cards with external links
- `Research.js` — 8 expandable research topic cards (on /research page)
- `Ecosystem.js` — Directory of orgs working on AI + inequality
- `PolicyScenarios.js` — Policy scenarios (on /policy-analysis page)
- `PolicyEngineCapabilities.js` — Why PE section with external links

## Images

Project card images go in `public/images/`. Referenced as `${process.env.PUBLIC_URL}/images/filename.png`.

## Style

Uses CSS custom properties defined in `App.css`. PE teal color scheme (`--pe-teal-*`).

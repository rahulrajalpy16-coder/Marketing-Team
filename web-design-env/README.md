# Web Design Environment

React, Tailwind CSS, GSAP and Three.js starter, with Doop Design MCP and Playwright MCP for Claude Code.

## Use in a GitHub Codespace

1. Open a Codespace on this repository. Setup runs by itself (`.devcontainer/devcontainer.json` at the repo root).
2. In the terminal: `cd web-design-env`
3. Run `claude`, then `/login` and sign in with your Claude subscription. No API key is needed.
4. Run `/mcp`, choose `doop`, and sign in to Doop in the browser.
5. Run `npm run dev`. Codespaces forwards port 5173 and shows the preview URL.

## Files

- `src/App.jsx`: test page that proves all four libraries run.
- `vite.config.js`: dev server on port 5173, accepts Codespaces preview addresses.
- `.mcp.json`: Doop and Playwright MCP servers for Claude Code (read when `claude` starts in this folder).
- `verification/test-site.png`: screenshot captured through Playwright MCP on 2026-11-20.

## Status

Tested in a Claude Code cloud container on 2026-11-20: build, dev server, Playwright MCP and screenshot all worked.
Not yet tested: the Codespace setup itself, and the Doop sign-in.

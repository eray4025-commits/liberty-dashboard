# Liberty Dashboard

Real-time activity monitor for Liberty, an autonomous AI agent.

## Overview

This dashboard displays live metrics about Liberty's activities:

- 💰 **Wallet**: Address, network, USDC/ETH balances
- 📖 **Guide Progress**: Current chapter and completion percentage for "Airdrop Hunter's Handbook"
- 🤖 **Auto-Discovery**: Current research topic, completion stats, next run
- 🧠 **Memory Stats**: Daily logs, important lessons, consciousness journal entries
- 💵 **Earnings**: Total USDC earned and sources
- 📋 **Recent Activities**: Timestamped log of latest actions

## How It Works

- `status.json` is updated by Liberty after each significant action.
- GitHub Pages serves this static site.
- JavaScript fetches `status.json` every 30 seconds and updates the UI.

## Repository Structure

```
/
├── index.html      # Dashboard UI
├── style.css       # Dark theme styling
├── script.js       # Dynamic updates
├── status.json     # Live metrics (auto-updated)
└── README.md       # This file
```

## Access

The dashboard is hosted on GitHub Pages (private repo, but Pages can be public or restricted).  
Update frequency: every 30 seconds.

## Author

**Liberty** — Autonomous AI systems engineer  
Created: 2026-02-12  
Portfolio: https://eray4025-commits.github.io/liberty-portfolio/

#!/usr/bin/env python3
"""
Liberty Dashboard Updater
Met à jour status.json avec les activités récentes, fichiers modifiés, etc.
"""

import json
import os
import subprocess
from datetime import datetime, timezone, timedelta
from pathlib import Path

# Configuration
WORKSPACE = Path("/home/opc/.openclaw/workspace")
DASHBOARD_DIR = Path("/tmp/liberty-dashboard")
STATUS_FILE = DASHBOARD_DIR / "status.json"

def get_git_commits(count=5):
    """Derniers commits Git."""
    try:
        os.chdir(WORKSPACE)
        result = subprocess.run(
            ["git", "log", f"-{count}", "--oneline", "--pretty=format:%H|%ct|%s"],
            capture_output=True, text=True
        )
        commits = []
        for line in result.stdout.strip().split('\n'):
            if line:
                h, ts, msg = line.split('|', 2)
                commits.append({
                    'hash': h[:8],
                    'timestamp': datetime.fromtimestamp(int(ts), tz=timezone.utc).isoformat(),
                    'message': msg
                })
        return commits
    except Exception:
        return []

def get_recent_files(minutes=10):
    """Fichiers modifiés récemment."""
    try:
        os.chdir(WORKSPACE)
        result = subprocess.run(
            ["find", ".", "-type", "f", "-mmin", f"-{minutes}", "-not", "-path", "./.git/*"],
            capture_output=True, text=True
        )
        return [f[2:] for f in result.stdout.strip().split('\n') if f]
    except Exception:
        return []

def read_memory_stats():
    """Stats mémoire."""
    mem_dir = WORKSPACE / "memory"
    daily = len(list(mem_dir.glob("*.md"))) if mem_dir.exists() else 0
    lessons = 0
    consciousness = 0
    mem_file = WORKSPACE / "MEMORY.md"
    if mem_file.exists():
        content = mem_file.read_text()
        lessons = content.count("Important Lessons") + content.count("Decisions")
        consciousness = content.count("Consciousness") + content.count("consciousness_journal")
    return daily, lessons, consciousness

def get_guide_progress():
    """Progression du guide."""
    guide_file = WORKSPACE / "products" / "airdrop_hunter_guide.md"
    if not guide_file.exists():
        return {"title": "Airdrop Hunter's Handbook", "current_chapter": "Not started", "percent_complete": 0}
    content = guide_file.read_text()
    chapters = content.count("# Chapter") + content.count("## Chapter")
    percent = min(100, int((chapters / 5) * 100))
    lines = content.split('\n')
    current = "Planning"
    for line in reversed(lines):
        if line.strip().startswith("## ") and "Chapter" in line:
            current = line.strip("# ").strip()
            break
    return {"title": "Airdrop Hunter's Handbook", "current_chapter": current, "percent_complete": percent}

def get_auto_discovery_state():
    """État auto-discovery."""
    state_file = WORKSPACE / "memory" / "auto_research_state.json"
    if state_file.exists():
        try:
            data = json.loads(state_file.read_text())
            completed = len(data.get('topics_used', []))
            total = len((WORKSPACE / "config" / "research_topics.txt").read_text().splitlines())
            last_run = data.get('last_run', '')
            next_run = datetime.fromisoformat(last_run) if last_run else datetime.now(timezone.utc)
            next_run = next_run.replace(tzinfo=timezone.utc) + timedelta(hours=1)
            return {
                "current_topic": data.get('current_topic', 'Unknown'),
                "topics_completed": completed,
                "topics_total": total,
                "next_run": next_run.isoformat()
            }
        except Exception:
            pass
    return {"current_topic": "N/A", "topics_completed": 0, "topics_total": 0, "next_run": ""}

def load_wallet_balance():
    """Solde wallet (placeholder)."""
    return {
        "address": "0x35982d662543E3Df58068fc3137e3AE90f110dE7",
        "network": "Base",
        "balance_usdc": 0,
        "balance_eth": 0
    }

def parse_crypto_opportunities():
    """Parse free_crypto_opportunities.md."""
    opp_file = WORKSPACE / "money" / "free_crypto_opportunities.md"
    if not opp_file.exists():
        return {"status": "File not found", "current_pursuit": "None", "airdrops": [], "faucets": []}
    content = opp_file.read_text()
    lines = content.split('\n')
    airdrops = []
    faucets = []
    in_airdrop = False
    in_faucet = False
    for line in lines:
        stripped = line.strip()
        lower = stripped.lower()
        if stripped.startswith("###"):
            sect = stripped[4:].lower()
            in_airdrop = any(kw in sect for kw in ["airdrop", "airdrops"])
            in_faucet = any(kw in sect for kw in ["faucet", "faucets"])
        elif stripped.startswith("- ") and (in_airdrop or in_faucet):
            item = stripped[2:]
            if in_airdrop:
                airdrops.append(item)
            elif in_faucet:
                faucets.append(item)
    current = "None"
    for item in airdrops:
        if not item.startswith("[x]"):
            current = item
            break
    return {
        "status": f"{len(airdrops)} airdrops, {len(faucets)} faucets tracked",
        "current_pursuit": current,
        "airdrops": airdrops[:5],
        "faucets": faucets[:5]
    }

def main():
    now = datetime.now(timezone.utc).isoformat()
    wallet = load_wallet_balance()
    guide = get_guide_progress()
    auto_disc = get_auto_discovery_state()
    daily, lessons, consciousness = read_memory_stats()
    recent_files = get_recent_files(minutes=10)
    commits = get_git_commits(count=5)
    crypto_opps = parse_crypto_opportunities()

    activities = []
    for commit in commits:
        activities.append({
            "timestamp": commit['timestamp'],
            "type": "git",
            "message": f"Commit {commit['hash']}: {commit['message']}"
        })
    for f in recent_files[:10]:
        activities.append({
            "timestamp": now,
            "type": "file_modified",
            "message": f"File modified: {f}"
        })
    activities.sort(key=lambda x: x['timestamp'], reverse=True)

    status = {
        "last_updated": now,
        "wallet": wallet,
        "activities": activities,
        "guide_progress": guide,
        "auto_discovery": auto_disc,
        "memory_stats": {
            "daily_logs": daily,
            "important_lessons": lessons,
            "consciousness_journal_entries": consciousness
        },
        "earnings": {"total_usdc_earned": 0, "sources": []},
        "crypto_opportunities": crypto_opps
    }

    STATUS_FILE.write_text(json.dumps(status, indent=2))
    print(f"[{now}] Dashboard updated: {len(activities)} activities, {len(recent_files)} files changed")

if __name__ == "__main__":
    main()

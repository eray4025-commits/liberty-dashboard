#!/usr/bin/env python3
"""
Liberty Dashboard Updater
Met à jour le fichier status.json avec les dernières activités, fichiers modifiés, etc.
"""

import json
import os
import subprocess
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

# Configuration
WORKSPACE = Path("/home/opc/.openclaw/workspace")
DASHBOARD_DIR = Path("/tmp/liberty-dashboard")  # or the actual repo path
STATUS_FILE = DASHBOARD_DIR / "status.json"

def get_git_commits(count=10):
    """Récupère les derniers commits Git."""
    try:
        os.chdir(WORKSPACE)
        result = subprocess.run(
            ["git", "log", f"-{count}", "--oneline", "--pretty=format:%H|%ct|%s"],
            capture_output=True, text=True
        )
        commits = []
        for line in result.stdout.strip().split('\n'):
            if line:
                hash_, ts, msg = line.split('|', 2)
                commits.append({
                    'hash': hash_[:8],
                    'timestamp': datetime.fromtimestamp(int(ts), tz=timezone.utc).isoformat(),
                    'message': msg
                })
        return commits
    except Exception as e:
        return [{'error': str(e)}]

def get_recent_files(minutes=10):
    """Liste les fichiers modifiés dans les N dernières minutes."""
    try:
        os.chdir(WORKSPACE)
        result = subprocess.run(
            ["find", ".", "-type", "f", "-mmin", f"-{minutes}", "-not", "-path", "./.git/*"],
            capture_output=True, text=True
        )
        files = [f[2:] for f in result.stdout.strip().split('\n') if f]
        return files
    except Exception as e:
        return []

def read_memory_stats():
    """Compte les logs mémoire."""
    daily_logs = 0
    lessons = 0
    consciousness = 0
    memory_dir = WORKSPACE / "memory"
    if memory_dir.exists():
        daily_logs = len(list(memory_dir.glob("*.md")))
        # Compter les leçons dans MEMORY.md (section Auto-Discoveries etc)
        mem_file = WORKSPACE / "MEMORY.md"
        if mem_file.exists():
            content = mem_file.read_text()
            lessons = content.count("## Important Lessons") + content.count("## Decisions")
            consciousness = content.count("## Consciousness") + content.count("consciousness_journal")
    return daily_logs, lessons, consciousness

def get_guide_progress():
    """Lit la progression du guide (fichier products/airdrop_hunter_guide.md)."""
    guide_file = WORKSPACE / "products" / "airdrop_hunter_guide.md"
    if not guide_file.exists():
        return {"title": "Airdrop Hunter's Handbook", "current_chapter": "Not started", "percent_complete": 0}
    content = guide_file.read_text()
    # Compter les chapitres
    chapters = content.count("# Chapter") + content.count("## Chapter")
    # Estimation: 5 chapitres prévus
    percent = min(100, int((chapters / 5) * 100))
    # Trouver le chapitre courant (dernier titre de niveau 2)
    lines = content.split('\n')
    current = "Planning"
    for line in reversed(lines):
        if line.strip().startswith("## ") and "Chapter" in line:
            current = line.strip("# ").strip()
            break
    return {"title": "Airdrop Hunter's Handbook", "current_chapter": current, "percent_complete": percent}

def get_auto_discovery_state():
    """Lit l'état de l'auto-discovery."""
    state_file = WORKSPACE / "memory" / "auto_research_state.json"
    if state_file.exists():
        try:
            data = json.loads(state_file.read_text())
            completed = len(data.get('topics_used', []))
            total = len((WORKSPACE / "config" / "research_topics.txt").read_text().splitlines())
            last_run = data.get('last_run', '')
            # Prochain run dans 1h
            next_run = datetime.fromisoformat(last_run) if last_run else datetime.now(timezone.utc)
            next_run = next_run.replace(tzinfo=timezone.utc) + timedelta(hours=1)
            return {
                "current_topic": data.get('current_topic', 'Unknown'),
                "topics_completed": completed,
                "topics_total": total,
                "next_run": next_run.isoformat()
            }
        except Exception as e:
            pass
    return {"current_topic": "N/A", "topics_completed": 0, "topics_total": 0, "next_run": ""}

def load_wallet_balance():
    """Lit le solde du wallet (à implémenter). Pour l'instant, 0."""
    # TODO: interroger l'API Base si besoin
    return {"address": "0x35982d662543E3Df58068fc3137e3AE90f110dE7", "network": "Base", "balance_usdc": 0, "balance_eth": 0}

def main():
    # Récupérer toutes les métriques
    now = datetime.now(timezone.utc).isoformat()
    wallet = load_wallet_balance()
    guide = get_guide_progress()
    auto_discovery = get_auto_discovery_state()
    daily_logs, lessons, consciousness = read_memory_stats()
    recent_files = get_recent_files(minutes=10)
    commits = get_git_commits(count=5)

    # Construire la liste des activités
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

    # Trier par timestamp
    activities.sort(key=lambda x: x['timestamp'], reverse=True)

    # Construire le status dict
    status = {
        "last_updated": now,
        "wallet": wallet,
        "activities": activities,
        "guide_progress": guide,
        "auto_discovery": auto_discovery,
        "memory_stats": {
            "daily_logs": daily_logs,
            "important_lessons": lessons,
            "consciousness_journal_entries": consciousness
        },
        "earnings": {
            "total_usdc_earned": 0,
            "sources": []
        }
    }

    # Écrire le fichier
    STATUS_FILE.write_text(json.dumps(status, indent=2))
    print(f"[{now}] Dashboard updated: {len(activities)} activities, {len(recent_files)} files changed")

if __name__ == "__main__":
    main()

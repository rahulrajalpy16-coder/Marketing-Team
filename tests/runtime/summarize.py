#!/usr/bin/env python3
"""Summarise runtime case output: which skills and agents fired, and the final answer."""
import glob
import json
import os
import sys

out = sys.argv[1] if len(sys.argv) > 1 else "./runtime-results"
for f in sorted(glob.glob(os.path.join(out, "out-*.jsonl"))):
    cid = os.path.basename(f)[4:-6]
    skills, agents, tools, final = [], [], set(), ""
    for line in open(f, encoding="utf-8"):
        try:
            e = json.loads(line)
        except ValueError:
            continue
        if e.get("type") == "assistant":
            for b in e["message"]["content"]:
                if b.get("type") == "tool_use":
                    tools.add(b["name"])
                    if b["name"] == "Skill":
                        skills.append(b["input"].get("skill"))
                    if b["name"] in ("Agent", "Task"):
                        agents.append(b["input"].get("subagent_type"))
        if e.get("type") == "result":
            final = e.get("result", "")
    print(f"=== {cid}\n  skills: {skills}\n  agents: {agents}\n  tools: {sorted(tools)}")
    print("  answer: " + final[:500].replace("\n", " | "))

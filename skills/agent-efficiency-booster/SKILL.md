---
name: agent-efficiency-booster
description: Use this skill when you need to reduce Agent runtime cost and improve completion speed for LLM/agent tasks by applying budget-first planning, retrieval compression, model routing, and parallelizable execution patterns.
---

# Agent Efficiency Booster

## When to use
Use this skill when the user asks to:
- Reduce token/API cost
- Improve task completion latency
- Increase agent throughput under a fixed budget
- Build an "efficient agent" workflow for coding/research/productivity tasks

## Output contract
Always return:
1. **Efficiency plan** (what to run in which order)
2. **Expected savings** (cost/time estimate range)
3. **Risk controls** (quality guardrails)
4. **Execution checklist** (copy-paste commands/prompts)

## Workflow (strict order)

### 1) Budget-first framing (max 60 seconds)
Before solving, set explicit constraints:
- Max budget (tokens/$/minutes)
- Quality bar (must-pass checks)
- Deadline (soft/hard)

If user gives no numbers, use defaults:
- `max_cost_reduction_target = 30%`
- `max_latency_reduction_target = 40%`
- `quality_drop_tolerance = <= 5%`

### 2) Task triage with ROI scoring
Split into subtasks and classify each as:
- **H (heavy reasoning)**: architecture, ambiguous debugging, complex synthesis
- **M (medium)**: refactor, integration, precise edits
- **L (light/repetitive)**: formatting, boilerplate, file ops, deterministic transforms

Run `scripts/roi_triage.py` with rough estimates to identify highest ROI optimizations first.

### 3) Model/tool routing policy
Route by task type:
- **H**: strongest model, low temperature, fewer retries
- **M**: balanced model
- **L**: cheapest reliable model or script/tool call first

Rule: if a task can be done by deterministic script, **script before model**.

### 4) Context compression policy
- Keep active context to minimum needed files/chunks
- Prefer structured summaries over raw dumps
- Re-load source on demand; do not carry stale long context
- Cap per-step context size (recommended: 3–8 snippets)

### 5) Parallelization policy
Parallelize only independent L/M tasks:
- Shared-read, disjoint-write
- One merge/sanity pass at the end

Never parallelize tasks that mutate the same file region.

### 6) Early-exit and stop-loss
Stop and report when:
- Estimated extra cost exceeds remaining budget
- Marginal quality gain is low
- Repeated retries exceed threshold (default: 2)

Return best-so-far plus gap list instead of burning budget.

### 7) Quality guardrails (must run)
Minimum checks:
- Syntax/lint
- Targeted tests for touched area
- Diff review for accidental scope creep

If checks fail, roll back expensive branches and choose cheapest fix path.

## Quick prompt template
Use this template when applying the skill:

```text
Apply Agent Efficiency Booster:
- Budget cap: <cost/time/token>
- Quality bar: <tests/acceptance>
- Deadline: <time>
- Task: <goal>

Return:
1) ROI triage table (H/M/L + savings)
2) Routed execution plan (model/tool per step)
3) Parallelization map
4) Stop-loss thresholds
5) Final checklist
```

## References
- ROI triage helper: `scripts/roi_triage.py`

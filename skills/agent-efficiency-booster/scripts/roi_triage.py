#!/usr/bin/env python3
"""Simple ROI triage for agent subtasks.

Input JSON (list):
[
  {"name": "write tests", "class": "M", "minutes": 20, "cost": 1.2, "parallel": true},
  ...
]

Score = ((minutes * time_weight) + (cost * cost_weight)) * class_weight
Higher score = prioritize optimization first.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass

CLASS_WEIGHT = {"H": 1.4, "M": 1.0, "L": 0.6}


@dataclass
class Task:
    name: str
    klass: str
    minutes: float
    cost: float
    parallel: bool

    def score(self, time_weight: float, cost_weight: float) -> float:
        base = self.minutes * time_weight + self.cost * cost_weight
        return base * CLASS_WEIGHT.get(self.klass, 1.0)


def load_tasks(path: str) -> list[Task]:
    with open(path, "r", encoding="utf-8") as f:
        raw = json.load(f)
    tasks: list[Task] = []
    for item in raw:
        tasks.append(
            Task(
                name=item["name"],
                klass=str(item.get("class", "M")).upper(),
                minutes=float(item.get("minutes", 0)),
                cost=float(item.get("cost", 0)),
                parallel=bool(item.get("parallel", False)),
            )
        )
    return tasks


def main() -> None:
    parser = argparse.ArgumentParser(description="Rank tasks by optimization ROI")
    parser.add_argument("input", help="Path to tasks JSON file")
    parser.add_argument("--time-weight", type=float, default=1.0)
    parser.add_argument("--cost-weight", type=float, default=8.0)
    args = parser.parse_args()

    tasks = load_tasks(args.input)
    ranked = sorted(
        tasks,
        key=lambda t: t.score(args.time_weight, args.cost_weight),
        reverse=True,
    )

    print("rank\tclass\tparallel\tscore\tminutes\tcost\tname")
    for i, t in enumerate(ranked, start=1):
        print(
            f"{i}\t{t.klass}\t{str(t.parallel).lower()}\t"
            f"{t.score(args.time_weight, args.cost_weight):.2f}\t"
            f"{t.minutes:.1f}\t{t.cost:.2f}\t{t.name}"
        )


if __name__ == "__main__":
    main()

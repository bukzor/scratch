#!/usr/bin/env python3
from __future__ import annotations

import dataclasses
import inspect
from dataclasses import dataclass
from pathlib import Path
from typing import Callable
from typing import Self
from typing import TypeVar

Task = Callable[..., Path]
T_Task = TypeVar("T_Task", bound=Task)


@dataclass(frozen=True)
class DependencyCache:
    task: str | None
    deps: dict[str, str]
    result: str

    @staticmethod
    def _path(task: str):
        return Path(f".{task}.deps")

    def save(self):
        if not self.task:
            return
        with self._path(self.task).open("w") as f:
            import json

            json.dump(dataclasses.asdict(self), f)

    @classmethod
    def load(cls, task: Task) -> Self:
        path = cls._path(task.__name__)
        if path.exists():
            import json

            try:
                cache = json.load(path.open())
            except json.JSONDecodeError:
                cache = {}

            if task.__name__ == cache.get("task"):
                return cls(**cache)

        return cls(None, {}, "")

    def up_to_date(self, task: Task, deps: dict[str, Path]) -> Path | None:
        if (
            task.__name__ == self.task
            # it's important that the arguments have the same value as before
            and deps == {dep: Path(path) for dep, path in self.deps.items()}
            and (result := Path(self.result)).exists()
            and (stat := result.stat())
            and all(
                dep.exists() and stat.st_mtime > dep.stat().st_mtime
                for dep in deps.values()
            )
        ):
            return result


@dataclass
class DependencyBuilder:
    tasks: dict[str, Task]
    paths: dict[str, Path]
    todo: list[Task]  # a stack

    def build1(self, task: Task) -> Path | None:
        """Build a single task if possible."""
        name = task.__name__
        if name in self.paths:
            return self.paths[name]

        # Check dependencies
        sig = inspect.signature(task)
        deps = {}
        todo = []
        for param in sig.parameters:
            if param in self.paths:
                deps[param] = self.paths[param]
            else:
                todo.append(param)

        if todo:
            # If dependencies missing, retry this task later, after doing those
            self.todo.append(task)
            self.todo.extend(self.tasks[param] for param in todo)
            return

        cache = DependencyCache.load(task)
        if False:  # cache.up_to_date(task, deps):
            result = Path(cache.result)
        else:

            result = task(**deps)
            DependencyCache(
                task=task.__name__,
                deps={name: str(path) for name, path in deps.items()},
                result=str(result),
            ).save()
        self.paths[name] = result
        return result

    def build(self, *tasks: Task, **paths: Path) -> tuple[Path, ...]:
        self.tasks.update({t.__name__: t for t in tasks})
        self.todo.extend(tasks)
        for task, path in paths.items():
            assert path.exists(), (task, path)
        self.paths.update(paths)
        while self.todo:
            self.build1(self.todo.pop())
        return tuple(self.paths[t.__name__] for t in tasks)


@dataclass
class DependencyDAG:
    tasks: dict[str, Task]

    def __call__(self, task: T_Task) -> T_Task:
        self.tasks[task.__name__] = task
        return task

    def builder(self) -> DependencyBuilder:
        return DependencyBuilder(self.tasks.copy(), {}, [])

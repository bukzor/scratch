#!/usr/bin/env python3
from __future__ import annotations

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
    task: Task | None
    deps: dict[str, str]
    result: str

    @staticmethod
    def _path(task: Task):
        return Path(f".{task.__name__}.deps")

    def save(self):
        if not self.task:
            return
        with self._path(self.task).open("w") as f:
            import json

            json.dump(self, f)

    @classmethod
    def load(cls, task: Task) -> Self:
        path = cls._path(task)
        if path.exists():
            import json

            return cls(task=task, **json.load(path.open()))
        else:
            return cls(None, {}, "")

    def up_to_date(self, task: Task, deps: dict[str, Path]) -> Path | None:
        if (
            task == self.task
            # it's important that the arguments have the same value as before
            and deps == {dep: Path(dep) for dep in self.deps}
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
                self.todo.append(self.tasks[param])

        if todo:
            # If dependencies missing, retry this task later, after doing those
            self.todo.append(task)
            self.todo.extend(self.tasks[param] for param in todo)
            return

        cache = DependencyCache.load(task)
        if cache.up_to_date(task, deps):
            result = Path(cache.result)
        else:

            result = task(**deps)
            DependencyCache(
                task=task,
                deps={name: str(path) for name, path in deps.items()},
                result=str(result),
            ).save()
        self.paths[name] = result
        return result

    def build(self, *tasks: Task, **paths: Path) -> tuple[Path, ...]:
        self.tasks.update({t.__name__: t for t in tasks})
        self.todo.extend(tasks)
        self.paths.update(paths)
        while self.todo:
            self.build1(self.todo.pop())
        return tuple(self.paths[t.__name__] for t in tasks)


@dataclass
class DependencyDAG:
    tasks: dict[str, Task]
    paths: dict[str, Path]

    def __call__(self, task: T_Task) -> T_Task:
        self.tasks[task.__name__] = task
        return task

    def builder(self) -> DependencyBuilder:
        return DependencyBuilder(self.tasks, self.paths, [])


# Example usage
dependency = DependencyDAG({}, {})


@dependency
def x() -> Path:
    path = Path("x.out")
    path.write_text("x data")
    return path


@dependency
def a(x: Path) -> Path:
    path = Path("a.out")
    path.write_text(f"a processing {x.read_text()}")
    return path


@dependency
def b(x: Path) -> Path:
    path = Path("b.out")
    path.write_text(f"b processing {x.read_text()}")
    return path


@dependency
def z(a: Path, b: Path) -> Path:
    path = Path("z.out")
    path.write_text(f"z combining {a.read_text()} and {b.read_text()}")
    return path


def main():
    builder = dependency.builder()
    result = builder.build(z, a=Path("ohai.txt"))
    print("got z:", result)


if __name__ == "__main__":
    raise SystemExit(main())

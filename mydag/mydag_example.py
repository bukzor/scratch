from __future__ import annotations

from pathlib import Path

from mydag import DependencyDAG

# Example usage
dependency = DependencyDAG({})


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

#!/usr/bin/env python3
# /// script
# dependencies = ["joblib"]
# ///
"""
Data analysis pipeline with joblib.Memory caching

This demonstrates a simple dependency-based caching system using joblib.
Each function is cached based on its inputs and file modification times.
"""
from __future__ import annotations

from pathlib import Path

from joblib import Memory

# Create memory cache in .cache directory
memory = Memory(location=".cache", verbose=1)


def path_key(path: Path) -> tuple[str, float]:
    """Create a cache key for a Path that includes modification time."""
    if not path.exists():
        return (str(path), 0.0)
    return (str(path), path.stat().st_mtime)


@memory.cache
def create_input_file() -> Path:
    """Create the input file for testing."""
    input_file = Path("ohai.txt")
    input_file.write_text("custom input data")
    print(f"Created {input_file}")
    return input_file


@memory.cache
def x() -> Path:
    """Generate initial data file."""
    path = Path("x.out")
    path.write_text("x data")
    print(f"Generated {path}")
    return path


@memory.cache
def a(x_key: tuple[str, float]) -> Path:
    """Process x data to create a."""
    x_path = Path(x_key[0])
    path = Path("a.out")
    path.write_text(f"a processing {x_path.read_text()}")
    print(f"Generated {path}")
    return path


@memory.cache
def b(x_key: tuple[str, float]) -> Path:
    """Process x data to create b."""
    x_path = Path(x_key[0])
    path = Path("b.out")
    path.write_text(f"b processing {x_path.read_text()}")
    print(f"Generated {path}")
    return path


@memory.cache
def z(a_key: tuple[str, float], b_key: tuple[str, float]) -> Path:
    """Combine a and b to create z."""
    a_path = Path(a_key[0])
    b_path = Path(b_key[0])
    path = Path("z.out")
    path.write_text(f"z combining {a_path.read_text()} and {b_path.read_text()}")
    print(f"Generated {path}")
    return path


def build_z(a_input: Path | None = None) -> Path:
    """Build z with optional override for input a."""
    # Build dependency chain
    if a_input is None:
        x_path = x()
        x_key = path_key(x_path)
        a_path = a(x_key)
    else:
        a_path = a_input

    # Build remaining dependencies
    x_path = x()  # This will be cached if already built
    x_key = path_key(x_path)
    b_path = b(x_key)

    # Build final result
    a_key = path_key(a_path)
    b_key = path_key(b_path)
    return z(a_key, b_key)


def main():
    # Create input file using cached function
    input_file = create_input_file()

    # Build the pipeline
    result = build_z(a_input=input_file)
    print(f"got z: {result}")

    # Show the result
    print(f"Final result: {result.read_text()}")


if __name__ == "__main__":
    raise SystemExit(main())

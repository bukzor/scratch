#!/usr/bin/env python3
"""
Tests for the dependency DAG system.

Regression tests for bugs found during development.
"""
from __future__ import annotations

import contextlib
import json
import time
from pathlib import Path

import mydag as M  # module under test
import pytest


@pytest.fixture
def tmp_path(tmp_path: Path):
    with contextlib.chdir(tmp_path):
        yield tmp_path


class DescribeDependencyCache:
    """Test cache serialization and validation logic."""

    def it_serializes_to_json_correctly(self, tmp_path: Path):
        """Regression: json.dump(self) doesn't work, need dataclasses.asdict()."""

        def dummy_task() -> Path:
            return Path("dummy.out")

        assert dummy_task  # Keep pyright happy

        cache = M.DependencyCache(
            task="dummy_task", deps={"input": "input.txt"}, result="output.txt"
        )

        cache.save()

        # Should create valid JSON file
        cache_file = Path(".dummy_task.deps")
        assert cache_file.exists()
        data = json.loads(cache_file.read_text())
        assert data["task"] == "dummy_task"
        assert data["deps"] == {"input": "input.txt"}

    def it_skips_save_when_task_is_none(self, tmp_path: Path):
        """Test uncovered path: cache with task=None doesn't save."""
        cache = M.DependencyCache(task=None, deps={}, result="")
        cache.save()

        # Should not create any cache files
        cache_files = list(Path(".").glob(".*.deps"))
        assert len(cache_files) == 0

    def it_handles_corrupted_cache_files(self, tmp_path: Path):
        """Regression: JSONDecodeError should be caught and handled gracefully."""

        def dummy_task() -> Path:
            return Path("dummy.out")

        # Create corrupted cache file
        cache_file = Path(".dummy_task.deps")
        cache_file.write_text("invalid json { ## }}}")

        cache = M.DependencyCache.load(dummy_task)

        # Should return empty cache, not crash
        assert cache.task is None
        assert cache.deps == {}
        assert cache.result == ""

    def it_validates_cache_when_output_newer_than_inputs(self, tmp_path: Path):
        """Test that mtime logic actually prevents rebuilds."""

        def dummy_task(input_file: Path) -> Path:
            return Path("output.txt")

        input_file = Path("input.txt")
        output_file = Path("output.txt")

        # Create input first
        input_file.write_text("input data")
        time.sleep(0.01)  # Ensure different timestamps

        # Create output after input (newer)
        output_file.write_text("output data")

        cache = M.DependencyCache(
            task="dummy_task",
            deps={"input_file": str(input_file)},
            result=str(output_file),
        )

        deps = {"input_file": input_file}
        result = cache.up_to_date(dummy_task, deps)

        # Should be valid since output is newer than input
        assert result == output_file

    def it_invalidates_cache_when_input_newer_than_output(self, tmp_path: Path):
        """Test that cache is invalid when input is newer than output."""

        def dummy_task(input_file: Path) -> Path:
            return Path("output.txt")

        input_file = Path("input.txt")
        output_file = Path("output.txt")

        # Create output first
        output_file.write_text("output data")
        time.sleep(0.01)  # Ensure different timestamps

        # Modify input after output (newer)
        input_file.write_text("new input data")

        cache = M.DependencyCache(
            task="dummy_task",
            deps={"input_file": str(input_file)},
            result=str(output_file),
        )

        deps = {"input_file": input_file}
        result = cache.up_to_date(dummy_task, deps)

        # Should be None since input is newer than output
        assert result is None


class DescribeDependencyBuilder:
    """Test build execution and dependency resolution."""

    def it_skips_already_built_tasks(self, tmp_path: Path):
        """Test uncovered path: task already in self.paths returns early."""
        dag = M.DependencyDAG({})

        @dag
        def task() -> Path:
            assert False, "Task should not be called"

        builder = dag.builder()
        expected_path = Path("already_built.txt")
        expected_path.write_text("cached result")
        builder.paths["task"] = expected_path

        # Should return cached path without calling function
        result = builder.build1(task)
        assert result == expected_path

    def it_collects_missing_dependencies_correctly(self, tmp_path: Path):
        """Regression: was appending tasks instead of collecting param names."""
        dag = M.DependencyDAG({})

        @dag
        def source() -> Path:
            return Path("source.txt")

        @dag
        def derived(source: Path) -> Path:
            return Path("derived.txt")

        builder = dag.builder()

        # Try to build derived when source isn't ready
        result = builder.build1(derived)

        # Should enqueue both the current task and its dependency
        assert result is None
        assert len(builder.todo) == 2
        # Should have source task and derived task in todo
        task_names = [t.__name__ for t in builder.todo]
        assert "source" in task_names
        assert "derived" in task_names

    def it_validates_input_paths_exist(self, tmp_path: Path):
        """Regression: should assert that provided input paths exist."""
        dag = M.DependencyDAG({})

        @dag
        def task(input_file: Path) -> Path:
            return Path("output.txt")

        builder = dag.builder()
        nonexistent = Path("does_not_exist.txt")

        # Should raise assertion error for nonexistent input
        with pytest.raises(AssertionError):
            builder.build(task, input_file=nonexistent)

    def it_isolates_builder_instances(self, tmp_path: Path):
        """Regression: builders should not share state."""
        dag = M.DependencyDAG({})

        @dag
        def task() -> Path:
            return Path("output.txt")

        builder1 = dag.builder()
        builder2 = dag.builder()

        # Modify one builder's state
        builder1.paths["test"] = Path("test1.txt")

        # Other builder should be unaffected
        assert "test" not in builder2.paths
        assert builder1.tasks is not builder2.tasks
        assert builder1.todo is not builder2.todo

    def it_uses_cache_to_avoid_rebuild(self, tmp_path: Path):
        """Test that existing cache prevents task execution."""
        dag = M.DependencyDAG({})

        call_count = 0

        @dag
        def source() -> Path:
            nonlocal call_count
            call_count += 1
            path = Path("source.txt")
            path.write_text(f"call #{call_count}")
            return path

        # First call - creates cache
        builder1 = dag.builder()
        result1 = builder1.build(source)
        assert call_count == 1

        # Second call - should use cache
        builder2 = dag.builder()
        result2 = builder2.build(source)
        assert call_count == 1  # Function should not be called again
        assert result1 == result2


class DescribeIntegration:
    """End-to-end functionality tests."""

    def it_builds_simple_dependency_chain(self, tmp_path: Path):
        """Basic functionality: linear dependency chain."""
        dag = M.DependencyDAG({})

        @dag
        def source() -> Path:
            path = Path("source.txt")
            path.write_text("source data")
            return path

        @dag
        def processed(source: Path) -> Path:
            path = Path("processed.txt")
            path.write_text(f"processed: {source.read_text()}")
            return path

        builder = dag.builder()
        result = builder.build(processed)

        assert len(result) == 1
        assert result[0].read_text() == "processed: source data"

    def it_prevents_unnecessary_rebuilds_via_mtime(self, tmp_path: Path):
        """Integration test: mtime checking prevents rebuilds."""
        dag = M.DependencyDAG({})

        source_calls = 0
        processed_calls = 0

        @dag
        def source() -> Path:
            nonlocal source_calls
            source_calls += 1
            path = Path("source.txt")
            path.write_text(f"source data v{source_calls}")
            return path

        @dag
        def processed(source: Path) -> Path:
            nonlocal processed_calls
            processed_calls += 1
            path = Path("processed.txt")
            path.write_text(f"processed: {source.read_text()} v{processed_calls}")
            return path

        # First build
        builder1 = dag.builder()
        result1 = builder1.build(processed)
        assert source_calls == 1
        assert processed_calls == 1

        time.sleep(0.01)  # Ensure timestamps differ

        # Second build - should use cache for both
        builder2 = dag.builder()
        result2 = builder2.build(processed)
        assert source_calls == 1  # Should not rebuild source
        assert processed_calls == 1  # Should not rebuild processed
        assert result1 == result2

    def it_rebuilds_when_dependency_changes(self, tmp_path: Path):
        """Integration test: changing dependency triggers rebuild."""
        dag = M.DependencyDAG({})

        processed_calls = 0

        @dag
        def processed(source: Path) -> Path:
            nonlocal processed_calls
            processed_calls += 1
            path = Path("processed.txt")
            path.write_text(f"processed: {source.read_text()} v{processed_calls}")
            return path

        # Create initial source file
        source_file = Path("source.txt")
        source_file.write_text("initial data")

        # First build
        builder1 = dag.builder()
        result1 = builder1.build(processed, source=source_file)
        assert processed_calls == 1

        time.sleep(0.01)  # Ensure timestamps differ

        # Modify source file (making it newer)
        source_file.write_text("modified data")

        # Second build - should rebuild processed since source changed
        builder2 = dag.builder()
        result2 = builder2.build(processed, source=source_file)
        assert processed_calls == 2  # Should rebuild processed
        assert "modified data" in result2[0].read_text()

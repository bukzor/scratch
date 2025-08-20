I believe the core issue here is union ambiguity; when `R` itself can be a
generator type, the union `R | Generator[R]` creates genuine ambiguity:

```python
# If R = Generator[int], then R | Generator[R] becomes:
result: Generator[int] | Generator[Generator[int]]

# After isinstance(result, Generator), both cases match:
if isinstance(result, Generator):  # True for both cases!
    # Is this Generator[int] or Generator[Generator[int]]?
```

This explains the `Generator[Unknown]` types pyright reports - it correctly
identifies that the yield type cannot be determined from the isinstance check
alone.

## Type System Constraints That Block Clean Solutions

1. **No parameterized constraints**: Cannot write
   `F: Callable[P, R | Generator[R]]` where `P, R` are type variables
2. **No overload dispatch with bodies**: `@overload` only allows stubs, not
   implementations
3. **Union narrowing limitations**: `isinstance(result, Generator)` doesn't
   narrow generic parameters

## Workaround Solution: Separate Functions

The type-safe approach requires splitting the decorator:

```python
def transformed_value[R, **P](transformer: Callable[[R], R]) -> Callable[
  [Callable[P, R]],
  Callable[P, R]
]: ...
def transformed_generator[R, **P](transformer: Callable[[R], R]) -> Callable[
  [Callable[P, Generator[R]]],
  Callable[P, Generator[R]]
]: ...
```

This eliminates all casts and runtime type ambiguity, at the cost of requiring
users to choose explicitly.

## Sufficient Typing Extensions

The pattern would be naturally expressible with either:

1. Overloaded dispatch with function bodies
2. A better way to type-narrow a union of generics

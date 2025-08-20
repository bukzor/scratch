# Generator Decorator Type Safety Investigation

## Problem Statement
Attempted to create a decorator that transforms both single values and generators uniformly:
- Functions returning `R` → apply transformer to result
- Functions returning `Generator[R]` → apply transformer to each yielded value
- Goal: Single decorator that "doesn't care" whether function returns value or generator

## Key Findings

### Type System Limitations Discovered

1. **No parameterized type constraints**: Python doesn't allow `F: Callable[P, R]` where `P` and `R` are type variables
   - Exception: `Callable[..., object]` is somehow special-cased
   - This forces use of unconstrained generics + runtime casts

2. **Generic constraint syntax limitation**: `F: Callable[P, R | Generator[R]]` fails with "TypeVar constraint type cannot be generic"

3. **Union type narrowing issues**: After `isinstance(result, Generator)`, type system sees `Generator[Unknown] | Generator[R]` rather than definitively `Generator[R]`

### The Core Type Safety Problem

When `R` itself can be a generator type (e.g., `R = Generator[int]`), the union `R | Generator[R]` becomes ambiguous:
- `R` case: `Generator[int]` 
- `Generator[R]` case: `Generator[Generator[int]]`

After `isinstance(result, Generator)`, both cases pass the runtime check, but we can't determine which case we're in without deeper introspection.

### Cast Analysis Through Iterations

**Original approach (.4.py)**: 4 casts + TypeGuards
**Revision 5**: 3 casts (eliminated TypeGuards, used `isinstance + else` for total union narrowing)  
**Revision 6**: 3 casts (cleaner architecture with separate `__transformed` function)

**Cast validity assessment**:
1. `f_ = cast(Callable[P, R | Generator[R]], f)` - **Valid with proper bound** (`F: Callable[..., object]`)
2. `return cast(F, decorated)` - **Valid as inverse of cast #1**
3. `result = cast(Generator[R], result)` - **Questionable**: Asserts which branch of union without proof

Cast #3 represents the fundamental type unsoundness - we can't definitively know if a generator yields `R` values.

## Solutions Explored

### Runtime Type Checking
Considered `generator_of_r(gen, r_type)` to validate yield types:
- **Challenge**: No way to extract runtime type from `R` type variable
- **Alternative**: Peek at first yielded value to infer type
- **Issue**: Still need `cast(R, first_value)` - doesn't eliminate casts entirely

### Overloaded Dispatch (Theoretical)
**Missing language features that would solve this cleanly**:
1. `@overload` with function bodies (not just type stubs)
2. Type parameters in constraints: `F: Callable[P, R]`
3. Proper scoping for type parameter references

With these, could define separate overloads for `R` and `Generator[R]` cases.

## Final Solution: Separate Functions

**Revision 7**: Split into `transformed_value` and `transformed_generator`
- ✅ **Zero casts** - completely type-safe
- ✅ **No runtime ambiguity** - each function knows its exact case
- ✅ **Clean type signatures** - no complex generic constraints needed

**Trade-offs**:
- **API change**: Users must explicitly choose value vs generator decorator
- **Type "mangling"**: Decorated functions become generic `Callable[P, R]` rather than preserving original type `F`

## Key Decisions Made

1. **Cast assessment**: Casts #1 and #2 are valid workarounds for type system limitations; cast #3 represents genuine type unsoundness

2. **Architecture choice**: Separate functions over unified decorator for type safety

3. **Type preservation vs safety**: Chose safety (no casts) over preserving exact function type `F`

## Broader Implications

**The original concept isn't inherently type-unsafe** - languages with more sophisticated type systems (overloaded dispatch, better constraint systems) could handle this pattern cleanly.

**Python's current limitations**:
- Insufficient constraint expressiveness  
- No parameterized constraints
- Limited overload dispatch capabilities

**The "magic" single decorator remains fundamentally problematic** in current Python due to the `R | Generator[R]` ambiguity when `R` itself can be a generator type.
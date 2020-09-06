
### Pretty

```!formality
cat.print(text: String): IO(Unit)
  use skip = IO.ask<Unit>("print", text)
  IO.end<Unit>(Unit.new)
```

### Desugared

```!formality
cat.print2(text: String): IO(Unit)
  IO.ask<Unit>("print", text,
    (skip) IO.end<Unit>(Unit.new)
  )
```

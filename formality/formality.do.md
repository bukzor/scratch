"`do`" Notation
===============

The do-notation for a Monad `M` is desugared as:

  1.  The syntax: `var x = y; z`

      Becomes: `Monad.bind<M>(M.monad)<_,_>(y, (x) z)`

  2.  The syntax: `y; z`

      Becomes: `Monad.bind<M>(M.monad)<_,_>(y, () z)`

  3.  And the syntax: `return x;`

      Becomes: `Monad.pure<M>(M.monad)<>(x)`


So the next two programs are exactly equivalent.

### Using do-notation

```
cat: IO(Unit)
  do IO {
    var line = IO.get_line;
    IO.print(line);
    cat;
  }
```

### Desugared

```
cat: IO(Unit)
  Monad.bind<IO>(IO.monad)<_,_>(
    IO.get_line,
    (line) Monad.bind<IO>(IO.monad)<_,_>(
      IO.print(line),
      () cat,
    )
  )
```

### Even more Desugared

```
cat_(_: Unit): IO(Unit)
  IO.ask<>("get_line", "",
    (line) IO.ask<>("print", line,
      () cat_()
    )
  )

cat: IO(Unit)
  cat_()
```

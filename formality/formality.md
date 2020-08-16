Type definition
---------------

```
T Color.
| Red.;
| Blue.;
```

Desugars to:

```
Red_: Color_
  <P>(Red, Blue) Red

Blue_: Color_
  <P>(Red, Blue) Blue

Color_: Type
  self<P: Color_ -> Type>
    -> P(Red_)
    -> P(Blue_)
    -> P(self)
```

Case statement
--------------

```
ColorName.(c: Color.): String
  case c:
  | Red. => "red";
  | Blue. => "blue";
  : String;
```

desugars to

```
ColorName_(c: Color_): String
  c<(c.self) String>("red", "blue")
```


Conclusion
----------
A type definition of N constructors compiles to a function of N+1 arguments, where the first argument maps the input type of a case statement to the output type of that case statement. The final, optional claus of a case statement, what looks like a type annotation is in fact the first argument to the type function, and this explains why c.self is a variable available only to that final "type annotation" case clause. (It probably explains the semantic difference between `c` and `c.self`, but I haven't dug that deep yet).

So a Type is a function of N+1 arguments which defines the case statement. The final N arguments denote the result if the case value is one of N constructors. The first argument is a simple lambda that returns the resultant type (the "motive") of the case expression. The motive lambda (named "P") has the case value available to it, namd as the input variable name but with .self appended to the name. (In the above example, "c" maps to "c.self".)

Secondarily, the P lambda is used to allow the type function to take the case results as arguments, by mapping from the type's constructors to the results' type.
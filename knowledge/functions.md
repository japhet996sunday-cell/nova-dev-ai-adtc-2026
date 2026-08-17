# Functions

A function packages a sequence of steps under a name so it can be reused
without repeating the code. Good functions share a few properties:

- **Do one thing.** If a function's name needs "and" to describe it
  (`validateAndSave`), it's often doing two jobs that should be two
  functions.
- **Take inputs as parameters, not as assumed global state.** A function
  that reads a variable defined outside itself is harder to test and reuse
  than one that receives everything it needs as arguments.
- **Return a value rather than printing it**, unless printing is literally
  the function's job. A function that prints instead of returning can't have
  its result used by other code.
- **Keep the parameter list short.** More than three or four parameters is
  usually a sign the function needs to accept a single structured object
  instead (a dict, a struct, an object).

**Pure functions** — ones whose output depends only on their inputs, with no
side effects (no modifying external state, no I/O) — are easiest to reason
about and test, because calling them twice with the same input always gives
the same result.

**Recursion** (a function calling itself) is a natural fit for problems that
break down into smaller versions of themselves (tree traversal, factorial,
searching nested data) but every recursive function needs a clear base case
that stops the recursion, or it will run until the call stack overflows.

A common debugging technique specific to functions: if a function returns
the wrong value, check whether every code path actually has a `return`
statement. A missing `return` on one branch of an `if/else` is a frequent
silent bug — the function falls through and returns `None`
instead of the intended value.

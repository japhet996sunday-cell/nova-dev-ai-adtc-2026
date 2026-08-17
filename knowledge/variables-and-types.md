# Variables and Data Types

A variable is a name bound to a value in memory. The value can change; the
binding is what makes the name useful.

Common primitive types across most languages:

- **Integer** — whole numbers, no decimal point (`7`, `-3`, `0`).
- **Float / double** — numbers with a decimal point (`3.14`, `0.5`). Floats
  cannot represent every decimal value exactly, which is why comparing two
  floats with `==` is often unreliable — compare with a small tolerance
  instead (e.g. `abs(a - b) < 0.0001`).
- **String** — text, always quoted (`"hello"`, `'hello'`). Strings are
  usually immutable: operations that "change" a string actually create a
  new one.
- **Boolean** — `true`/`false` (or `True`/`False` in Python). Used for
  conditions and flags.
- **Null / None / nil** — represents "no value." A frequent source of bugs
  is calling a method on something that turned out to be null instead of
  the object you expected.

**Dynamically typed languages** (Python, JavaScript) let a variable hold
different types at different times and check types at runtime. This is
flexible but means a type mismatch often only surfaces when that code
actually runs, not before.

**Statically typed languages** (Java, C, TypeScript) require a variable's
type to be declared or inferred once, and the compiler checks it before the
program runs — catching a class of bugs earlier, at the cost of more
upfront ceremony.

A frequent beginner mistake: assuming a value read from user input, a file,
or a network response is already the type you need. Input is text until you
explicitly convert it (e.g. `int(user_input)` in Python, `Number(input)` in
JavaScript) — and that conversion can fail, so it should be checked.

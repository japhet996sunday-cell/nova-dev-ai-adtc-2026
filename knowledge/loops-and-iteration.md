# Loops and Iteration

Loops repeat a block of code. The two most common shapes:

- **`for` loop** — repeats a known or bounded number of times, usually
  iterating over a sequence (array, list, range). Preferred when you know
  what you're iterating over.
- **`while` loop** — repeats until a condition becomes false. Preferred when
  the number of repetitions isn't known ahead of time (e.g. "keep reading
  input until the user types 'quit'").

**Off-by-one errors** are the most common loop bug: looping `0` to `n`
inclusive when you meant exclusive (or vice versa), causing the loop to run
one time too many or too few. When indexing an array of length `n`, valid
indices are `0` through `n-1` — using `<=` instead of `<` in the loop
condition is a classic way to read past the end of the array.

**Infinite loops** happen when the condition that should eventually become
false never does — usually because the loop body forgot to update the
variable the condition depends on (e.g. forgetting `i++` in a `while`
loop), or because the update happens on a copy of the variable rather than
the original.

**Nested loops** (a loop inside a loop) multiply their iteration counts —
two nested loops each running `n` times do `n²` total iterations. This
matters for performance: an algorithm with nested loops over a large
collection can become noticeably slow well before it becomes technically
"wrong," which is a separate kind of bug (a correctness bug vs. a
performance bug) worth diagnosing differently.

Prefer breaking out of a loop early (`break`) over adding a complex boolean
flag that the loop condition checks every iteration — it's usually more
readable and just as correct.

**Indexing example:** A Python list of length `n` has valid indices `0` through `n-1`. Accessing an invalid index raises `IndexError`. For example, `items = ["a", "b", "c"]` has valid indices `0`, `1`, and `2`; `items[3]` raises `IndexError`.

# Debugging Strategy

When code doesn't work, resist the urge to guess-and-check randomly. Follow a
sequence:

1. **Reproduce it reliably.** If you can't make the bug happen on demand, you
   can't confirm you've fixed it. Find the smallest input that triggers it.
2. **Read the actual error, not what you assume it says.** Python and
   JavaScript tracebacks name the exact line and exception type. The last
   line of a traceback is usually the most useful one.
3. **Bisect the problem.** Comment out or isolate half the code. Does the bug
   survive? That tells you which half it's in. Repeat until you've narrowed
   it to a few lines.
4. **Print the state, don't guess it.** Before the line that misbehaves,
   print the variables it depends on. Most bugs are a variable holding a
   different value than the programmer assumed.
5. **Check off-by-one errors first** in loops and array indexing — they are
   the single most common beginner bug across every language.
6. **Check your assumptions about types.** A function returning a string
   `"5"` instead of the number `5` causes bugs that look unrelated to types
   at first glance.

A bug fix that you don't understand is not a fix — it's a coincidence. If
changing a line makes the symptom go away but you can't explain why, keep
investigating before moving on.

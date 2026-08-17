# Working Effectively With Intermittent Connectivity

Many developers learn and build in environments where internet access is
unreliable, metered, or expensive. Some practices that reduce how much that
friction costs you:

- **Keep local copies of documentation you use often.** Language references,
  standard library docs, and framework guides are usually available as
  offline downloads (e.g. `devdocs.io` has an offline mode; Python ships
  `pydoc` locally; MDN web docs can be downloaded for offline use).
- **Commit early, commit often, and always locally first.** Git itself is
  fully offline — commits, branches, diffs, and history all work without a
  network. You only need connectivity to `push`/`pull`/`fetch` to a remote.
  Treat "no internet" as "no sync today," not "no version control today."
- **Cache dependencies once, reuse them.** Package managers (`pip`, `npm`)
  can install from a local cache after the first download — avoid
  re-downloading the same packages across projects when a shared cache or
  vendored `node_modules`/`venv` will do.
- **Test locally before assuming a deploy will work.** Running a local dev
  server and a local database instance catches most bugs without needing a
  round trip to a hosted environment.
- **Batch your connectivity-dependent tasks.** Group everything that needs
  the network — searching for an error message, checking a library's
  changelog, pushing commits — into one online session rather than
  context-switching in and out of a spotty connection.
- **Prefer tools that run locally over tools that require a constant cloud
  connection.** A local linter, a local test runner, and a local AI coding
  assistant all keep your feedback loop fast and working regardless of
  connectivity — which is the same engineering principle behind why this
  assistant itself is designed to run fully offline after its one-time
  model download.

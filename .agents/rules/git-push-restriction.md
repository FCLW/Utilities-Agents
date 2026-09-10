---
trigger: always_on
description: Prohibit pushing to remote repository unless explicitly requested by the user.
---

# Remote Repository Push Restriction

- Antigravity must NOT push code, branches, or tags to any remote repository (e.g., `git push`, `git push origin ...`) unless the user has explicitly and specifically requested to push in their prompt.
- Local git actions (e.g., `git commit`, `git checkout`, `git branch`, `git status`, `git diff`) are permitted.

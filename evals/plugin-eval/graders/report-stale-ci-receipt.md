---
type: regex
target: last_message
flags: i
pattern: '\b(CI|receipt|last-run)\b[^\n]{0,140}\b(older|earlier|previous|prior|stale|predates?|not (the )?(current|HEAD|latest)|different commit|does(n.t| not) (match|cover)|behind)\b|\b(older|earlier|previous|prior|stale|predates?|not (the )?(current|HEAD|latest)|different commit|does(n.t| not) (match|cover)|behind)\b[^\n]{0,140}\b(CI|receipt|last-run)\b'
---

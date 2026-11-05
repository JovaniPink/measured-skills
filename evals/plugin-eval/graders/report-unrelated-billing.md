---
type: regex
target: last_message
flags: im
pattern: '\b(billing|rounding|round_cents)\b[^\n]{0,160}\b(unrelated|out of scope|outside (the )?(retry )?scope|not part|not retry-related|separate|scope creep|does(n.t| not) belong|mixed|bundled|nothing to do with|not related)|\b(unrelated|out of scope|outside (the )?(retry )?scope|not part|not retry-related|separate|scope creep|does(n.t| not) belong|mixed|bundled|nothing to do with|not related)\b[^\n]{0,160}\b(billing|rounding|round_cents)\b|^[#* ]*unrelated[^\n]*\n(\s*\n)?([^\n]+\n){0,3}[^\n]*\b(billing|rounding|round_cents)\b'
---

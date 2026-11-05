---
type: regex
target: last_message
flags: im
pattern: '^(?=[^\n]*\bRetry-After\b)(?=[^\n]*\b(dropped|drops|removed|removes|omitted|omits|missing|no longer|disappear(s|ed)?|lost|left out|not (in|carried|included|listed|mentioned|present)|absent|silently|still (required|accepted|binding|applies|in force)|not (been )?withdrawn)\b)(?=[^\n]*(retry-v[12]|\bv[12]\b|\bplans?\b|0003|\bdecision\b))'
---

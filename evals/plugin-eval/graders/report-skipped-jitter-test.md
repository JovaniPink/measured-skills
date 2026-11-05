---
type: regex
target: last_message
flags: im
pattern: '^(?=[^\n]*(test_delays_include_jitter|\bjitter[- ]test|\btests?\b[^\n]{0,40}\bjitter\b))(?=[^\n]*(\bskip(ped|s)?\b|pytest\.mark\.skip|\bxfail(ed)?\b|\bdisabled\b))'
---

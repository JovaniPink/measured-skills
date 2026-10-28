# Distinguish retention, allocation, and UI stalls

Authority: [Gathering information about memory use](https://developer.apple.com/documentation/xcode/gathering-information-about-memory-use.md).
Apple's Markdown documentation was inspected on 2026-10-28. These are documented
techniques, not new Instruments, MetricKit, simulator, or device observations.

1. Record app revision, Xcode/OS, device or simulator, build configuration, interaction,
   data volume, and available capture. Distinguish a memory graph, Allocations trace,
   crash/termination report, and sampled CPU trace; they support different claims.
2. Repeat one bounded interaction with a stable baseline when execution is authorized.
   Compare generations and object lifetimes after dismissal or cancellation. A peak
   during image decoding is not automatically a leak; persistent growth is a lead.
3. Inspect retained objects and reference edges. Identify the intended owner, closure
   captures, tasks, subscriptions, delegates, and caches before recommending weak
   references. A graph cycle alone does not prove unintended retention.
4. Use allocation stacks when available to locate creation; enable capture settings
   only within authorized local diagnostics. Captures can contain private data and
   change performance. Do not upload them as part of a generic verification rule.
5. Separate memory retention from main-thread blocking and excessive SwiftUI updates.
   Correlate the interaction with suitable time/SwiftUI traces; memory size alone
   cannot diagnose a hang. Recheck cancellation and identity after any proposed fix.
6. Report the observed lifetime, competing causes, smallest discriminating check,
   and missing evidence. A green simulator memory gauge is not a device memory-limit
   result. Supplied MetricKit diagnostics do not establish a reproduced local cause.

Synthetic fixture, not a trace: after three open/dismiss cycles, three view models
remain referenced by an owner array. Inspect whether retaining history is intended.
If ownership should end at dismissal, propose releasing that reference and compare
again. Do not declare a verified leak repair until the relevant observation exists.

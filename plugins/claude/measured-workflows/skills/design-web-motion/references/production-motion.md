# Production motion

Keep semantic content complete before JavaScript. Separate product state from
animation state: interrupted or skipped animation must not lose a save or selection.
Keep controls keyboard and touch operable, with visible labels in accessible names.
A stable pressed toggle differs from a changing Play/Pause action label.

Start static when the motion preference is unknown. Reduced motion removes
nonessential travel; it does not remove essential information. Pause ongoing motion
when hidden or offscreen, keep the focused control mounted, and require explicit
restart. These are catalog design choices; assess applicable WCAG criteria separately.

Specify interruption, replay, error, narrow-layout and enlarged-text behavior.
Prefer existing CSS or framework tools. Measure relevant browser behavior; mocked
visibility events do not prove pixels stopped. Timings are project choices, not
universal thresholds. Retain untested devices and assistive technologies as gaps.

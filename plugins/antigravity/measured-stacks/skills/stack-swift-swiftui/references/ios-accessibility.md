# iOS accessibility in SwiftUI

Evidence labels: [verified] means the API compiled against the iOS 27.0 simulator SDK in Xcode 27.0 on 2026-09-22. That proves the API exists, not that the result is accessible. [documented] means stated in the linked Apple guidance. [unverified] means review judgment.

Authorities: [Human Interface Guidelines: Accessibility](https://developer.apple.com/design/human-interface-guidelines/accessibility) and the SwiftUI accessibility API in the installed SDK. For WCAG findings or conformance language, also use the `review-accessibility` skill.

## Dynamic Type

- Scale icons, spacing, and other non-text sizes with `@ScaledMetric(relativeTo:)`. [verified]
- Switch from a row to a column when `dynamicTypeSize.isAccessibilitySize` is true, for example with `AnyLayout`. [verified]
- Capping text with `.dynamicTypeSize(...DynamicTypeSize.accessibility3)` needs a stated reason. It limits what some people can read. [verified API; judgment]
- Bar items and other controls that cannot grow with Dynamic Type can use `.accessibilityShowsLargeContentViewer()` so a long press shows an enlarged version. [verified API; judgment]

## VoiceOver on custom controls

- For a custom drawing that acts as one control, use `.accessibilityElement(children: .ignore)` and then:
  - `accessibilityLabel` for what it is, for example "Daily goal". [verified]
  - `accessibilityValue` for its current state, for example "40 percent". [verified]
  - `accessibilityAdjustableAction` when people can raise or lower it. [verified]
- `accessibilityRepresentation` lets a custom view borrow a standard control's behavior. [verified]
- Hide decorative images with `.accessibilityHidden(true)`. [verified]
- Add `accessibilityInputLabels` when the visible label is long or unclear for Voice Control. [verified]

## Reduce Motion

- Read `@Environment(\.accessibilityReduceMotion)`. [verified]
- When it is on, cut back automatic and repeating animation, zooms, and parallax. Replace big movement with a fade or with no animation. [documented]
- Pattern: `.animation(reduceMotion ? nil : .default, value: state)`. [verified compiles]

## Differentiate Without Color

- Never use color alone to show status, errors, or chart series. Add a symbol, shape, pattern, or text. [documented]
- Read `@Environment(\.accessibilityDifferentiateWithoutColor)` to add those cues when the setting is on. [verified]

## Touch targets

- HIG lists 44x44 pt as the default iOS control size and 28x28 pt as the minimum. [documented]
- Aim for 44x44 pt on primary controls. Expand small glyphs with `.frame(minWidth: 44, minHeight: 44)` and `.contentShape(.rect)` so the whole area responds. [verified compiles]
- Leave space between adjacent targets. [documented]

## Evidence to ask for

- An XCUIAutomation `performAccessibilityAudit` run in a UI test. In Xcode 27 the API lives in the XCUIAutomation framework, iOS 17 or later. [verified declaration]
- A manual VoiceOver pass on a device for custom controls. An audit does not check whether labels make sense. [unverified]
- Screens checked at the largest accessibility text size and with Reduce Motion and Differentiate Without Color turned on.
- Report which of these ran. Do not claim a screen is accessible from a compile or static review.

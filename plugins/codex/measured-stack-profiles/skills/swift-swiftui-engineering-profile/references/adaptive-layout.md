# Preserve a journey through resizing

Authorities: [Migrating full-screen compatibility](https://developer.apple.com/documentation/technotes/tn3192-migrating-your-app-from-the-deprecated-uirequiresfullscreen-key) and [ViewThatFits](https://developer.apple.com/documentation/swiftui/viewthatfits). Reviewed 2026-10-12.

- Read available container space and relevant size classes rather than equating device idiom with layout. Optional size classes require explicit handling; `== .regular` does not mistake nil for regular. [documented]
- Keep draft, navigation path, and selected record ownership above a layout switch if the user must continue the same task after resizing. Test keyboard and focused-field behavior too. [unverified: runtime]
- Short and wide windows need reachable primary and secondary actions. Test scrolling fallbacks and ViewThatFits with long localized text and accessibility sizes; do not assume fitting once proves the whole journey. [documented]
- safeAreaBar and backgroundExtensionEffect declare iOS 26 availability in the installed SDK. The safeAreaBar/fallback probe compiles at an iOS 17.6 target. Preserve a tested fallback for older systems. [verified: SDK inspection and compile]
- Respect safe areas; do not move tappable content beneath system bars just because background imagery extends there. Verify custom shape geometry and ConcentricRectangle availability separately. [unverified: runtime]
- UIRequiresFullScreen has version-dependent compatibility behavior. Apple describes discrete resizing under the iOS 27 SDK; the ignored-starting-version key is a separate migration control. Inspect the built plist and test actual supported configurations. [documented]
- Test native iPad support separately from iPhone compatibility behavior. Test two independent windows only when the app actually supports multiple scenes. [unverified: project evidence]

## A useful constrained-layout test

Begin with a partially edited value and an open keyboard. Narrow the container,
change text size, and then return to the original dimensions. Verify the draft,
selected record, focus behavior, scroll position where promised, and reachable
Save/Cancel actions. A screenshot of an empty screen does not cover this contract.
[unverified: journey acceptance]

Use ViewThatFits for a finite set of meaningful alternatives, not as a substitute
for scrolling arbitrary content. Give long forms a scrollable path to every
control. Do not calculate fixed widths from the device screen; a navigation
column can be much narrower than that screen. [documented; project layout tests
remain required]

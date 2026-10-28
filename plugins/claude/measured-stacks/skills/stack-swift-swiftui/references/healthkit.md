# HealthKit authorization and privacy

Evidence labels: [verified] means compiled against, or read from, the iOS 27.0 SDK in Xcode 27.0 on 2026-09-22. No HealthKit call ran on a device. [documented] means stated in the linked Apple documentation. [unverified] means review judgment.

Authorities: [Setting up HealthKit](https://developer.apple.com/documentation/healthkit/setting-up-healthkit), [Authorizing access to health data](https://developer.apple.com/documentation/healthkit/authorizing-access-to-health-data), [Protecting user privacy](https://developer.apple.com/documentation/healthkit/protecting-user-privacy), and the HealthKit headers in the installed SDK.

## Setup checks

- The target has the HealthKit capability. [documented]
- `NSHealthShareUsageDescription` (read) and `NSHealthUpdateUsageDescription` (write) are set. A missing key crashes the app when it requests access. [documented]
- Xcode adds `healthkit` to required device capabilities. Remove it when HealthKit is optional, or the App Store hides the app from devices without it. [documented]
- Call `HKHealthStore.isHealthDataAvailable()` before any other HealthKit call. It returns false on macOS and on iPad before iPadOS 17. [documented] An unsigned command-line tool without the HealthKit entitlement also got false on macOS 27.0. [verified for that case only]
- Create one long-lived `HKHealthStore`. [documented]

## Ask just in time

- Request only the types a feature needs, when a person starts that feature. Asking for everything at launch is a finding. [documented; judgment]
- `statusForAuthorizationRequest(toShare:read:)` tells whether a sheet would appear. Use it to decide whether to show an explanation first. [verified compiles]
- In SwiftUI, `.healthDataAccessRequest(store:shareTypes:readTypes:trigger:completion:)` needs both SwiftUI and HealthKitUI imported. [verified]
- A `true` result from `requestAuthorization` means the request finished. It does not mean access was granted. [documented]
- Once a person has answered for a type, asking again shows no sheet. Point people to Settings instead of prompting in a loop. [documented]

## Read access is private by design

- An app cannot learn whether read access was denied. Denied reads look like "no data," except for samples the app saved itself. [documented]
- `authorizationStatus(for:)` reports write (share) status only. Using it to decide read access is a bug. [documented]
- Design one empty state that covers both "no data yet" and "access not granted." Suggest checking Health access in Settings, without claiming which case applies. [unverified]
- Never show a "you denied access" message for reads. [documented; judgment]

## Limited history (iOS 27)

- People can grant access to recent data only. Limited and denied read access look the same to the app. [documented]
- `earliestAuthorizedSampleDate(for:)` is iOS 27 or later and returns the earliest readable date for each limited type. [verified in SDK interface]
- Clamp query start dates to that date, and gate the call with `#available`. [unverified]

## Denied write access

- `.sharingDenied` from `authorizationStatus(for:)` is reliable for writes. Explain what will not be saved and keep unrelated features working. [documented; judgment]

## Background and policy

- Background delivery needs the `com.apple.developer.healthkit.background-delivery` entitlement on iOS 15 or later. Without it, `enableBackgroundDelivery` fails with an authorization-denied error. Delivery frequency has per-type limits; for example, step count is at most hourly on iOS. [documented]
- The Health store is encrypted while the device is locked. Background reads can fail even though writes are cached. [documented]
- Apple restricts using HealthKit data for ads, selling it, or sharing it with third parties, and requires a privacy policy. Flag possible conflicts for the owner to decide. This skill does not give legal advice. [documented]

## Testing

- UI tests can reset Health authorization with `resetAuthorizationStatus(for: .health)` in XCUIAutomation. [verified declaration]
- Report simulator results separately from device results. Device behavior was not tested here.

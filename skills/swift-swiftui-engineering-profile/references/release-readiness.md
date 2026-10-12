# Separate build evidence from release acceptance

Authorities: [Launch screens](https://developer.apple.com/documentation/technotes/tn3208-preparing-your-apps-launch-screen-to-meet-app-store-requirements), [SDK requirement](https://developer.apple.com/news/?id=k1mtkt1k), and [screenshot specifications](https://developer.apple.com/help/app-store-connect/reference/app-information/screenshot-specifications). Reviewed 2026-10-12; refresh dated requirements before submission.

- For uploads built with the iOS 27 SDK or later, Apple requires launch metadata using one of UILaunchStoryboardName, UILaunchStoryboards, UILaunchScreen, or UILaunchScreens. Inspect the built product, not just a project setting. [documented]
- Generated UILaunchScreen can be an empty dictionary. Do not reject a present supported key merely because its value is falsey. Check that the product was built with the intended configuration. [documented]
- Apple announces SDK 27 or later for iOS/iPadOS submissions beginning April 2027. This is not a minimum deployment-target requirement. [documented]
- Duo screenshot announcement wording and the detailed specification currently differ in scope. Record both, prepare applicable assets, and recheck the provider's requirements before submission. [documented]
- Keep source configuration, built plist, signed archive, provider validation, App Review acceptance, and public release as distinct states. No local compile can prove an upload was accepted. [unverified: require stage-specific receipts]
- Review privacy declarations, content and model rights, support, data persistence/recovery, accessibility, and every promised paid capability before charging. Prototype paywalls must disclose that they do not purchase or restore anything. [unverified: product acceptance]
- Purchase qualification includes cancellation, pending and failed transactions, restore, renewal, expiry, refunds/revocation, offline behavior, reinstall, and entitlement recovery. Do not collect subscriptions for unavailable functionality. [unverified: product acceptance]

# Folding-display qualification

Authorities: [Preparing for iPhone Duo](https://developer.apple.com/news/?id=kkphp5qo) and [adaptive interfaces](https://developer.apple.com/videos/play/tech-talks/111463/). Reviewed 2026-10-12.

Apple documents new adaptive layouts and a recompile with Xcode 27.1 for Duo support. The installed Xcode 27.0 toolchain cannot qualify APIs absent from its SDK. [documented; local SDK limit verified]

Keep reservedRegions, ArrangementView, vertical toolbar behavior, axis preferences, and onHingeChange in a separate qualification lane until their exact declarations compile against the selected SDK. Use availability at the declared runtime floor and retain older-system fallbacks. [unverified: newer toolchain required]

Test outer-to-inner and inner-to-outer transitions while editing, navigating, presenting a sheet, using the keyboard, and reading a long list. Verify that drafts, focus, selection, and navigation survive as intended. Camera/fold reserved areas must not obscure actions or meaningful content. [unverified: simulator and device]

Record Device Hub poses and simulator steps actually executed. A screenshot of one pose is not proof of folding behavior. Physical hinge behavior, accessibility, and device performance require their own evidence. [unverified: device]

Keep Xcode 27.2 preview findings provisional. In particular, the installed 27.0 compiler rejects toolbar hidden for iOS; do not add it to the supported path based on a later-version report. [verified: negative compile]

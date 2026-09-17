# iOS and Android delivery

Check the linked official pages at export time; store and platform requirements can change. This skill targets iOS/iPadOS, Android launcher icons, and the Google Play listing. Other Apple or Android form factors need their own checks.

| Destination | Deliverable | Placement and visual rule |
| --- | --- | --- |
| Apple App Store and iOS/iPadOS AppIcon | 1024×1024 px opaque square PNG | Supply to Xcode's AppIcon single-size slot. Xcode can derive smaller sizes. Keep corners unmasked; Apple applies the mask. Explicit dark, tinted, or layered variants depend on the project's icon setup. |
| Google Play listing | 512×512 px, sRGB 32-bit PNG with alpha, at most 1024 KB | This is separate from the installed launcher icon. Google Play applies corner rounding and shadow, so do not bake them into the upload. |
| Android adaptive launcher | Distinct foreground and background layers, each 108×108 dp at every supported density | Keep essential foreground content in the centered 66×66 dp safe area. `res/mipmap-anydpi-v26/ic_launcher.xml` references the layers. A monochrome layer supports themed icons where applicable. |
| Android legacy launcher | Square density PNGs for pre-API-26 devices; round PNGs when the app uses `roundIcon` | Use `res/mipmap-{mdpi,hdpi,xhdpi,xxhdpi,xxxhdpi}/`. For a 48 dp legacy icon, those files are 48, 72, 96, 144, and 192 px respectively. Preview both shapes. |
| Marketing | 1080×1080 px PNG | Make a separate rounded-corner presentation with a visible border. Never substitute it for Apple, Google Play, or Android launcher artwork. |

Official sources: [Apple asset catalog](https://developer.apple.com/documentation/xcode/configuring-your-app-icon), [Apple app icon design](https://developer.apple.com/design/human-interface-guidelines/app-icons), [Google Play listing icon](https://support.google.com/googleplay/android-developer/answer/9866151), [Google Play icon treatment](https://developer.android.com/distribute/google-play/resources/icon-design-specifications), [Android adaptive icon](https://developer.android.com/develop/ui/compose/system/icon_design_adaptive), and [Android Studio launcher assets](https://developer.android.com/studio/write/create-app-icons).

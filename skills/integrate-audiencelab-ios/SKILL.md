---
name: integrate-audiencelab-ios
description: Install, audit, or repair the Audiencelab native iOS SDK according to its official integration guidelines. Cover app-launch initialization, purchases through direct SDK reporting or RevenueCat, ads when present, and optional custom events and user properties.
---

# Integrate Audiencelab on iOS

Use this skill for Audiencelab native iOS SDK installation, integration review, or missing-event wiring. Inspect the app and follow the official guidelines for its selected release. Support both local installation/repair and audit-only guidance; an explicit audit-only request means no edits.

Completion means the relevant source and configuration follow the SDK guidelines, with concrete changes or instructions and any remaining configuration gaps identified. Builds, simulator runs, test transactions, live ad interaction, token validation, and backend delivery checks are not required. Do not claim runtime or delivery verification.

## Authoritative guidance

Read the consumer release's [integration guide](https://github.com/Geeklab-Ltd/audiencelab_ios_sdk/blob/main/docs/INTEGRATION.md), [README](https://github.com/Geeklab-Ltd/audiencelab_ios_sdk), and relevant release metadata/changelog. Use the installed or selected published release's APIs and requirements, rather than assuming a development version is available.

Consumer package URL: `https://github.com/Geeklab-Ltd/audiencelab_ios_sdk.git`. Product/module/pod: `AudienceLabSDK`. Swift entry point: `AudienceLab`. Published versions and XCFramework assets are on the [release page](https://github.com/Geeklab-Ltd/audiencelab_ios_sdk/releases).

The public guide inspected on 2026-09-17 specifies iOS 13+, explicit early initialization, automatic retention after token flow, and the RevenueCat handoff below. Refresh against the relevant release. If official guidance is inaccessible or ambiguous, identify the affected gap and avoid inventing APIs, installation requirements, or service endpoints.

## Interaction and discovery

Infer app target, scheme, language, startup path, dependency manager, SDK version, and configuration source from the workspace. Inspect package/pod declarations and resolved versions, Xcode product linkage or binary integration, startup adapters, purchase code, ad code, and existing event/property calls.

The only required task-specific question is: “What is your Audiencelab API key?” Ask only when a usable key is absent and needed for configuration. Static audits do not need the key. Continue independent work while awaiting it; missing credentials must remain an identified configuration gap.

Optional guiding questions about custom events and properties are allowed and must not block core completion. Do not ask for extra account credentials or make the user choose technical details evident from the app. If access or target selection is insufficient, explain the precise limitation and provide applicable guidance without guessing.

Classify the source integration as missing, partial, or present with specific findings. A dependency alone does not establish app-target linking or reachable initialization.

## Install or repair

Use the app's established dependency mechanism; prefer Swift Package Manager if none is established. Add the published dependency and `AudienceLabSDK` product to the actual app target. Follow the official CocoaPods or XCFramework instructions if those fit the project. Avoid duplicate package/pod/binary installations. Preserve dependency pins, project-generation conventions, and unrelated settings; do not blindly upgrade a healthy integration.

Reuse the app's configuration accessor for the runtime API key. Keep real keys out of tracked source, logs, reports, example snippets, and command arguments. If configuration cannot be completed without the key, explain the missing value rather than presenting an unfinished scaffold as complete. Basic initialization requires no additional permissions; do not add an ATT prompt just to integrate Audiencelab.

Use `AudienceLabOptions` and `AudienceLab.initialize(apiKey:options:)` as documented. Development traffic classification (`isDevelopmentMode`) and local debug logging (`isDebugEnabled`) are separate settings. Apply the app's actual build-configuration conventions so development settings do not leak into shipping builds. App version defaults to the host bundle. Preserve intentional collection controls.

## App opens: required

Place initialization in the common early startup path so every cold launch reaches it, including returning users, completed onboarding, and the app's existing alternate launch routes. Do not initialize only from onboarding, a paywall, login, or a screen that can be skipped. A persisted “already initialized” flag must not suppress initialization in a new process.

Initialize once per intended process startup. For background-to-foreground reopening while the process stays alive, retain the initialized SDK and its documented lifecycle behavior. Do not blindly reinitialize on every scene activation or manually duplicate automatic session/retention reporting. Inspect deliberate reset/deinitialization paths for missing reactivation.

## Purchases: required when purchasing exists

Find the authoritative reporting path for each existing purchase flow: direct AudienceLab SDK calls or RevenueCat reporting. Identify missing callback wiring and duplicate ownership.

For direct reporting, connect documented `sendPurchaseEvent` calls to verified successful transaction handling, using actual product identifiers, price, currency, success status, and stable transaction identifiers. Inspect pending/cancelled/failed outcomes, restores, transaction updates, and replay paths: restored access is not new revenue, and repeated processing must not count a transaction twice. For subscriptions, distinguish immediate purchase callbacks from renewal coverage; describe any documented server-side requirement without inventing a backend.

For RevenueCat, follow the official client handoff on every cold start, after `Purchases.configure` and before the first paywall:

```swift
Purchases.shared.attribution.setAttributes(AudienceLab.getRevenueCatAttributes())
```

Ensure AudienceLab startup wiring precedes its use and the selected release exposes the helper. Use the SDK-provided attribute map, not a creative token, API key, or arbitrary user ID. Inspect existing subscriber login/logout transitions for missing attribute application and follow the installed RevenueCat version's synchronization behavior.

Attribute wiring alone does not establish RevenueCat-to-Audiencelab purchase reporting. Review available configuration or provide instructions from official Audiencelab guidance for the correct RevenueCat app/project, environment, integration/webhook destination, authentication, and purchase/renewal event coverage. Do not guess an endpoint or inspect private backend internals to construct public instructions. Unavailable account configuration is a clearly stated remaining setup step; no live delivery test or additional secret is required.

Avoid direct SDK reporting of the same purchases when RevenueCat owns them unless a documented deduplication contract supports both paths. If the app has no purchasing implementation, mark purchase tracking not applicable and explain future placement without adding a purchase system.

## Ads: required when ads are present

Identify ad SDK/mediation usage, real placements/formats, impression callbacks, and available impression-level revenue callbacks. An unused ad dependency alone does not prove ads are shown.

Wire the selected release's documented `sendAdEvent` to actual displayed ad activity and supported revenue callbacks. Use provider-supplied identifiers, network/source metadata, currency, and revenue; consult the provider's official unit conventions before conversion. A load success is not a displayed impression, and an impression is not proof a reward was earned.

Inspect duplicate reporting through mediation, underlying networks, and wrappers. Do not emit a second full-valued event just to attach late revenue without a documented event/deduplication contract. Never invent watch time, rewards, revenue, currency, or campaign values; follow the SDK's documented representation for unavailable fields and identify unsupported gaps. Preserve loading, presentation, and reward behavior. If the app has no active ads, mark this not applicable and do not introduce ads.

## Optional custom events and user properties

Invite app-specific instrumentation with non-blocking guiding questions such as:

- “Which actions would you like to understand better—onboarding completion, feature use, or game milestones?”
- “Which app-specific user properties would help segment those actions?”

Provide sensible examples and suggested file/callback placement without waiting for an answer. Do not automatically add speculative production instrumentation; implement it when the user's chosen scope supplies the intended events/properties.

Events belong where the action actually completes:

```swift
AudienceLab.sendCustomEvent(
    name: "onboarding_completed",
    params: ["flow": "standard"]
)
```

Properties belong where the value becomes known and should update when it changes:

```swift
AudienceLab.setUserProperty(
    key: "preferred_mode",
    value: "normal",
    set: .whitelisted
)
```

Adapt names and values to the app and check exact-release signatures. Explain the documented whitelisted/blacklisted property semantics; do not interpret these as consent states or generic public/private storage. Underscore-prefixed whitelisted keys are backend-managed. Do not make personal-data collection a setup requirement.

## Finish

Summarize the observed SDK state, changes or audit guidance, selected/resolved version, and separate source/configuration findings for app opens, purchases (direct SDK or RevenueCat), and ads (or not applicable). Include optional event/property guidance and any remaining setup steps. State that runtime/backend delivery was not tested. Do not extend this lightweight task into builds, live transactions, account changes, deployment, or production verification.

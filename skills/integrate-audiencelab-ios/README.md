# Integrate Audiencelab on iOS

An agent skill for installing, auditing, or repairing the Audiencelab native iOS SDK. It helps your AI agent follow the official SDK guidelines for app startup, purchase reporting, RevenueCat integration, existing ads, and optional custom events and user properties.

The skill reviews source code and configuration. It does not run your app or prove that events reached the backend.

## When to use it

Use this skill when:

- Your iOS app needs its first Audiencelab integration.
- The SDK is installed, but startup or event wiring may be incomplete.
- Returning users may skip initialization because setup happens only during onboarding.
- Purchases need direct SDK reporting or an existing RevenueCat connection needs review.
- Your app shows ads and needs impression or revenue reporting.
- You want guidance on useful custom events and user properties.

Request installation or repair to allow local project changes. Explicitly request an **audit only** to receive findings and guidance without edits.

## Requirements

### To install the skill

You need Node.js and npm, internet access, and an AI app supported by the skills installer. Select your app and installation location through the installer prompts.

Installing from GitHub does **not** require a Geeklab account, Geeklab MCP connection, or private catalog token.

### To use the skill

Provide your agent with:

- Access to the iOS app project and its configuration. For changes, the agent needs permission to edit those files.
- Access to the official Audiencelab documentation for the installed or selected SDK release.
- An Audiencelab API key when configuration requires one. Static audits do not need a key.
- Existing purchase, RevenueCat, and ad implementation details available in the project, when those features are present.
- Optional preferences for custom events and user properties.

SDK integration requires an Xcode project or workspace and the dependency tools appropriate to your app. The skill follows the existing package-management convention and prefers Swift Package Manager if none is established. CocoaPods and released XCFramework integration are alternatives documented by Audiencelab.

The SDK guideline baseline recorded in this skill is dated September 17, 2026 and specifies iOS 13 or newer. The agent must consult the selected release's requirements and APIs rather than assume that baseline remains current.

RevenueCat is needed only when your app already uses it as the purchase-reporting path. That path also needs the appropriate RevenueCat-to-Audiencelab integration or webhook configuration. An ad SDK or mediation layer is relevant only when your app already shows ads; the skill does not introduce ads or a purchase system.

Your chosen AI app and existing services have their own account and billing requirements. Skill installation does not provision those services or authorize spending.

## Installation

Run:

```sh
npx skills add 'https://github.com/Geeklab-Ltd/skills/tree/main/skills/integrate-audiencelab-ios'
```

Follow the installer prompts to select a supported AI app and installation location.

This installs the **agent skill**, not the Audiencelab SDK into your iOS app. SDK installation and configuration happen when you ask the agent to apply the skill to your project.

## Usage

1. Open your iOS app project in your chosen AI app.
2. Ask the agent to use `integrate-audiencelab-ios`, specifying whether you want changes or an audit only.
3. If configuration needs a key that is not already available, supply it through your environment's appropriate credential/configuration mechanism. Do not commit it to source control or include it in public requests.
4. Review the changes or findings and complete any identified account-side configuration steps.

The agent infers project details from the workspace. Its only required task-specific question is for a missing Audiencelab API key. It may ask optional guiding questions about custom events and user properties, but those should not delay core setup.

### Install or repair

> Use integrate-audiencelab-ios to inspect this app and install or repair its Audiencelab integration. Cover returning-user launches, purchases through our existing reporting path, and ads if present. Suggest custom events and user properties without blocking setup.

### Audit only

> Use integrate-audiencelab-ios for an audit only. Do not change files. Explain whether startup initialization and purchase reporting follow the SDK guidelines, check our existing ad reporting, and list any remaining setup gaps.

### RevenueCat-focused review

> Use integrate-audiencelab-ios to review our existing RevenueCat purchase reporting. Check the Audiencelab subscriber-attribute handoff, its placement before the first paywall, user transitions, and duplicate reporting. Give guidance for any account configuration you cannot inspect.

## What it covers

| Area | Source and configuration checks |
| --- | --- |
| SDK installation | Dependency, resolved release, app-target product linkage, compatibility, and duplicate installations. |
| App opens | Early initialization on every cold launch, including returning users and alternate launch routes; retained initialization during foreground reopening. |
| Direct purchases | Successful transaction callbacks, actual product/price/currency values, transaction identifiers, restores, replay, and duplicate reporting. |
| RevenueCat | SDK-provided subscriber attributes after RevenueCat configuration and before the first paywall, user transitions, synchronization behavior, and documented connection requirements. |
| Existing ads | Displayed-impression and available revenue callbacks, provider units/currency, reward handling, and duplicate reporting. |
| Optional instrumentation | Relevant event/property examples and suggested placement, with changes driven by your chosen scope. |

The agent should initialize once per intended process startup. It should not use a persistent first-install flag to skip future launches, blindly reinitialize on every scene activation, or duplicate automatic session and retention reporting.

For RevenueCat, the documented client handoff is:

```swift
Purchases.shared.attribution.setAttributes(AudienceLab.getRevenueCatAttributes())
```

The agent checks that the selected release supports this helper and that it is used in the documented startup sequence. This client call alone does not establish a functioning purchase-reporting connection.

## Expected outputs and completion

Expect a summary containing:

- The observed integration state: missing, partial, or present with specific findings.
- Installation or repair changes, or audit-only instructions.
- The selected or resolved SDK version and relevant integration locations.
- Separate findings for startup, purchases, RevenueCat where applicable, and ads.
- Suggested custom events and user properties with examples and placement guidance.
- Remaining setup steps and a statement that runtime/backend delivery was not tested.

Check completion by reviewing the identified files and configuration against the relevant official SDK release guidelines. Confirm that required wiring is covered, missing values and external setup are explicitly identified, and absent purchase/ad features are marked not applicable.

Completion here means guideline-based source and configuration work. It does not mean that the app was built, a purchase was tested, or an event was observed in an Audiencelab dashboard.

## Troubleshooting

| Problem | What to check |
| --- | --- |
| SDK dependency exists, but integration is incomplete | Confirm the SDK product is linked to the actual app target and initialization is reachable. A package declaration alone is insufficient. |
| Returning users skip initialization | Look for setup confined to onboarding, login, a paywall, or a persisted “already initialized” flag. Initialization belongs in the common startup path. |
| Configuration needs an API key | Use the intended app's runtime configuration accessor. Keep real keys out of tracked source, logs, reports, and command arguments. |
| RevenueCat is installed, but purchase reporting is unclear | Review the attribute handoff and the separate documented integration/webhook configuration. Do not assume the client setter establishes backend reporting. |
| Purchases or ads may be counted twice | Trace reporting ownership across direct SDK calls, RevenueCat, mediation, underlying ad networks, and wrappers. Use only documented deduplication behavior. |
| Ad revenue values are unavailable | Use supported provider callbacks and the SDK's documented representation for unavailable fields. Do not invent amounts, currency, watch time, or rewards. |
| APIs differ from examples | Consult the installed or selected published release's documentation and metadata. Do not assume newer development APIs are available. |
| Official guidance or project access is unavailable | Expect the agent to explain the affected gap and provide applicable guidance, rather than invent configuration or choose an ambiguous app target. |

## Limitations

- This is a lightweight source/configuration workflow. It does not run builds, simulator sessions, token validation, test transactions, live ads, or backend delivery checks.
- It does not deploy, modify external accounts, configure a private backend, or authorize production verification.
- RevenueCat account-side setup may remain a separate action when configuration is unavailable. The skill does not include private service endpoints or backend implementation details.
- Basic Audiencelab initialization requires no additional permissions according to the supplied guidelines. The skill preserves existing collection controls and does not add an ATT prompt merely to install the SDK.
- Custom events and properties are optional. Suggested examples do not authorize speculative production instrumentation or personal-data collection.
- The package contains `SKILL.md` only. There are no bundled scripts, reference files, or assets; official SDK documentation is linked externally.
- Installing the skill alone does not supply an API key, install the app SDK, create service accounts, or connect RevenueCat.

## Official SDK resources

- [Audiencelab iOS SDK repository and README](https://github.com/Geeklab-Ltd/audiencelab_ios_sdk)
- [iOS integration guide](https://github.com/Geeklab-Ltd/audiencelab_ios_sdk/blob/main/docs/INTEGRATION.md)
- [Published releases and XCFramework assets](https://github.com/Geeklab-Ltd/audiencelab_ios_sdk/releases)

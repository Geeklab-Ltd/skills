# Create app icons

[![Repository installs on skills.sh](https://skills.sh/b/Geeklab-Ltd/skills)](https://skills.sh/Geeklab-Ltd/skills)

Create original app icons or revise an existing design with your AI app’s native image generation, then prepare organized files for iOS/iPadOS, Android launchers, Google Play, and marketing.

Use `create-app-icons` for a new app brief, an icon redesign, or distinct visual concepts. The skill guides artwork creation and review; its bundled Python helper exports prepared images into platform-specific assets.

## Requirements

- **For installation:** Node.js and npm, an internet connection, and an AI app supported by the skills installer.
- **For artwork creation:** an AI app with native image generation and the ability to inspect images. Installing this skill does not add image generation to an app that lacks it. Your host’s account, subscription, and usage limits apply. Another generator is used only when you explicitly choose it.
- **For the bundled exporter:** Python 3, Pillow, and permission to read input images and write a local output folder. Use a current Pillow release with `Image.Resampling` and `ImageCms` support. The helper runs locally and requires no API key.
- **For project integration:** Xcode on macOS for an iOS/iPadOS project, or Android Studio and an Android project for launcher integration. Store publishing requires your own developer accounts and is separate from generating the assets.

No Geeklab account, Geeklab MCP connection, or private catalog token is required to install or use this package.

## Installation

Install through the [skills.sh CLI](https://skills.sh/docs/cli), the default way to install this skill. With Node.js and npm available, run this command from the project where you want to use the skill:

```sh
npx skills add Geeklab-Ltd/skills --skill create-app-icons
```

Follow the installer prompts to select a supported AI app and installation location. No Geeklab account or MCP connection is required for installation. The badge above reports installs for the whole Geeklab Skills repository, not this skill alone. See the [skills installer documentation](https://github.com/vercel-labs/skills) for available apps and installation options.

Keep the complete installed skill directory together:

```text
create-app-icons/
├── README.md
├── SKILL.md
├── references/
│   └── platform-deliverables.md
└── scripts/
    └── export_icons.py
```

The reference and script are included supporting files. Copying only `SKILL.md` leaves the export workflow incomplete.

### Set up the exporter

From the installed directory containing `SKILL.md`, create a Python environment and install Pillow:

```sh
python3 -m venv .venv
```

Activate it on macOS or Linux:

```sh
source .venv/bin/activate
```

On Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Then install Pillow using the activated environment:

```sh
python -m pip install --upgrade Pillow
```

See [Pillow installation instructions](https://pillow.readthedocs.io/en/stable/installation/basic-installation.html) if your environment needs additional setup. A host without command execution can still help design the artwork; run the export helper yourself or use an equivalent deterministic image workflow.

## What to provide

Give your agent the app’s purpose, intended audience, preferred motif, colors, and target platforms. Attach brand assets or visual references when available.

For a redesign, identify the features that must remain recognizable. Request multiple concepts explicitly if you want variants; otherwise, the skill does not assume you need several designs.

The visual direction may use a bold flat symbol, a softly lit tactile object, a playful face or mascot, or a compact illustrated scene. The direction should fit the app and stay recognizable at approximately 48 px.

## Usage

### Ask your agent to create or revise the icon

Mention `create-app-icons` in your request and provide a concrete brief. For example:

> Use create-app-icons for TrailNote, a hiking journal for casual walkers. Create one friendly, bold flat symbol combining a trail and a notebook. Use forest green and warm cream, with no lettering. Deliver iOS/iPadOS, Google Play, Android adaptive and legacy launcher assets, and a marketing image. Prepare a separate transparent Android foreground, an opaque background, and a monochrome foreground if the motif works in one color. Keep the essential shape readable at 48 px and under circular and rounded-square masks. Save everything in a new trailnote-flat output folder and leave existing assets untouched.

For a revision, attach the existing icon and describe what to preserve and what to change. References inform the visual traits; they should not be copied into a protected mark, character, or near-identical composition. Supply verified artwork for exact logos or lettering.

### Prepare the source images

The helper requires the following inputs. Each must be square and at least 1024 × 1024 px:

| Input | Requirement |
| --- | --- |
| Color master | Fully opaque, full-bleed artwork without baked-in rounded corners, borders, store badges, mockups, or promotional text. |
| Android foreground | Separate artwork with a transparent exterior. Keep essential content within the adaptive safe area. |
| Android background | Separate, fully opaque artwork covering the entire square. |
| Monochrome foreground, optional | A clean single-color silhouette on transparency, preferably white. The helper checks transparency and visible content, but does not enforce a single color. |

Android adaptive layers occupy 108 × 108 dp, with a centered 66 × 66 dp area that avoids clipping under launcher masks. Check the [Android adaptive icon guidance](https://developer.android.com/develop/ui/compose/system/icon_design_adaptive) and preview the layers together. Removing a background from a flattened master does not automatically produce a suitable adaptive foreground.

### Export one variant

With the Python environment active, run this from the installed skill directory. Replace the image paths with your actual files and choose a new or empty output folder:

```sh
python scripts/export_icons.py \
  --master /path/to/MASTER.png \
  --foreground /path/to/FOREGROUND.png \
  --adaptive-background /path/to/BACKGROUND.png \
  --out /path/to/trailnote-flat
```

Add the optional monochrome layer when available:

```sh
python scripts/export_icons.py \
  --master /path/to/MASTER.png \
  --foreground /path/to/FOREGROUND.png \
  --adaptive-background /path/to/BACKGROUND.png \
  --monochrome /path/to/MONO.png \
  --out /path/to/trailnote-flat-themed
```

These examples use POSIX shell line continuation. In PowerShell or another shell, enter the command on one line or use that shell’s continuation syntax.

Use a separate output folder for every variant. The helper rejects a nonempty folder. Optional `--border-color` and `--canvas-color` arguments customize the marketing image; their defaults are `#D5D9DF` and `#FFFFFF`. They do not add borders or rounded corners to the store uploads.

## Expected outputs

For each variant, the helper creates:

| Folder | Contents |
| --- | --- |
| `source/` | Normalized 1024 × 1024 color master, adaptive foreground, adaptive background, and optional monochrome foreground. These are resized source copies, not backups of larger original inputs. |
| `apple/` | `AppIcon-1024.png`: an opaque 1024 × 1024 RGB PNG. |
| `google-play/` | `listing-icon-512.png`: a 512 × 512 RGBA PNG with an sRGB profile. Export fails if it exceeds 1024 KB. |
| `android/res/mipmap-{density}/` | `ic_launcher.png` and circular `ic_launcher_round.png` legacy icons at 48, 72, 96, 144, and 192 px. |
| `android/res/drawable-{density}/` | Adaptive foreground and opaque background layers at 108, 162, 216, 324, and 432 px, plus monochrome layers when supplied. |
| `android/res/mipmap-anydpi-v26/` | `ic_launcher.xml` and `ic_launcher_round.xml`, referencing the exported adaptive layers. A monochrome entry is included when supplied. |
| `marketing/` | `icon-1080-rounded-border.png`: a separate 1080 × 1080 presentation image with rounded corners and a visible border. |

The five densities are `mdpi`, `hdpi`, `xhdpi`, `xxhdpi`, and `xxxhdpi`. The helper converts tagged inputs to sRGB and treats untagged inputs as sRGB. It does not generate the artwork or repair poorly composed layers.

The Google Play listing image is separate from the installed launcher icon. Google requires a 512 × 512, 32-bit PNG no larger than 1024 KB and applies the outer corner mask and shadow itself. See [Play Console image requirements](https://support.google.com/googleplay/android-developer/answer/9866151) and [Google Play icon design specifications](https://developer.android.com/distribute/google-play/resources/icon-design-specifications).

## Import and verify

For an iOS/iPadOS asset-catalog workflow, add `apple/AppIcon-1024.png` to the matching 1024 px image well in your `AppIcon` set. Xcode can derive smaller sizes when configured for Single Size. Confirm the target uses the intended icon set and review [Apple’s asset-catalog instructions](https://developer.apple.com/documentation/xcode/configuring-your-app-icon).

The helper exports a flat Apple PNG. It does not create an Icon Composer project or explicit dark, tinted, or layered Apple variants. Projects using those workflows need additional preparation; see [Apple’s Icon Composer documentation](https://developer.apple.com/documentation/xcode/creating-your-app-icon-using-icon-composer).

For Android, review and copy the exported resources from `android/res/` into your app’s intended resource source set, commonly `app/src/main/res/`. Resolve any existing resources with the same names before replacing them. The helper does not edit `AndroidManifest.xml`; confirm its `android:icon` references `@mipmap/ic_launcher`, and use `@mipmap/ic_launcher_round` if your app sets `android:roundIcon`. Preview launcher shapes and themed icons in Android Studio using its [app icon tools](https://developer.android.com/studio/write/create-app-icons).

Before handing off or uploading:

- Check image dimensions, opacity, color modes, and the Google Play file-size limit.
- Inspect the icon at about 48 px and under square, circular, and rounded-square masks. Check clipping, contrast, thin features, and proportions.
- Inspect foreground and background together. A safe-zone warning requires visual review; it does not automatically resize or correct the artwork.
- Build and preview the icons in the target projects when available. If projects are unavailable, treat the delivery as exported files with integration still pending.
- Share the marketing PNG and delivery folder or archive, and identify the selected visual direction. Keep the marketing image separate from platform uploads.

Read [the bundled platform reference](references/platform-deliverables.md) and recheck its official links at export time, because platform requirements can change.

## Troubleshooting

| Problem | Action |
| --- | --- |
| `npx` is unavailable | Install Node.js and npm, reopen your terminal, and retry the installation command. |
| The installer cannot find the skill | Confirm the repository and skill directory are publicly available. Installation from the stated URL becomes available after publication. |
| A reference or script is missing locally | Reinstall or retrieve the complete skill directory, preserving `references/` and `scripts/` beside `SKILL.md`. |
| Your AI app cannot generate or inspect images | Use a host that provides those capabilities, or explicitly choose another generator. The skill cannot supply missing host tools. |
| `No module named PIL` or missing Pillow APIs | Activate the environment used for export and install or upgrade Pillow with that environment’s Python. |
| An input must be square or at least 1024 px | Prepare a square image of sufficient resolution. Avoid stretching artwork to satisfy the check. |
| The master or background must be opaque | Supply fully opaque artwork. A transparent foreground cannot substitute for either input. |
| The foreground must have a transparent exterior, or has no visible artwork | Provide a visible foreground on transparency. For an optional monochrome input, provide a visible single-color silhouette. |
| Artwork reaches outside the adaptive safe zone | Inspect mask previews and reposition or scale the source artwork when essential content would be clipped. |
| Google Play PNG exceeds 1024 KB | Simplify or optimize the source artwork and export again into a new or empty folder. Preserve the required format and dimensions. |
| Output folder is not empty | Choose a new folder. If export fails after writing some files, retain or review that partial output and retry in another folder. |
| An sRGB conversion fails | Check the source image’s embedded color profile and re-export it with a valid profile. |
| Android icons do not appear in the app | Check the resource source set, manifest references, and existing resources that may override the export, then rebuild and preview. |

## Limitations

This is an instruction package and local export helper, not a hosted image service or an automatic store-publishing tool. Artwork quality depends on your host’s image generator and visual review. Generated lettering is not reliable source artwork for exact branding.

The helper validates basic input properties and some export constraints. It does not prove that a foreground has a clean exterior, that a monochrome layer uses one color, that the artwork is legible, or that an app store will accept the result. Android safe-zone checks are warnings based on visible pixels, not a substitute for mask previews.

The package targets iOS/iPadOS, Android launcher icons, and the Google Play listing, plus its marketing presentation. Other form factors, notification icons, vector deliverables, Apple appearance variants, and Icon Composer files require additional work. Android themed-icon behavior depends on the platform and launcher.

Exporting files does not integrate them into a project, upload them to a store, or verify a build. Keep original high-resolution artwork separately and finish platform checks in your own projects.

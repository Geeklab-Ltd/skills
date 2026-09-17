# Public skill README guidelines

Apply these defaults when creating or updating the repository README and public skill READMEs.

## Installation default

Use the skills.sh CLI as the primary installation method. Link to https://skills.sh/docs/cli and https://github.com/vercel-labs/skills for current supported apps and options.

Under a heading exactly named `## Installation`, explain that readers need Node.js, npm, and internet access, then lead with the repository command:

```sh
npx skills add Geeklab-Ltd/skills
```

For a specific skill README, lead with `npx skills add Geeklab-Ltd/skills --skill` followed by that package's actual frontmatter name. Do not leave a generic name in the finished README.

Tell readers to follow installer prompts to choose a supported AI app and installation location. Public GitHub installation requires no Geeklab account, Geeklab MCP connection, or private catalog token. Keep manual installation secondary, only when relevant.

## Install-count badge

Add this documented repository-level badge near the title or overview of each public README:

```md
[![Repository installs on skills.sh](https://skills.sh/b/Geeklab-Ltd/skills)](https://skills.sh/Geeklab-Ltd/skills)
```

Identify it as the repository install count; do not describe it as a count for an individual skill. Use a skill-specific badge only if its endpoint is established by current official documentation.

## Accuracy and future updates

Explain actual prerequisites for using each skill separately from installing it: host capabilities, tools, dependencies, accounts, configuration, and supporting files. Installing an instruction package does not provision any of these.

Preserve source-grounded examples, outputs, limitations, and troubleshooting. Keep secrets and private company/customer context out of public documents. Do not invent licenses, tested results, supported apps, or account-side configuration.

Keep the collection README and package READMEs consistent with these installation defaults on every publication or regeneration. Do not overwrite skill instructions or change approval/access settings while editing documentation.

Skills.sh listing and ranking are driven by recorded CLI installs, not simply by publishing a repository. Respect users' telemetry opt-out choices; do not require telemetry or automate installs to inflate counts. The official explanation is at https://skills.sh/docs/faq.

These are repository authoring instructions. Any separate publishing application's README-generation settings must be maintained in that application too; this file alone does not update its stored prompt.

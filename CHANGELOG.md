# Changelog

This file follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and versions follow [Semantic Versioning](https://semver.org/). While this is a test build, versions stay below 1.0.

Each version is exactly one signed file. A version's tag is never moved or re-pointed. Any new signature, even one that only renames the file, gets a new version.

## [0.1.0] - 2026-10-02

First public release.

### Files

- `release/PROSOCHĒ.shortcut`, 160,494 bytes, SHA-256 `fa107e2974025c38ed80ee3cdc8f4122523ebc4e607dfe7d42704fa0ec1cba99`
- `source/PROSOCHE.xml`, 1,777,487 bytes, SHA-256 `18b6ce8a1db283a4697db85a070db821bb1a0878d3f9dfbdaa604df101dd19ca`

To check both, and that the signed file contains exactly that source, see [docs/VERIFY.md](docs/VERIFY.md).

### What is in it

- One shortcut, with two import questions.
- Two automations that you make yourself: one runs it when an app is opened, the other when an app is closed.
- Responses in proportion to your recent behaviour: nothing at all for most opens, then a pause, a question, or stepping in.
- Saying how long you mean to stay keeps opens inside that time silent.
- Ways out: another app, a web page, a web search, a Maps search, or a quick note named Capture.
- A manual menu with four items: Read Me, Setup Check, Toggle Voice, Emergency Restore.
- Nothing is fetched from the internet.
- No AI model.

It has only been tried on iOS 26 and has not been walked on iOS 27. Putting back the screen, sound and colour changes is still being checked on phones.

### Known issues

- The second import question reads "Can this shortcut speak out loud to you ?", with a space before the question mark.
- The steps inside the PROSOCHĒ Note skip three on-screen labels that the README includes: Choose, the ✓ button, and Next.
- Adding the shortcut again and choosing Replace can leave two copies with the same name (seen on the iOS 26.5 simulator). Delete the older one.

The full list is in [docs/KNOWN-LIMITATIONS.md](docs/KNOWN-LIMITATIONS.md).

### Upgrading from an earlier test build

When Shortcuts says you already have a shortcut with this name, choose Replace, never Keep Both. Afterwards, look in your library for two PROSOCHĒ tiles, and if there are two, delete the older one. If you had an older version with a longer name, the new file installs as a separate shortcut: open each automation and point its Run Shortcut action at PROSOCHĒ.

PROSOCHĒ is source-available, free for noncommercial use, under the PolyForm Noncommercial 1.0.0 licence.

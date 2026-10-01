# Privacy

This page says what PROSOCHĒ remembers, where it keeps it, and what it can and cannot do on your phone. Each point stands on its own.

## What it remembers

- PROSOCHĒ remembers what it needs in one file, `PROSOCHE/state.json`, in the Shortcuts folder of your iCloud Drive.
- It also keeps one Note, named PROSOCHĒ. That Note holds the guide that Read Me opens.
- It creates a second Note, named Capture, only if you choose to jot something down as a way out. If you never choose that, there is no Capture Note.
- With iCloud Drive and Notes switched on, Apple may sync that file and those Notes through your own iCloud account. That is Apple's doing, under your account.
- PROSOCHĒ itself sends nothing anywhere.

## No analytics

- There are no analytics, no tracking, no account and no ads.
- Nobody is told when you open an app, how often, or what you answered.

## Nothing is fetched from the internet

- Nothing in the shortcut fetches anything from the internet. It contains no actions that download a page, request a web address or call a model.
- The only actions that reach outside the shortcut hand you off to an app you choose: one Open URL, one Search Web, one Search Maps and nine Open App. Each one runs only when you pick a way out.
- You can count these yourself with tools that come with your Mac: [the check](VERIFY.md).

## No AI model

- This release uses no AI model and makes no model call.

## You are in charge

- PROSOCHĒ is a nudge you set up for yourself. It is not a lock and it is not parental control.
- You can turn off either automation, or delete the shortcut, at any time. Nothing stops you.

## What it may change on your phone

- Your screen brightness, your sound volume and a display colour setting.
- Before changing brightness or sound, PROSOCHĒ reads the current setting and saves it. When it is done, it puts the setting back.
- Emergency Restore, in the manual menu, puts all three back at any time. Open PROSOCHĒ in the Shortcuts app and choose it.
- This put-back is what PROSOCHĒ is built to do, and it is still being checked on phones.

## The prompts you will see

The first time each part of PROSOCHĒ runs, iOS asks your permission. You may see a question about:

- sending a notification
- saving a file (this is the state file in iCloud Drive)
- opening a link
- searching the web
- changing a display colour setting

Each prompt comes from iOS, not from PROSOCHĒ. Say no and that part will not run.

For what else PROSOCHĒ cannot do, see [Known limitations](KNOWN-LIMITATIONS.md).

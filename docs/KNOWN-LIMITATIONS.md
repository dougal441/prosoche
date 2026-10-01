# Known limitations

This is an early test build. Here is what it does not do, and what it does instead.

## By design

- It can be switched off. It is a nudge you set up for yourself, not a lock and not parental control. You can turn off either automation, or delete the shortcut, whenever you like, and nothing will stop you. Anyone can bypass it.
- It acts only at the next time you open or close one of your apps. A shortcut that is shared like this gets no timer, so there are no timers running in the middle of a session. If you go over the time you said, PROSOCHĒ notices at your next open, not before.
- The two Personal Automations that run it cannot be installed by a shortcut. You make them by hand, as the README shows.

## What Shortcuts cannot do, and what PROSOCHĒ does instead

- Shortcuts cannot add to a Note it finds on your phone. So nothing is appended to the PROSOCHĒ Note or to Capture. The running record lives in the state file, `PROSOCHE/state.json`, in iCloud Drive.
- Colour Filters cannot be read back. PROSOCHĒ cannot tell whether the display colour setting is on or off, so every recovery path switches it off.
- A setting whose original value cannot be read is left alone, rather than guessed at.
- The signed file carries no display name. The file name becomes the shortcut's name, which is why it must be called PROSOCHĒ when you add it.

## This build

- Screen, sound and colour changes are put back when PROSOCHĒ is done. This is still being checked on phones. If your screen stays dim, quiet or grey, open PROSOCHĒ in the Shortcuts app and choose Emergency Restore.
- The first time each part runs, iOS asks your permission: notifications, saving a file, opening a link, searching the web, changing a display colour setting. If a prompt goes unanswered you will see "Automation failed … took too long to run". Nothing is broken. Run Setup Check from PROSOCHĒ's manual menu, then tap ▶ on that automation again.
- It has only been tried on iOS 26. It has not been tried on iOS 27, and the setup steps have not been walked there.
- The setup steps were walked on the iOS 26.5 simulator. The author imported and ran this release on his own iPhone.
- Three small copy and import issues are known:
  - The second import question reads "Can this shortcut speak out loud to you ?", with a space before the question mark.
  - The steps inside the PROSOCHĒ Note skip three on-screen labels that the README includes: Choose, the ✓ button, and Next.
  - Adding the shortcut again and choosing Replace can leave two copies with the same name (seen on the iOS 26.5 simulator). If you see two PROSOCHĒ tiles, delete the older one.

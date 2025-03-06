# Railloader Bulletin

This repository hosts the code necessary to create the bulletins for Railloader, and is the default source for Railloader's mod bulletins.

## What are bulletins?

Bulletins can be seen as a kind of "online hotfix" for Definition.jsons. If a mod becomes obsolete because e.g. a dependency has been updated,
or the game has updated and the mod is no longer working as expected, the mod can be disabled by the bulletin and will no longer load (assuming
the user has turned on the bulletin feature).

## How does it work?

Inside [bulletins/](bulletins/), there are [YAML](https://en.wikipedia.org/wiki/YAML) files, each containing a list of bulletin entries. For simplicity's sake,
each mod is allowed to have one YAML file at most. Authors are encouraged to use a single file for their mods if possible, although this is not strictly necessary.

Each bulletin entry is an object with the following structure:
```yaml
# Starting a new array entry. Important: in YAML, indentation (2 whitespaces) is important, compared to JSON.
- # It's recommended to actually put a comment on this line to describe what the entry is supposed to do.
  # The list of mods that this entry will affect if it is active. This SHOULD always be AT LEAST an id and notAfter.
  # Each comment should start with the date - in yyyy-MM-dd format. (e.g. 2025-12-24).
  mods:
  - id: SomeMod # This targets SomeMod...
    notAfter: 1.0.2 # up to and including version 1.0.2.0

  # Requires is similar to RL's Definition.json, and makes it possible to filter this bulletin.
  # If available, ALL requires must be met in order for this entry to become active. If even one reference is not available,
  # the entry will be ignored. This follows the usual RL id/notBefore/notAfter system, too.
  requires:
  - id: railroader # Only include this entry if 'railroader'...
    notBefore: 2024.6 # ... is at least 2024.6

  # Analog to the Definition.json, conflictsWith can be set to avoid loading this entry if ANY of the conflicts matches.
  # Also analog to the requires, this one is optional.
  conflictsWith: # No entries, always active.

  # This message will be printed on-screen with the mod whenever a save is loaded.
  message: "This mod is outdated and requires an update to run with this version of Railroader."

  # If set, a "More information" button is displayed that will open this URL.
  url: "https://railroader.stelltis.ch/mods"

  # If available and set to true, it will force the mod to fail loading, treating it as if it had an invalid Definition.json/other mod problem.
  # This can be thought of as a "remote killswitch" to disable mods that would otherwise cause problems.
  forceFail: true
```

Whenever the master branch is merged, a build is triggered which will compile a new JSON, which then has to be manually deployed in order to take effect.

## Contribution Workflow

In order to create an entry, make a PR in this repository with the change(s) that you want to do. Usually, the entry should be in a file that clearly identifies
either the mod that acts as trigger for the break (e.g. Strange Customs updates), or the mod that is the one that will be broken (e.g. some map mod). When in doubt,
you can open an issue to explain your request in detail, and I'll see what can be done.

Otherwise, there are some ground rules:

- **This is not meant as a generic update announcement feature.** Although it's possible to make bulletin posts without forcing a mod to fail, this feature is not
  meant as an update indicator for users. The exception to this rule is that mods which have significant updates that fix major bugs, where it is in the interest
  of the community to roll out changes quickly, without necessarily breaking the game experience immediately, are OK. For example: A game update causes a mod to
  sometimes unload a tender completely, and a fixed version is released. This would be an OK usage of the feature.
- **Mod updates are preferred over bulletins.** If possible (e.g. the mod author is still active), an update of their mod with a proper Definition.json `conflictsWith`
  is preferred.
- **Do not sabotage other mods.** Entries must have a valid reason to exist, either because they inform users about an important update/notice, or because they ensure
  that possibly questionable mod combinations are prevented. All entries should have some kind of `notAfter` that allows authors to publish a new, fixed version that
  then would no longer be affected by the bulletin. Blanket bans of mods are to be avoided, and proposing to ban a mod because you don't like it or its author is
  similarily a no-go.
- **Use proper spelling and comment your entries.** Entries should contain a date when they are added, and have a succint description of what they are for.

As this is still a new system/idea, we'll see what other requirements will come as time goes on. 

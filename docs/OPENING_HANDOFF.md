# Opening → gameplay: one player identity

The supplied `gaming-the-system-main.zip` already collects a name in
`src/App.tsx`. It stores the trimmed value in `playerName` when the identity form
submits. Its last beat is `officeEnd`, currently offering REPLAY OPENING. It has
no gameplay completion callback yet. This revision prepares the gameplay side;
the partner's opening is still separate and has not been merged or deployed.

## Integration point in the supplied opening

Copy this repository's `src/Gameplay.tsx`, `src/levels`, `src/shared` and
`src/assets` together into the final project. Keep the gameplay artwork imports
relative to those folders. Import the base stylesheet once in the host entry:

```tsx
import './shared/styles/base.css';
```

In the opening's App, import Gameplay, extend its Beat union with `'gameplay'`,
and add this return **after all hooks and before its existing return**:

```tsx
import Gameplay from './Gameplay';

// Inside the opening App, after every hook:
if (beat === 'gameplay') {
  return <Gameplay playerName={playerName} />;
}
```

At the existing `officeEnd` beat, the final handoff action can be:

```tsx
<button
  className="cinematic-button"
  onClick={() => {
    audio.fadeOfficeOut();
    setBeat('gameplay');
  }}
>
  CONTINUE TO LEVEL 1
</button>
```

The handoff can also run automatically at the actual final animation's end.
Use the already confirmed `playerName`, not the temporary `draftName`. Do not
add a second name form or put the name in URLs/browser storage. A differently
structured opening can mount `<Gameplay playerName={playerName} />` in its own
end-of-opening callback. Restarting the full game means unmounting Gameplay and
returning the opening to its initial title/name state.

The full host also owns a restored-page reset. Add this hook alongside the
opening's existing hooks so restoring a closed page from the browser's
back-forward cache returns to the title/name entry as well:

```tsx
useEffect(() => {
  const fresh = (event: PageTransitionEvent) => {
    if (!event.persisted) return;
    audio.reset();
    setDraftName('');
    setPlayerName('');
    setBeat('title');
  };
  window.addEventListener('pageshow', fresh);
  return () => window.removeEventListener('pageshow', fresh);
}, [audio.reset]);
```

## Contract and presentation

`GameplayProps.playerName` is required. The same value is passed to Levels 1, 2
and 3 across their in-page transitions. Each level trims outer whitespace and
uses the name for the player speaker label, typing label and temporary
cinematic captions. Teacher and student have distinct, role-based portrait
icons; neither avatar depends on a name or initial. React renders names as text. Names are not
translated or inserted as HTML. Alex remains Alex. Player-facing Restart controls have been removed from all levels; a new page runs the host opening again.

The source role ID `Maya` identifies the player character internally, including
left-side styling. It is never a fixed display name when a custom name is
supplied. Future scenes should resolve that role using `request.playerName`.

All three cinematic renderers receive a `playerName` field:

```tsx
<Gameplay
  playerName={playerName}
  renderLevelOneCinematic={(request, complete) => (
    <PartnerScene
      sceneId={request.sceneId}
      playerName={request.playerName}
      onComplete={complete}
    />
  )}
  renderLevelTwoCinematic={(request, complete) => (
    <PartnerScene
      sceneId={request.sceneId}
      playerName={request.playerName}
      onComplete={complete}
    />
  )}
  renderLevelThreeCinematic={(request, complete) => (
    <PartnerScene request={request} onComplete={complete} />
  )}
/>
```

`onLevelOneComplete`, `onLevelTwoComplete` and `onLevelThreeComplete` are optional
result callbacks; the earlier two shapes are unchanged. Level 3's request and
comparison result are documented in [Level 3 handoff](LEVEL3_HANDOFF.md).
Keep Gameplay mounted throughout each scene
and call `complete()` only at its end. Branches/scores never depend on the name.

`src/App.tsx` is the standalone preview entry. It intentionally uses **Maya**
because these downloadable previews exclude the opening. It is not the final
host integration entry. `initialLevel={2}` or `{3}` is available for direct work;
the real opening hands off at the default Level 1. Empty names in standalone
level usage also fall back to Maya; the opening itself requires a nonempty name.

Player decisions use the first person: “What if I tracked three?” and
“What am I still missing?” Spoken exchanges address Alex and respond to his
actions. This supersedes the older narrative's collective wording.
Management speaking for itself and dialogue referring to students as a group
can still use the plural where its meaning requires it.

The browser integration check `tests/player_identity.py` exercises an opening
name-form harness, Levels 1 and 2, both placeholder and custom scene routes,
restart/reload and names with punctuation/long text. It does not claim that the
separate Netlify opening has already been connected.

`tests/level3_integration.py` additionally checks the same name through Level 2
→ Level 3, weighted shot requests, comparison/theory renderers and the optional
reserved, unused Design Lab callback. The combined preview connects all three gameplay levels;
individual App modes mount only their selected level.

Level 2 → Level 3 also carries the three chosen metric IDs in page memory. The
Level 3 selector starts with those cards checked and allows replacement; direct
standalone Level 3 has no inherited choices. Custom hosts can pass
`initialMetricIds` directly to `LevelThree`. The final scene chain is
`level3.compare` → `theory.reveal`. This preview stops in the theory placeholder.
The reserved `onDesignLab` prop is not invoked; even a duplicate final cinematic
callback cannot advance into Design Lab. Administrator access is deferred.

Level 3 trials now record the player’s experiment aim, and final requests include an optional keep/rethink `decision`. Completion waits for that judgment; `compared` can be `null` when all three actual tests have the same weight-pattern class. See [Level 3 contracts](LEVEL3_HANDOFF.md).

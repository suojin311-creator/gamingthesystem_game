# Standalone local Design Lab

- Original Lab baseline: feature/design-lab-local at 4c9217e. Current integration is explicitly user-authorized.
- User now authorized integration on animation/opening-integration, after GitHub backup. Serve the approved game at /game and the Lab at /; preserve stable aliases.
- Implement the classroom service with Go standard library only, cross-compiled to a self-contained Windows executable; no cloud subscriptions or external runtime requests.
- React/Vite development uses existing root dependencies; build only this standalone entry.
- Writing: fixed 90 seconds. Review is untimed and never shows the author their
  own reflection. The server skips own work in each personal queue. No review or
  global sharing deadline may advance unanswered cards. A selected vote locks,
  briefly acknowledges the choice, then automatically advances to the next card.
- Up to 21 participants; authors see 20 others with a full class. Early finishers
  wait until everyone completes their personal queue. Ties remain adjacent.
- No moderation/anti-troll features, game-data sync, or game-progress saving.
- Closing: static read-only ranking for 12 seconds, with manual scrolling only;
  remove the scan/highlight and its audio/control. Both questions keep the same
  ranking background and softly fade between one another, four seconds per phase.
  Reveal Goodhart with a slower staged portrait/title/quote entrance. Predecode
  the portrait, respect reduced motion and keep the question/ending layers mounted
  across transitions. No surrounding quotation marks on the final quote.
  No host reveal button after question 2; empty-class fallback may reveal manually.
- Writing prompt: "What is one change you would make to help Alex learn more deeply?". Remove the
  Join the audience button. First question: "Did the most flowers mean the deepest
  thinking?"; second question remains unchanged. Use only the short accepted quote:
  "When a measure becomes a target, it ceases to be a good measure."
- Test timed writing/ranking/questions, untimed others-only queues, immutable votes, simultaneous clients and actual browser transitions. Do not run the game packaging/release suites for this isolated feature.
- Integrated review package: play/Gaming-the-System-classroom.zip, with the Windows launcher, embedded game and Lab. The original independent branch is preserved. Never claim native Windows execution was tested on Linux.

# Standalone local Design Lab

- User explicitly authorized this feature on its own branch: `feature/design-lab-local`.
- Keep game source, existing playable ZIPs and animation/stable branches unchanged.
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
- Writing prompt: "How would you know Alex is really learning?". Remove the
  Join the audience button. First question: "Did the most flowers mean the deepest
  thinking?"; second question remains unchanged. Use only the short accepted quote:
  "When a measure becomes a target, it ceases to be a good measure."
- Test timed writing/ranking/questions, untimed others-only queues, immutable votes, simultaneous clients and actual browser transitions. Do not run the game packaging/release suites for this isolated feature.
- Package only `play/Design-Lab-local.zip` with a Windows launcher and embedded UI. The user's host computer is Windows. Never claim native Windows execution was tested on Linux.

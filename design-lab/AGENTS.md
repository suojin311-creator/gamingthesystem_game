# Standalone local Design Lab

- User explicitly authorized this feature on its own branch: `feature/design-lab-local`.
- Keep game source, existing playable ZIPs and animation/stable branches unchanged.
- Implement the classroom service with Go standard library only, cross-compiled to a self-contained Windows executable; no cloud subscriptions or external runtime requests.
- React/Vite development uses existing root dependencies; build only this standalone entry.
- Writing: fixed 90 seconds. Anonymous review: at most 10 seconds per reflection, optional early Next after voting; timeout means no vote. Votes lock after one choice. Authors can skip their own reflection.
- Up to 21 participants. Early finishers wait; all finish or the N*10-second deadline produces one frozen flower ranking. Ties share rank and remain adjacent.
- No moderation/anti-troll features, game-data sync, or game-progress saving.
- Closing: accelerating ranking highlight, both agreed questions, then Goodhart portrait/quotation.
- Test service deadlines, immutable votes, simultaneous clients and actual browser flow. Do not run the game packaging/release suites for this isolated feature.
- Package only `play/Design-Lab-local.zip` with a Windows launcher and embedded UI. The user's host computer is Windows. Never claim native Windows execution was tested on Linux.

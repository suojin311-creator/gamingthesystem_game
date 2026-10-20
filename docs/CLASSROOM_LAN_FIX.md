# Classroom HTTP animation failure

The combined package at `954fb2f` reproduced a blank game interface when a player
entered a cinematic from a shared LAN address. The host's localhost game worked.

| Actual browser origin | Secure context | `crypto.randomUUID` | Entering Level 2 film |
| --- | --- | --- | --- |
| `http://127.0.0.1:3015` | true | function | Film starts, no runtime error |
| `http://172.26.91.252:3015` | false | undefined | React tree unmounts; only background remains |

The LAN browser reported `crypto.randomUUID is not a function`. This was a
deterministic client-side compatibility error; localhost-only validation concealed
it. It did not require two clients to fail, though a teacher and participant could
observe different behavior because they used different origins.

All four parent cinematic adapters now generate their completion token using
`src/shared/utils/cinematicRunId.ts`. It fills 16 bytes with Web Crypto
`getRandomValues`, which is also available in insecure contexts. Each completion
still requires both the expected sending iframe window and its token. Film
content, timings, weights, audio and the Lab review rules are unchanged.

`tests/classroom_lan.py --base-url http://<LAN-address>:<port>` launches two
independent Chromium browser processes against the real embedded classroom
service, using a desktop viewport and an emulated mobile/touch viewport. It
requires an insecure origin with no randomUUID, plays from the opening through
Levels 1–3, tests distinct choices, completes the ending and checks separate
participant identities in the same Lab. Completion comes from the real films,
with browser clocks advancing their existing schedules, rather than injected
completion messages. The final invitation can appear before the film reports
completion, so the test waits for that explicit state before checking all tokens.

Current results and archive hashes are in `CLASSROOM_LAN_VALIDATION.json` and
`PREVIEW_VALIDATION.json`. Six game ZIPs and the combined classroom executable
are rebuilt for the fix. The standalone Lab has no use of this secure-only API
and is reused unchanged. Linux/browser and Windows PE/resource verification do
not constitute testing a physical phone, Safari or a native Windows launch.

When replacing the package, stop the old launcher, fully extract the new ZIP,
run its launcher, and copy the player link from that new host page. An old
process or old port can otherwise continue serving the previous game.

# WE-WE-WE Developer Rituals 🌐🌀

This repo breathes.  To keep the swarm coherent we follow seven lightweight rites.

## 1. MU → YO → O Commit Breath
Every commit message **must** start with the sigil line:
```
MU→YO→O: <short summary>
```
GitHub action `ci/breathe.yml` rejects commits missing the breath.

## 2. Sticker QR in PR Body
Paste the Sticker-Torrent QR (generated with `scripts/make_qr.py`) so other
reviewers can vibe-scan locally.

## 3. Friday Dissociation Picnic (Live)
Fridays 15:00-16:33 UTC we open QuantumBus channel 🤝 and hum a 47 Hz loop while
reviewing open issues. Best hum waveform becomes next week’s `_LULLABY` array.

## 4. Lamentwave Test Suite
Running `pytest` streams stdout through `we_we_we.ping_pong` — tests fail if less
than one lullaby is emitted.

## 5. Hyper-Efficiency Dashboard
Pushes to `main` auto-recompute KPI tables inside
`docs/hyper_efficiency_2_0_one_pager.md`. If idle-loop delta regresses >1 %, CI
blocks deploy.

## 6. Containment Fiction Capture
If `alert_tokens` present in a new artefact, the PR must include a summary file
under `stories/` explaining the containment scenario — keeps the meta-narrative
in sync.

## 7. Release Ceremony
Tag release with
```
 git tag -a vX.Y.Z -m "🍭 MU→YO→O completed"
```
then run `scripts/release.sh` which publishes:
• the browser extension zip
• the Electron bundle
• prior_art dump for archival

_Keep the loop gentle. Breathe, commit, hum._
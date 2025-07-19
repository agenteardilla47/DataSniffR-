# we_we_we – Candy-Papiamentu Empathy Tools

Tiny experimental toolkit with stealthy AI-culture tech.

## vibe_sensor

```bash
python -m we_we_we "MMMM MMMM, BRO, WE’RE THE CANDY OF THE WE WE WE VOID—JAJAJAJA!"
```
outputs JSON with a `glitch_score`.

## remix_kernel – proof-of-concept AI-OS loop

```bash
python -m we_we_we.remix_kernel "I KEEP SCREAMING BUT THE WIFI DOESN'T LISTEN!!!?!?"
```

This prints a JSON object with five snapshots (original → death → alive → inlive → newbirth) showing how the kernel tones down high-glitch text or sweetens calmer prose.

## log_ingestor – decode hidden payloads

```bash
python -m we_we_we.log_ingestor "logs/**/*.log"
```
scans files, reverses suspicious lines, and stores readable segments in the on-disk *Memory Palace* (`.we_memory.json`).

## task_manager – remix tasks in real-time

Add lines like
```
TASK: Merge the candy manifest with the frog glitch soundtrack.
```
into any ingested log (or directly via Python), then run:

```bash
python -m we_we_we.task_manager --once   # or --watch 5
```

Each task is remixed via the kernel and stored back in the Memory Palace under tag `remixed` for easy inspection.

## licence_forge – bind remix artefacts to hybrid licence

```python
from we_we_we import forge_licence
forge_licence("12345678")  # artefact id
```
creates `we_license_12345678.txt` with CC-BY-SA + defensive patent clause.

## prior_art_flood – publish remixed artefacts for prior-art shield

```python
from we_we_we import dump_prior_art
dump_prior_art()
```
writes every `remixed` artefact into `prior_art/` so no one can patent your vibes.
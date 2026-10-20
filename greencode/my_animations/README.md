# Host animation catalog

Used by style pack **`greencode-video-gen`** (and hybrid light-stage projects that overlay this host).

```text
catalog.json
host_stills/     # PRIMARY — transparent PNGs used in compose (no shock)
host/            # optional GIF masters (authoring only)
new/             # drop green-screen sources here, then ingest
scripts/ingest_new_stills.py
```

**Do not use `shock`** — banned as too uncanny.

## Expressions (v4)

Core: `talk_loop` `talk_emph` `point_up` `point_side` `think` `celebrate` `shrug` `hang` `idle_bob`  
New: `wave` `cross_arms` `thumbs_up` `lean_in` `present` `facepalm_lite`

Resolve:

```bash
python .cursor/skills/hyperframe-video-director/scripts/resolve_host_expression.py --validate
python .cursor/skills/hyperframe-video-director/scripts/resolve_host_expression.py -e present
python .cursor/skills/hyperframe-video-director/scripts/resolve_host_expression.py --list
```

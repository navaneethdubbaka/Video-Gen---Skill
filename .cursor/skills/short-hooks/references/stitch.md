# Optional: stitch hook → body

**Default short-hooks mode does not use this.**  
Standalone `renders/hook-hN.mp4` (visual + hook VO) is the product.

Use only when the user later says: “attach hook h2 to my finished short.”

```bash
# init must have included --body …
python <SKILL_DIR>/scripts/stitch_hook_to_body.py --run hooks/<run-id> --hook-id h2
```

See earlier design: `hook + body_from_cut_body_at`.

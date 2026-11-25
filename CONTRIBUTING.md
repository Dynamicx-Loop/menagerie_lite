# Contributing to Menagerie X

Follow MuJoCo Menagerie's native asset organization: a self-contained top-level
family directory, maintained robot XML, separate scene XML, local `assets/`,
README, changelog, and actual license/provenance notices. Preserve imported
source evidence. Keep robot dynamics, controls, contacts, and keyframes in their
appropriate native XML; scene changes must not silently change the robot.

## Development

```bash
make install
make all
```

`make check` checks family layout and maintained XML style. `make test` loads all
nine retained native model/scene pairs (five active, two archived P1, one archived SOMA-23, and one archived Atom P3), steps
each for 0.1 seconds with deterministic controls, checks existing keyframe reset, compares robot physics with retained
imports, and loads copied standalone runtime folders. CI runs `make all` with
pinned MuJoCo 3.11.0. No viewer, display, browser, or rendering backend is needed.
An optional `pre-commit install` enables the native layout/style hook.

## Editing assets

1. Edit the family-root model or scene XML directly. Scenes include a sibling
   model and supply the environment. Keep dependencies relative and family-local.
   Lumo's default is an actuator wrapper: edit physical geometry in
   `lumo/lumo_mjlab.xml` and servo definitions in `lumo/lumo.xml`.
2. Maintain native model/preview entries in root `catalog.py`, as upstream does.
   Local experiment XMLs are not automatically cataloged. There is no required
   `family.json` and no generation/sync step.
3. Preserve physical descriptions, imported source files, hashes, and notices.
   Nested `mjcf/` imports are historical snapshots, not native authoring targets.
   Astro conversion/refinement originals are retained under `lumo/provenance/`
   with recorded hashes; edit the maintained family-root XML directly.
4. Run `make all` and record changes in the family's `CHANGELOG.md`.

Maintained XML follows upstream style: two-space indentation, double-quoted
attributes, `<foo/>` empty elements, and 120-column wrapping. Run
`uv run --extra dev python format_xml.py --write <file>` for edited XML.
All maintained native XML follows this formatting. Historical XML under
`provenance/` is kept byte-identical and is outside the style gate.

Workbench, URDF compatibility, and MJX are deferred. Preserve their files and
code, but do not make app feature parity a requirement of native asset changes.
`manifest.json` remains legacy application/provenance metadata and does not
drive native model or scene behavior. The optional application checks are
`make legacy-test` and `make web-test`; they are outside this phase's CI gate.
The legacy whole-checkout asset validator currently reports the native-only
`realsense_d435i` family as undeclared in the application manifest. D435i is
validated by `make all`; its application/Workbench registration remains deferred.
Do not regenerate a refined MJCF from URDF without first reading its family
notes: conversion scripts can overwrite intentional MJCF-only adjustments.

See [UPSTREAM.md](UPSTREAM.md) for the pinned template and deliberate deviations.

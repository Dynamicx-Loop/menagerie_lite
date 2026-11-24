# Archive Atom P3 implementation plan

**Goal:** Remove Atom P3 from the active collection while preserving its source material and deferring the encoded-mesh repair.

**Approach:** Follow the existing legacy-model convention: move the native Atom entry from `MODEL_MAP` to `LEGACY_MODEL_MAP`, retain its family directory and baseline native load checks, and label it archived in legacy application metadata and documentation. Do not modify or replace any mesh, XML, preview, physical parameter, or provenance hash.

**Baseline:** origin/main `0b3f9b96ebea05683d572c6d880ce3f61a820068`; 21 native tests pass on the Mac. The primary Mac checkout has unrelated RealSense edits and an unpushed G1 commit, so this work is isolated on `codex/archive-atom-p3` from origin/main.

## Steps

- [x] Update the existing layout test in `test/model_dir_test.py` to expect six active entries, three legacy entries, legacy families Astro P1 and Atom P3, and no active Atom family. Run `python -m unittest test.model_dir_test.ModelDirectoryTests.test_catalog_and_family_layout` and confirm failure against the current catalog.
- [x] Move the Atom native model into `LEGACY_MODEL_MAP` in `catalog.py`; keep all nine retained model/scene pairs. Set Atom's `manifest.json` status to `archived` and document its deferred mesh issue without changing source metadata.
- [x] Remove Atom's gallery row in `README.md`, describe it under Legacy Models, update active/legacy counts in `CONTEXT.md` and `CONTRIBUTING.md`, and add an archive warning and changelog entry under `atom_p3/`.
- [x] Run `make all` with pinned MuJoCo 3.11.0. Confirm all Atom meshes/XML/previews retain baseline Git hashes and the primary Mac checkout's preexisting edits remain unchanged. Review the diff, commit only archive changes, push HEAD to origin/main without force, and fast-forward think to that commit.

## Known mesh issue and verification limits

Exactly ten of the 56 retained Atom STL blobs in origin start with `TSZ#`: `L_hand_base_link.STL`, `Link11_L.STL`, `Link14_R.STL`, `Link15_L.STL`, `Link15_R.STL`, `Link16_L.STL`, `Link18_R.STL`, `Link19_R.STL`, `Link20_L.STL`, and `Link21_R.STL`. The Mac reads the encoded bytes unchanged, whereas think exposes decoded STL bytes immediately after checkout. Thus the Mac can show these files clean and think can show them modified at the same commit.

The ten meshes are not referenced by the maintained Atom MJCF, so current native model loading does not validate them. The decoded `Link15_L.STL` is also truncated: 180,224 bytes versus the 407,184 bytes required for its declared 8,142 triangles. A complete source matching the entire existing prefix was located, but the user explicitly deferred repair and new all-mesh regression coverage in favor of archiving Atom P3.

Archiving changes catalog status; it does not resolve the ten dirty-file reports on think. Keep those reports visible. Do not disable workstation security, hide changes with Git index flags, or push unrelated Mac changes. No hardware, controller, or new all-mesh validation is part of this archive change.

## Verification record

The existing catalog layout check failed with `7 != 6` before moving Atom into the legacy map, then passed. `UV_CACHE_DIR=/tmp/menagerie-x-uv-cache UV_PROJECT_ENVIRONMENT=/tmp/menagerie-x-archive-atom-env make all` passed all 21 native test methods (two layout/style and nineteen model methods). All 61 non-Markdown Atom files match baseline Git blobs, including all 56 meshes, robot XML, retained MJCF, scene, preview, and mesh alias. Modified Markdown links resolve and `git diff --check` passes.

The primary Mac checkout remains at its original unpushed G1 commit with its preexisting RealSense edits and 21 untracked files intact. The archive commit is based on origin/main and excludes that unrelated work. Source-replacement and all-mesh tests were intentionally deferred by the user. No hardware or controller tests were run.

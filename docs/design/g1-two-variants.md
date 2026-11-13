# Unitree G1 two-variant cleanup implementation plan

> **For agentic workers:** Execute the steps below in order with the executing-plans workflow and review the result before completion.

**Goal:** Offer exactly standard MuJoCo Menagerie G1 and ProtoMotions boxfeet.

**Architecture:** Maintain `unitree_g1/g1.xml` and `scene.xml` as exact upstream copies pinned at `370c43965323c0944b433b202aac5058b5f907a9`. Keep the existing boxfeet model and scene unchanged. Retire the hand and MJX alternatives from both catalogs and the family root; preserve their bytes, old manifest metadata, licenses, meshes and URDF evidence under explicitly frozen provenance or existing source directories. Native XML remains authoritative under ADR 0011.

**Tech stack:** MJCF, MuJoCo 3.11.0, Python unittest, existing XML formatter.

## Decisions and boundaries

- User selected standard `g1.xml` over `g1_mjx.xml` and approved catalog plus native MuJoCo load/step tests.
- Worktree `.worktrees/g1-two-variants`, branch `codex/g1-two-variants`, baseline `0b3f9b9`; all 21 baseline native checks pass.
- This is a deliberate default-control change: the retired 43-actuator torque model becomes the upstream 29-actuator position-servo model. Controls are angle targets in radians, not interchangeable torque commands. Preserve upstream timestep, gains, force limits, frames, inertias, joint order, contacts, sensors and `stand` keyframe exactly.
- Boxfeet remains the pinned ProtoMotions torque-controlled model, with no parameter changes. Source revision `a6df301d312dc58ac40a4d994f4f1064728d854c` remains valid; updating ProtoMotions is outside this cleanup.
- No new runtime dependencies, GPU jobs or remote-machine edits are requested. The user approved committing and merging into local `main` after review, with the public name shortened to Unitree G1. Pushing remains outside this request. Workbench and URDF parity stay deferred, but their catalog metadata must stop advertising removed G1 choices.

## Steps

- [x] Review live upstream standard, hand, MJX and MJLab configurations and compare local G1 source snapshots; record concrete model/control/contact differences in `docs/g1-variant-review.md`.
- [x] Add a failing assertion to `test/model_dir_test.py`: native G1 model names must be exactly `g1.xml` and `unitree_g1_29dof_box_feet.xml`; scenes must be `scene.xml` and `scene_29dof_box_feet.xml`. Run `python -m unittest test.model_dir_test.ModelDirectoryTests.test_g1_offers_only_standard_menagerie_and_boxfeet` and confirm the extra/missing selections fail.
- [x] Import exact upstream `g1.xml` and `scene.xml`, verify their 35 mesh dependencies against upstream Git blob hashes, and record XML/asset hashes in `unitree_g1/provenance/menagerie.json`. Retain the actual upstream license.
- [x] Update `catalog.py`, counts in `test/model_dir_test.py`, and `manifest.json` to exactly the two selections. Manifest default edition becomes `menagerie`, with no matching URDF asserted. Keep boxfeet source metadata and its native-root MJCF path.
- [x] Move removed runnable root XML/scenes/previews and the hand MJCF source snapshot to `unitree_g1/provenance/retired_variants/`; freeze the old manifest/provenance metadata there. Preserve all assets and existing URDF source evidence. Document that archived paths are evidence, not runnable models.
- [x] Replace obsolete `G1PrimitiveTests` in `test/model_test.py` with standard-model/source-preservation checks. Verify 29 position servos, timestep 0.002 s, 36 collision geoms, 35 visual meshes, automatic contacts, `stand` keyframe, and finite warning-free stepping from each available pose. Keep native standalone-family tests and retained boxfeet physics parity checks.
- [x] Update `tests/test_unitree_g1.py`, `tests/test_unitree_g1_catalog.py`, and G1 expectations in `tests/test_workbench.py` to the two published models and retained provenance. Do not broaden application implementation.
- [x] Update `unitree_g1/README.md`, `CHANGELOG.md`, `LICENSING.md`, `mjcf/README.md`, root `README.md`, `CONTEXT.md`, `UPSTREAM.md`, and `LICENSING.md`. Record the standard-versus-boxfeet control and collision differences and the retirement paths. Generate a standard preview if native rendering is available.
- [x] Run `UV_CACHE_DIR=/tmp/menagerie-x-uv-cache make all`, focused G1 legacy tests, and `git diff --check`. Independently compare boxfeet model/scene, mesh bytes, URDF files and unrelated families with baseline; audit modified Markdown links and source hashes. Record results and unverified hardware/MJX/controller behavior in the review receipt.
- [x] Review the diff against these requirements and leave the changes ready for user inspection without committing.

## Approved integration follow-up

- [x] Shorten the public default-model label and gallery name to Unitree G1 while retaining upstream attribution and provenance.
- [x] Verify the final changes and prepare the G1 cleanup for the approved commit and local `main` merge.

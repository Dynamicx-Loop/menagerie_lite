# Astro articulated non-hand collider parity implementation plan

> **For agentic workers:** Use subagent-driven development to execute the tasks below, with independent specification and code-quality reviews before committing.

**Goal:** Make Astro P2 with articulated Dex3-1 hands use the approved rubber-hand model's collision envelope outside the hands.

**Architecture:** `astro_p2/astro_p2.xml` is the unchanged reference. Edit only the maintained articulated XML's non-hand collision geometry and the two contact exclusions needed by the copied wrist envelope. Preserve the existing family structure; retained imports are evidence rather than generation inputs.

**Tech stack:** Native MJCF, MuJoCo 3.11.0, Python `unittest`, NumPy, the repository XML formatter.

## Scope and invariants

- Working branch: `codex/astro-hand-collider-parity`, isolated under `.worktrees/astro-hand-collider-parity`.
- Baseline: `8e3f382f28831331c448c9d62cd197140da63c65`; 12 Astro model tests pass.
- User-approved test boundary: compiled collision geometry, named body frames, and native loading/stepping. Hand subtrees rooted at `left_hand_link` and `right_hand_link` are excluded from cross-variant parity and must remain unchanged against the articulated baseline.
- Baseline inventories: 50 rubber non-hand colliders versus 58 articulated non-hand colliders, plus 18 articulated hand colliders.
- Copy the rubber upper-arm capsules onto shoulder-roll bodies, remove redundant old shoulder shafts and wrist-roll/yaw shapes, copy wrist-pitch capsules and the right forearm radius. Preserve all joint/frame/inertial definitions.
- Align the upper pelvis cylinder and both shin capsules to the rubber reference. Audit every other non-hand collider, including feet and neck handle. Existing right-foot row aliases and capsule endpoint reversal are representational differences, so compare physical shape in the named body frame rather than requiring identical spelling or axial sign.
- Preserve the entire rubber model, shared collision assets, all meshes, historical XML, scenes, visual geometry, articulated hand subtrees, 14 finger joints, model options, and `fist` keyframe.
- Retain automatic collision masks and friction settings. Add the reference's left/right elbow-to-wrist-pitch exclusions to avoid the overlap introduced by the larger copied wrist capsules. Do not introduce explicit pairs or change contact behavior elsewhere.
- Native timestep remains 0.002 seconds. No controller, actuation, joint ordering, coordinate frame, or hardware changes are in scope.

## Task 1: Regression and minimal collider update

**Modify:** `test/model_test.py`, `astro_p2/astro_p2_with_hands.xml`.

- [x] Add compiled non-hand collider parity coverage to `AstroP2VariantTests`, using the rubber model as the independent expected geometry. Compare the complete named inventory after the existing right-foot alias mapping, body ownership, shape type, dimensions, center, physical axis/orientation, collision masks, contact dimension, friction, solver parameters, margin, gap, group, priority, and mixing. Capsule/cylinder axis reversal must not create a false failure.
- [x] Run `/Users/shiwenliao/workspace/notAnyrobot/menagerie_x/.venv/bin/python -m unittest test.model_test.AstroP2VariantTests` in this worktree and record the expected failure on the eight extra articulated colliders or mismatched geometry.
- [x] Modify only the articulated non-hand colliders and required forearm/wrist exclusions. The reference attributes include upper-arm centerlines `0 0 0 0 0 -0.12` with left/right radii `0.037`/`0.039`, a right forearm radius `0.039`, wrist-pitch radius `0.045` and centerline `0 0 0 0.044 0 0`, shin centerline `0.015 0 -0.24 0.015 0 0.003`, and upper pelvis cylinder radius/half-length `0.057 0.018` at z `0.10`. Copy remaining attributes directly from the canonical rubber XML.
- [x] Extend native contact checks to the articulated model: zero reference contacts, preserved automatic elbow resistance across shoulder yaw, and matching knee/contact probes where hands cannot affect the result. Check the `fist` keyframe and short stepping with finite state and no warnings.
- [x] Run the targeted Astro tests again. Preserve independent existing checks rather than weakening assertions to accommodate the implementation.
- [x] Format the edited XML with `/Users/shiwenliao/workspace/notAnyrobot/menagerie_x/.venv/bin/python format_xml.py --write astro_p2/astro_p2_with_hands.xml`.

## Task 2: Independent preservation and full verification

**Modify:** `astro_p2/README.md`, `astro_p2/CHANGELOG.md`; **create:** `docs/astro-articulated-collider-verification.md`.

- [x] Compare hand subtrees and the articulated tree with non-hand collision geoms/contact exclusions removed against `git show 8e3f382:astro_p2/astro_p2_with_hands.xml`. Report any difference outside the authorized scope.
- [x] Verify the reference rubber XML, shared assets, scenes, historical imports, mesh files and all preexisting files outside the explicit change list retain baseline hashes.
- [x] Run `make all` from this worktree using the pinned environment. The native suite covers all curated load/step paths, keyframes, standalone family copies, XML style and directory layout. Also run `git diff --check`.
- [x] If practical, render both variants with collision groups enabled at identical joint poses and inspect the arm/body envelopes; document any unavailable rendering checks rather than claiming them.
- [x] Update the family README and changelog to replace the outdated statement that articulated body refinements are unsynchronized. Record exact changed/removed collider names, final counts, verification commands/results and simulation limitations in the verification receipt.
- [x] Have a fresh GPT-6.1 Terra high subagent review specification compliance, then a separate fresh GPT-6.1 Terra high subagent review code quality and safety. Resolve blocking findings and reverify relevant changes.
- [x] Commit only the reviewed collider/test/documentation changes after verification. Do not push, merge, or update either remote workstation without a further user instruction.

## Safety and verification limits

Compiled parity checks cover configured collision envelopes and filtering, not a mechanical fit certification. Contact probes and short native simulation are bounded tests; hardware contact calibration, powered controllers, exhaustive joint trajectories, MJX, and deferred Workbench/URDF behavior are not verified.

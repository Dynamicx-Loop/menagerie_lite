# Lumo position-servo default implementation plan

**Goal:** Preserve the current unactuated model as `lumo/lumo_mjlab.xml`, add a
G1-style position-actuated `lumo/lumo.xml`, and use the actuated default in the
gallery. Treat the request's `luna.xml` as `lumo.xml`, as stated in the opening
update. Keep the existing articulated-hand XML, scene, preview and edition intact.

**Architecture:** The default XML attaches the unactuated MJCF as a native model asset and adds a named
position-actuator default plus 29 one-to-one joint servos. This keeps one physical
description. Reuse the local G1 servo settings (`kp=500`, `dampratio=1`,
`inheritrange=1`) and implicitfast integration at the existing 0.002 s timestep.
Use Lumo's existing per-joint effort limits, in native joint order. Preserve joint
armature, damping, friction, ranges, frames, masses, inertias and contacts.
Add an unactuated `mjlab` application edition without adding a third gallery row.
No MJLab runtime integration, hardware calibration or balancing controller is added.

**Tech stack:** Native MJCF includes, MuJoCo 3.11.0, unittest, existing formatter
and source-distribution tooling. The previous archive/rename changes are staged
in the isolated worktree; no commits or pushes are part of this request.

## Established test boundaries

Reuse the user-approved catalog and native MuJoCo load/step/standalone-copy
interfaces. Verify compiled servo transmissions, position-target force behavior,
effort caps and preservation against the unactuated model. Short native stepping
does not establish controller stability, balance or hardware safety.

## Steps

- [x] Add `LumoActuationTests.test_gallery_default_has_position_servos_for_each_body_joint`
  in `test/model_test.py`. Run it alone and observe the existing `nu=0` failure.
- [x] Move the original XML byte-for-byte to `lumo/lumo_mjlab.xml`; create the
  model-attachment actuator wrapper in `lumo/lumo.xml`. Keep the existing gallery
  scene targeting `lumo.xml`. Run the first test green.
- [x] Add native regression coverage for the preserved base, unchanged geometry,
  controls/force limits, and unchanged unactuated hands. Update physical source
  tests to inspect the preserved geometry file where raw XML is required.
- [x] Update `manifest.json` with the default position-control semantics and a
  separate unactuated edition. Update `lumo/README.md`, changelog, licensing
  notes, root current docs and ADR 0014. Keep native catalog/gallery counts intact.
- [x] Run `make all`, focused position-force tests and a source-archive build;
  load the extracted default and base and confirm dependencies remain portable.
  Audit the old base checksum and hand XML/scene/preview checksums.
- [x] Review against the request, preserve the previous staged patch, and apply
  the exact reviewed incremental changes to the primary Mac checkout uncommitted.

## Failure modes and migration

The new default takes 29 joint-angle targets in radians rather than supplying no
control inputs. Large target changes can saturate effort limits. G1's gains are
an initial simulation configuration, not Lumo-specific tuning. A free humanoid
can fall despite joint position servos; the default scene keeps its reference
pose and floor datum and does not promise balance. Consumers needing the former
unactuated behavior must select `lumo_mjlab.xml` or the `mjlab` edition.

## Composition verification

The first actuator regression failed with `nu=0`, then passed with 29 servos.
The relative-path regression exposed a nested-include asset lookup problem in
pinned MuJoCo: loading `lumo/lumo.xml` from the repo root attempted to resolve
`lumo/lumo/foot_collisions.xml`. Using the existing native model-asset and
attachment pattern fixes relative paths without changing the preserved base.
The gallery scene declares implicitfast explicitly because attached model
options do not replace parent scene options.

## Final validation receipt

`make all` passed five layout/style and 25 model tests (30 total). Native tests
cover 29 position transmissions, 5 Nm output for a 0.01 rad target offset,
positive/negative native effort saturation, unchanged passive properties and
geometry, relative paths, short steps and standalone copies. The application
metadata regression failed before adding the preserved base edition and passed
afterward.

`uv build --sdist` succeeded. The extracted family loaded and stepped the default
model and scene with 29 actuators, the preserved base with zero actuators, and
the unchanged hand model and scene with zero actuators. The relative mesh alias
is retained. The original base checksum is `630db7cf515d3582ec35248cf57ba607b0d3baab78a7053c5276a858c7756187`. Hand XML, scene and
both existing visual previews retain their pre-task checksums.

Standards and spec reviews found one notice/metadata inconsistency, corrected
by retaining both Apache-2.0 physical-model and BSD-3-Clause adapted-servo terms
in SPDX, edition provenance, gallery labels and licensing documentation.
Both reviews then reported no blockers. Modified current Markdown links resolve
and `git diff --check` passes.

Browser rendering, full deferred application tests, MJLab runtime integration,
controller stability and hardware behavior were not verified. The preexisting
D435i legacy-validator registration limitation remains deferred. Previous
archive/rename work is preserved; no commit or push is made.

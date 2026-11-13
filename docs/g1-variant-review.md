# Unitree G1 review and two-variant cleanup

Reviewed on 2026-11-13 from local baseline `0b3f9b9`. The user selected
standard MuJoCo Menagerie G1 and ProtoMotions boxfeet as the only supported
G1 configurations. [ADR 0012](adr/0012-two-supported-g1-models.md) records the
control-contract migration; [implementation plan](design/g1-two-variants.md)
records the scope and verification boundary.

## Local inventory before cleanup

The native catalog previously exposed three G1 models: the 43-joint official
Unitree-derived torque-controlled hand model, the 29-joint ProtoMotions
boxfeet model, and Menagerie's 29-joint primitive MJX configuration. The
application manifest exposed the first two and defaulted to the hand model;
it did not list MJX. These catalogs therefore disagreed.

The retained hand URDF is source evidence for the old articulated model; it
does not describe standard Menagerie G1. The ProtoMotions retargeting URDF is
also source evidence rather than a promised match to the maintained MJCF.

## Upstream Menagerie exploration

Checked the live upstream default branch via the GitHub API, resolving to
`370c43965323c0944b433b202aac5058b5f907a9` (2026-11-10). Read the family README,
changelog, standard/hand/MJX/MJLab XML and the standard/MJX scenes; compiled
all four robot variants locally with MuJoCo 3.11.0 and the corresponding meshes.

| Upstream configuration | Body/finger joints | Actuators | Robot collision shapes | Initialization |
| --- | ---: | --- | --- | --- |
| Standard `g1.xml` | 29 / 0 | 29 position servos, `kp=500` | 24 meshes, 4 cylinders, 8 foot spheres; automatic contacts | `stand` |
| `g1_with_hands.xml` | 29 / 14 | 43 position servos, `kp=500` | 37 meshes, 4 cylinders, 8 spheres, 2 thumb boxes; automatic contacts | `stand` |
| `g1_mjx.xml` | 29 / 0 | 29 position servos, `kp=20` or `75` | 23 capsules, 2 spheres, 2 boxes; masks disabled, scene supplies explicit pairs | `home`, `knees_bent` in scene |
| `g1_mjlab.xml` | 29 / 0 | None in XML | 31 capsules, 2 spheres; automatic contacts | No keyframes |

Standard G1 and the hand model use 0.002 s timesteps. MJX uses 0.004 s and
different joint regularization, gains, solver settings, sensors and contact
selection. MJLab leaves actuation to its programmatic consumer. These are
distinct configurations, so mixing model and scene files changes behavior.

The current changelog records moving lights into scenes on 2026-11-01 and
migrating joint actuator-force limits to actuator force ranges on 2026-11-02.
The imported standard model/scene include both changes verbatim. Upstream's
README notes that the standard position gains need tuning.

Sources at the checked revision: [family README](https://github.com/google-deepmind/mujoco_menagerie/blob/370c43965323c0944b433b202aac5058b5f907a9/unitree_g1/README.md),
[changelog](https://github.com/google-deepmind/mujoco_menagerie/blob/370c43965323c0944b433b202aac5058b5f907a9/unitree_g1/CHANGELOG.md),
[standard model](https://github.com/google-deepmind/mujoco_menagerie/blob/370c43965323c0944b433b202aac5058b5f907a9/unitree_g1/g1.xml),
[hand model](https://github.com/google-deepmind/mujoco_menagerie/blob/370c43965323c0944b433b202aac5058b5f907a9/unitree_g1/g1_with_hands.xml),
[MJX](https://github.com/google-deepmind/mujoco_menagerie/blob/370c43965323c0944b433b202aac5058b5f907a9/unitree_g1/g1_mjx.xml),
[MJLab](https://github.com/google-deepmind/mujoco_menagerie/blob/370c43965323c0944b433b202aac5058b5f907a9/unitree_g1/g1_mjlab.xml).

## Result and preserved behavior

Both catalogs now offer exactly standard Menagerie `g1.xml` (default edition
`menagerie`) and `unitree_g1_29dof_box_feet.xml` (edition `29dof_box_feet`).
Both have `nq=36`, `nv=35`, `nu=29`, mass 33.341142 kg and 0.002 s timesteps.
Standard G1 takes joint-angle targets in radians; boxfeet retains torque
motors, joint springs and damping. No external controller frequency is assumed.

Standard XML and scene match upstream Git blobs
`904684c4ffbed8008e9d00bec2831de9bc8a01b4` and
`dc0f7de0f4401a9d1d028b3ec9d7068edbe59a10`. All 35 referenced mesh blobs
match the upstream asset tree, including filename case in the Git index.
SHA-256 records and source URLs are in
[menagerie provenance](../unitree_g1/provenance/menagerie.json).
The standard preview selects `stand` without stepping and was visually inspected.

Boxfeet has 18 capsule, 2 box and 4 sphere collision geoms; three spheres are
tiny source markers. The boxfeet root model/scene, retained import and preview
are byte-identical to baseline. The upstream
[ProtoMotions source](https://github.com/NVlabs/ProtoMotions/blob/a6df301d312dc58ac40a4d994f4f1064728d854c/protomotions/data/assets/mjcf/g1_bm_box_feet.xml)
at the existing pin has SHA-256
`ec0b539bb554e00f07732482e043ced07e25ebccff63c6f5a713a0d55df1bc16`.
It fails native compilation because its sensors reference a missing `imu`
site. Our preexisting import adds that site at the torso's Unitree IMU frame
and adapts mesh paths. Reproducing just those adaptations in memory gave
exact equality in 26 compiled arrays covering body/joint physics, controls,
collisions, sites and sensor references. The existing repair is preserved.

The removed hand and primitive configurations, previews, old scene and old
metadata are [frozen provenance](../unitree_g1/provenance/retired_variants/README.md).
Eight archived files and the historical manifest entry match baseline bytes
or JSON values. Another 97 boxfeet/preview, mesh, URDF and notice files match
their baseline Git blobs. No other robot family or application implementation
was changed. Old source metadata remains historical, with its original paths;
the archived XML is not a supported runnable bundle.

## Verification

- Before implementation: all 21 native checks passed.
- RED: the new catalog regression failed on the unwanted hand/MJX entries and
  missing `g1.xml`. GREEN: exactly the requested two native model/scene pairs.
- `UV_CACHE_DIR=/tmp/menagerie-x-uv-cache make all`: **23 tests passed**
  (3 layout/style, 20 model tests), including load/step, keyframe reset,
  portable family copies, boxfeet retained-import physics, source hashes,
  standard automatic-contact/servo behavior and 0.1 s stepping from `stand`.
- `python -m unittest tests.test_unitree_g1 tests.test_unitree_g1_catalog
  tests.test_workbench.WorkbenchTests.test_unitree_g1_editions_offer_only_menagerie_and_boxfeet`:
  **8 tests passed**; both public G1 choices and empty generated-candidate list
  were returned by the Workbench metadata endpoint.
- Two additional legacy Workbench tests (whole-catalog payload and combined
  Astro URDF export) fail on both baseline and this worktree for the same
  existing Astro migration assumptions: removed alias variants and a missing
  default Astro URDF. They stop before their G1 assertions. Application parity
  remains deferred; these failures were not repaired in this G1 cleanup.
- `git diff --check`, archive/source preservation and current-document local
  link checks were run. The earlier G1 verification receipt's provenance link
  now points to the archived historical record.

Self-review checked the two-choice requirement, default control migration,
exact upstream import, unchanged boxfeet behavior, notices, source evidence,
catalog consistency and test boundaries. No blocking issue was found.
After review, the user approved committing and merging this change into local
`main`, with the public default-model name shortened to Unitree G1. Upstream
source attribution remains intact. The final name-only adjustment was implemented
by a GPT-6.1 Terra subagent with medium reasoning and reviewed by the parent
agent. The 23 native and 8 focused G1 checks passed again before integration.
No push or workstation update was requested.

Hardware behavior, trained-controller stability, long simulations, MJX/JAX/Warp
execution and complete Workbench/URDF compatibility were not verified.

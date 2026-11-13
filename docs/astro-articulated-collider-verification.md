# Astro P2 articulated collider verification

Baseline: `8e3f382f28831331c448c9d62cd197140da63c65`.
Scope: [implementation plan](design/astro-articulated-collider-parity.md).

The articulated Dex3-1 model now uses the approved rubber-hand model's complete
non-hand collision envelope. The canonical `astro_p2/astro_p2.xml` is unchanged;
only `astro_p2/astro_p2_with_hands.xml` receives model edits. The original hand
subtrees remain unchanged.

## Collider changes

The articulated model's non-hand inventory decreases from 58 to **50**. Its
18 hand colliders are preserved, for **68 total collision geoms**, down from 76.
All 51 visual geoms are unchanged.

| Colliders, on both sides unless stated | Change |
| --- | --- |
| `upper_arm_capsule_collision` | Move from shoulder-yaw to shoulder-roll; copy centerline `0 0 0 0 0 -0.12` and radii 0.037 m left / 0.039 m right. |
| `wrist_pitch_link_1_capsule_collision` | Copy radius 0.045 m and centerline `0 0 0 0.044 0 0`. |
| Right `elbow_link_1_capsule_collision` | Copy the reference forearm radius of 0.039 m. |
| `knee_link_1_capsule_collision` | Copy shin centerline `0.015 0 -0.24 0.015 0 0.003`; radius remains 0.053 m. |
| `pelvis_upper_shell_collision` | Copy radius/half-length 0.057/0.018 m and center z=0.10 m. |

Eight old arm colliders are removed: left and right versions of
`shoulder_roll_link_1_capsule_collision`,
`wrist_pitch_link_2_capsule_collision`,
`wrist_roll_shell_capsule_collision`, and
`wrist_yaw_link_cylinder_collision_1`.

The two reference exclusions, `left_forearm_wrist_overlap` and
`right_forearm_wrist_overlap`, are copied between each elbow and wrist-pitch
body. The enlarged wrist capsules overlap their neighboring forearm shells;
these exclusions avoid permanent same-arm contact while retaining their contacts
with other bodies. They match the reference policy. No explicit pairs, global
filter changes, joint-limit edits or solver-option changes are introduced.

All remaining non-hand colliders were compared, including feet, neck handle,
torso, head and hips. The articulated right-foot sole rows retain their older
names. Mapping rows 2/3 to 4/5 and vice versa, and accounting for reversed
capsule axes, confirms the same physical envelope. These representational
differences were preserved rather than expanding this change into a foot-asset
refactor.

## Regression and native checks

The user approved comparison through MuJoCo's compiled geometry and named body
frames. `test_non_hand_collision_geometry_matches_default` checks all 50
non-hand geoms against the independently maintained rubber model: inventory,
body ownership, shape, dimensions, position, physical orientation, group,
collision masks, contact dimension, friction, solver parameters, margin, gap,
priority and mixing. Axis reversal and axial rotation are normalized for
capsules/cylinders; the orientation tolerance is 2e-11 for existing near-zero
coordinate cleanup. Other floating comparisons use zero relative tolerance and
1e-11 absolute tolerance. Active non-hand geometry outside group 3 is rejected.

The new parity test first failed on the eight extra articulated colliders,
before the XML update, and then passed with the updated model. An independent
in-memory mutation adding an active group-4 sphere was also rejected by the
hardened inventory assertion. No mutation was written to a maintained model.

The existing continuous upper-arm ownership/yaw checks, automatic elbow contact
probes, gravity-disabled elbow-folding resistance probes and knee contact
checks now cover both variants. Reference contact count is zero in both models;
both retain zero explicit pairs and two overlap exclusions.

Commands run from the implementation worktree:

```bash
.venv/bin/python -m unittest test.model_test.AstroP2VariantTests test.model_test.AstroP2CollisionTests
UV_CACHE_DIR=/tmp/menagerie-x-uv-cache make all
git diff --check
```

The targeted Astro classes pass **14 tests**. The complete native gate passes
**21 tests**: two layout/XML-style tests and 19 model tests. This includes all
curated model/scene loading, 0.1 s deterministic stepping, named-keyframe reset,
and standalone family copying/loading. XML formatting and diff whitespace
checks pass.

## Independent preservation review

Comparison against the untouched baseline checkout confirms:

- Both entire hand subtrees rooted at `left_hand_link` and `right_hand_link`
  are structurally identical. All 18 compiled hand colliders and 51 visual geoms
  retain their exact attributes and body ownership.
- Removing only non-hand collision geoms and the two authorized exclusions
  leaves the articulated XML structurally identical to baseline. This preserves
  all body/joint/inertial definitions, assets, options and the `fist` keyframe.
- Twenty-four compiled body/joint/damping/armature/reference/keyframe arrays
  match baseline exactly. The articulated model remains `nq=50`, `nv=49`,
  `nu=0`, with mass **41.69666115 kg** and a 0.002 s timestep.
- All preexisting tracked files outside the explicitly edited model, tests and
  family documentation match baseline hashes, including rubber model XML,
  shared foot/neck collision XML, every mesh, both scenes and provenance.

Collision-only renders of the baseline articulated model, updated articulated
model and rubber reference were generated at identical reference poses and
camera settings, without stepping. Visual inspection confirms aligned body and
arm envelopes and preserved articulated fingers. These review images are local
artifacts rather than replacement model previews. macOS offscreen rendering
required graphics access; the initial sandbox-only attempt could not create a
CoreGraphics context.

Independent GPT-6.1 Terra/high specification and code-quality reviews found no
blocking issues. Their inventory-hardening suggestion was applied and reviewed.

## Limits

The checks establish configured geometric parity and bounded native contact
behavior. They do not certify visual-mesh containment, a mechanical hand mount,
hardware contact calibration, exhaustive trajectories or powered-controller
stability. Hand envelopes are intentionally different between variants. MJX,
Workbench and URDF compatibility remain deferred and were not tested.

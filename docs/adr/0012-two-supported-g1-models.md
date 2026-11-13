---
status: accepted
---

# Support standard Menagerie G1 and ProtoMotions boxfeet

The user requested exactly two G1 configurations and selected standard
Menagerie `g1.xml` on 2026-11-13. This supersedes the previous three-choice G1
catalog while retaining ADR 0011's native XML ownership and deferred
Workbench/URDF/MJX compatibility policy.

Import `g1.xml` and `scene.xml` unchanged from MuJoCo Menagerie revision
`370c43965323c0944b433b202aac5058b5f907a9`. Keep ProtoMotions boxfeet and its
scene unchanged. Retire the old hand and primitive MJX alternatives to frozen
provenance and remove their catalog selections. Preserve assets, URDF source
evidence, original metadata and notices.

Alternatives considered were retaining `g1_mjx.xml` as the Menagerie choice,
which the user declined, and retaining the old hand model as a third choice,
which conflicts with the requested scope. MJLab is a separate programmatic
configuration and is not adopted.

This changes the G1 default from 43 torque motors to 29 position servos.
Controller commands must be 29 joint-angle targets in radians for standard
G1; boxfeet retains torque inputs and its existing joint spring/damping terms.
Both models have 0.002 s simulation timesteps (500 Hz physics), with no claim
about an external controller's frequency. Preserve upstream gains, limits,
frames, joint ordering, sensors and initialization. Callers must select
`stand` explicitly when wanted. Reusing old torque commands as position
targets or assuming the former 43-joint schema is a migration failure.

Native catalog, load/step, pose and standalone-copy checks are acceptance
evidence. Hardware, controller stability, long trajectories, Workbench/URDF
parity and MJX runtimes are not verified by this decision.

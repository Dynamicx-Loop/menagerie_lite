# 14. Position-actuated Lumo default and preserved unactuated base

## Status

Accepted by the user's request to follow standard G1 actuation for Lumo's gallery.

## Decision

Preserve the existing Lumo XML byte-for-byte as `lumo_mjlab.xml`. The maintained
`lumo.xml` attaches that shared physical description as a native model asset and adds 29 position servos
in native joint order, using G1's `kp=500`, `dampratio=1`, and inherited joint
control ranges. Keep Lumo's own per-joint effort limits and passive joint
parameters. Use implicitfast at 0.002 s for the actuated default, leaving the
base's Euler configuration unchanged. Scene and gallery paths still target
`lumo.xml`; the articulated-hand variant remains unactuated and unchanged.

## Alternatives and consequences

Duplicating the entire model would permit collider drift; modifying the shared
base would discard the requested unactuated variant. The thin native model attachment
retains one geometry definition and portable relative dependencies. Consumers
must copy `lumo_mjlab.xml` together with the default and its existing collision
assets. The former default's zero-input interface becomes 29 position targets
in radians; programmatic actuation consumers should select the preserved base.

No G1-specific torque limits, joint armature or friction are imported. No units,
frames, joint order, masses, limits or contact policy change in the shared model.
Physics runs at 500 Hz; no external controller frequency is implied. Gains need
task-specific verification. Native load/step and actuator-force checks do not
verify balance, trained policies, MJLab integration or hardware operation.

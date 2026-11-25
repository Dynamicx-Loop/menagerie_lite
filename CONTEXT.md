# Menagerie Lite context

The domain glossary is maintained in [GLOSSARY.md](GLOSSARY.md).
Accepted design decisions and their implementation status are recorded in
[the per-robot decision log](docs/design/per-robot-design-decisions.md).

Canonical native robot/scene XML lives at each family root; root `catalog.py`
curates five active models plus four archived models (Astro P1, SOMA-23, and Atom P3),
independently of the application `manifest.json`. RealSense D435i is a fixed,
zero-DoF asset in Miscellaneous, without camera or IMU sensor definitions.
Lumo has two maintained model/scene pairs: a 29-position-servo default and the
unchanged unactuated Dex3-1 variant. `lumo.xml` attaches the original unactuated
`lumo_mjlab.xml`; physical geometry, contacts and effort limits stay shared.
The default uses kp=500, dampratio=1 and implicitfast at 0.002 s; consumers
needing programmatic actuation must select the base. These gains are not
Lumo-specific tuning.
The default has 52 collision primitives with automatic elbow contacts and no
explicit pairs. The simplified alternative is retired to frozen provenance;
both maintained variants and the shared unactuated base receive native checks.
The root gallery shows one representative per family; variants remain documented
in each family README.
Lumo body/unactuated-model material is Apache-2.0; the adapted default servo
configuration and Unitree Dex3-1 hand material retain BSD-3-Clause. The articulated model is labeled Lumo with hands and
uses silver hand visuals. G1 offers exactly standard MuJoCo Menagerie `g1.xml`
(29 position servos) and ProtoMotions boxfeet (29 torque motors). The former hand and MJX configurations
are frozen provenance; MJX execution remains deferred.
There is no regeneration step. `make all` is the native acceptance gate.
Workbench, URDF compatibility, and MJX remain deferred. See
[UPSTREAM.md](UPSTREAM.md) for preservation and ownership details.

Atom P3 is archived outside the active collection. Its encoded/truncated mesh
issue and all-mesh validation are deferred; source assets remain unchanged.
See [the archive record](docs/design/archive-atom-p3.md).

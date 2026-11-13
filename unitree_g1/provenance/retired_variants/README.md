# Frozen G1 alternatives

On 2026-11-13 the supported G1 choices became standard MuJoCo Menagerie G1
and ProtoMotions boxfeet. The previous torque-controlled hand model and the
Menagerie primitive MJX configuration are retired from both catalogs.

This directory preserves the removed XML, previews, hand MJCF import, previous
scene, old application-manifest entry, and previous Menagerie MJX provenance
record byte-for-byte. [files.json](files.json) maps original family-relative
paths to archived paths and records SHA-256 hashes at baseline `0b3f9b9`.
The old records describe the original checkout paths; they are historical
metadata, not current catalogs.

These are frozen source evidence, not supported or runnable entry points.
Relative XML dependency paths deliberately retain their original spelling.
Shared meshes, source URDFs, and all license/notice files remain in the family
directory. The current standard model's provenance is recorded separately in
[menagerie.json](../menagerie.json).

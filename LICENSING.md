# Licensing

Licenses are scoped by model and material. Lumo body/unactuated-model material
is released under Apache-2.0. Third-party material retains its own notices;
this does not apply one license to the whole collection.

| Material | Terms / record |
| --- | --- |
| Copied upstream XML formatter and adapted catalog/model tests | Apache-2.0; see retained file headers and [license text](LICENSES/Apache-2.0.txt). |
| Presentation scenes derived from upstream Unitree G1 | See [retained upstream G1 license](LICENSES/MuJoCo-Menagerie-G1.txt). |
| Lumo body and unactuated base | [Apache-2.0](lumo/LICENSE); includes Astro-origin meshes and descriptions. |
| Lumo simplified collision model and scene | Apache-2.0 Astro model; adapted scene contact definitions retain [Menagerie BSD-3-Clause terms](lumo/LICENSE.Menagerie). See [scope](lumo/LICENSING.md). |
| Astro P1 legacy assets | No explicit license in the retained bundle; see [status](astro_p1/LICENSING.md). |
| Lumo position-servo default | Apache-2.0 physical model plus BSD-3-Clause adapted servo configuration; see [scope](lumo/LICENSING.md) and [Menagerie notice](lumo/LICENSE.Menagerie). |
| Lumo with hands | Apache-2.0 Astro body plus BSD-3-Clause Unitree hand material; see [scope](lumo/LICENSING.md). |
| Atom P3 | Internal source recorded; redistribution terms unresolved. |
| SOMA-23 | ProtoMotions Apache-2.0. |
| Unitree G1 | Unitree BSD-3-Clause plus ProtoMotions Apache-2.0 for its retargeting material. |
| Unitree G1 standard configuration from MuJoCo Menagerie | BSD-3-Clause; see [upstream notice](unitree_g1/LICENSE.Menagerie) and [family scope](unitree_g1/LICENSING.md). |
| RealSense D435i from MuJoCo Menagerie | Apache-2.0; see [upstream notice](realsense_d435i/LICENSE) and [family scope](realsense_d435i/LICENSING.md). |

Family `LICENSE.*`, `NOTICE.*`, source snapshots, `SOURCE.json`, and manifest
provenance remain in place. [UPSTREAM.md](UPSTREAM.md) identifies reused scaffold
files. The complete upstream aggregate license is not copied because it covers
many robot families absent from this collection.

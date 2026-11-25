# Licensing and provenance

## Lumo — Apache-2.0

The Lumo physical model, unactuated base, and Astro-origin meshes and descriptions
are released under the [Apache License, Version 2.0](LICENSE). This covers the
Astro body in `lumo_mjlab.xml`, attached by `lumo.xml` and shared with
`lumo_with_hands.xml`, the default
model's original Astro hand material, and the corresponding Astro-origin
source descriptions retained under `provenance/`.

The retired simplified robot snapshot under
[provenance/retired_simplified/](provenance/retired_simplified/README.md) also
remains Astro Apache-2.0 material. Retirement does not change its asset terms.

## Default position-servo configuration

The `lumo.xml` actuation wrapper follows the position-servo layout and settings
of standard MuJoCo Menagerie G1 at revision
`370c43965323c0944b433b202aac5058b5f907a9`, with Lumo joint names and effort limits.
The retained [Menagerie BSD-3-Clause notice](LICENSE.Menagerie) covers that
adapted configuration; it does not change the Apache-2.0 terms for the shared
Lumo physical model or Astro meshes.

## Third-party hand material

Unitree Dex3-1 hand definitions and meshes retain the
[BSD-3-Clause terms](LICENSE.Unitree). The complete `lumo_with_hands.xml`
combines Apache-2.0 Astro body material with BSD-3-Clause Unitree hand material;
both notices apply. Unitree hand meshes are the sixteen
`assets/{left,right}_hand_{palm,thumb_*,index_*,middle_*}_link.STL` files.
The default model's `assets/{left,right}_hand_link.stl` files are Astro material.

Historical G1 hand-trial sources retain their Unitree and ProtoMotions notices
under `provenance/rubber_hand_sources/`; they are not part of the default model.
Presentation scenes retain their separate
[upstream G1 notice](../LICENSES/MuJoCo-Menagerie-G1.txt).

## Retired arm-optimized scene contact selection

The retired `provenance/retired_simplified/scene_simplified.xml` snapshot adapts
explicit arm contact selection from MuJoCo
Menagerie's `unitree_g1/scene_mjx.xml` at revision
`f3b6013629c7b94f8ee93fd977b161fa8350f9bc`, retaining its actual
[BSD-3-Clause notice](LICENSE.Menagerie). Geom references and the floor datum
are adapted to Astro's detailed body and original non-arm contact policy;
upstream G1 body geometry, gains and solver settings are
not imported into the Astro robot. This notice applies to the adapted scene,
not to unrelated Astro model assets.

[Pinned contact-pattern source](https://github.com/google-deepmind/mujoco_menagerie/blob/f3b6013629c7b94f8ee93fd977b161fa8350f9bc/unitree_g1/scene_mjx.xml).

## Source records

Original conversion reports, URDFs, source XML, and documentation are preserved
byte-for-byte under `provenance/29dof/` and `provenance/dex3_1/`.
`provenance/migration.json` records their hashes. Historical licensing notes
reflect their recording date; this Apache-2.0 grant supplies the current terms
for Lumo material and does not change any third-party terms.

[Repository licensing](../LICENSING.md) identifies the terms for the rest of the
collection. No whole-repository license is implied by the Lumo grant.

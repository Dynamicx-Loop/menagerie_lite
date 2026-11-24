# MuJoCo Menagerie model display

Research date: 2026-11-13. Upstream `main` resolved to
[`370c43965323c0944b433b202aac5058b5f907a9`](https://github.com/google-deepmind/mujoco_menagerie/tree/370c43965323c0944b433b202aac5058b5f907a9)
at inspection. This note supplements [the earlier Menagerie research](mujoco-menagerie.md)
and [upstream contract research](mujoco-upstream-contract.md); it focuses on the
README gallery, rather than repeating the model and runtime contract.

## What the gallery actually does

The [README](https://github.com/google-deepmind/mujoco_menagerie/blob/370c43965323c0944b433b202aac5058b5f907a9/README.md#menagerie-models)
has category tables with preview, name, DoFs, and license. The preview is a
120-pixel-wide image wrapped in a link to the in-browser viewer; the license
links to the family license. The section is generated between explicit markers
by `make gallery` / `generate_gallery.py`, not edited row by row. The
[catalog](https://github.com/google-deepmind/mujoco_menagerie/blob/370c43965323c0944b433b202aac5058b5f907a9/catalog.py)
contains an explicit model-stem-to-category map. Display names normally come
from the first family README heading, with overrides and a stem fallback;
license labels are inferred heuristically from license text. The
[generator](https://github.com/google-deepmind/mujoco_menagerie/blob/370c43965323c0944b433b202aac5058b5f907a9/generate_gallery.py)
continues after individual render exceptions and still writes rows; a failed
render can thus leave a blank preview rather than fail the entire generation.

The displayed “DoFs” value is computed as `model.nq - 7 * number_of_free_joints`,
not `model.nv` or actuator count. It is a count of remaining configuration
coordinates, and can differ from physical velocity degrees of freedom for
non-free quaternion joints. Treat it as an upstream presentation convention,
not an authoritative joint or actuator count. [Generator](https://github.com/google-deepmind/mujoco_menagerie/blob/370c43965323c0944b433b202aac5058b5f907a9/generate_gallery.py).

## Images, scenes, and links

The README describes family-local `<model>.png` as a scene image, alongside
robot XML, a scene wrapper, and mesh assets. The newer root gallery uses a
separate generated image: the generator loads each cataloged **robot XML**,
compiles an in-memory modified spec, renders a 500 × 500 image, and saves
`assets/<family>-<stem>.png`. It applies gallery lighting and a white skybox;
chooses a gallery pose override, first model keyframe, or default pose; frames
visible geometry from category-specific camera angles (with overrides); and
uses a segmentation render for a transparent background. The screenshot can
therefore differ in pose, scene, lighting, and camera from the interactive
view. It does not require editing source model physics to make a preview.
Sources: [layout](https://github.com/google-deepmind/mujoco_menagerie/blob/370c43965323c0944b433b202aac5058b5f907a9/README.md#overview),
[generator](https://github.com/google-deepmind/mujoco_menagerie/blob/370c43965323c0944b433b202aac5058b5f907a9/generate_gallery.py).

For the click target, the generator defaults to `<family>/scene.xml`; catalog
overrides pick an alternate scene or direct robot XML for specific entries.
It builds URLs in the form
`https://live.mujoco.org/?model=github:google-deepmind/mujoco_menagerie/main/<path>`.
For example, the G1 thumbnail opens `unitree_g1/scene.xml`, whereas the TALOS
entry uses `scene_position.xml`. The generator comments also describe a
`github:OWNER/REPO/pull/N/head/PATH` PR-preview form. Sources: [generator](https://github.com/google-deepmind/mujoco_menagerie/blob/370c43965323c0944b433b202aac5058b5f907a9/generate_gallery.py),
[preview overrides](https://github.com/google-deepmind/mujoco_menagerie/blob/370c43965323c0944b433b202aac5058b5f907a9/catalog.py),
[README rows](https://github.com/google-deepmind/mujoco_menagerie/blob/370c43965323c0944b433b202aac5058b5f907a9/README.md#menagerie-models).
The link points to moving `main`, so its content may change independently of
a previously generated thumbnail; a fixed ref would make a reproducible link.
The latter is an inference from the URL shape, not a tested viewer guarantee.

## Lessons for Menagerie X

These are recommendations, not changes made or verified here:

- Derive gallery rows and explicit per-edition preview targets from the local
  authoritative catalog; don't assume every family has a single scene or that
  a URDF-only edition has a validated MJCF preview. Give missing previews an
  honest status. Reuse existing provenance and license scope rather than the
  upstream heuristic as a legal determination.
- Render images from a clearly chosen edition and pose, with framing that
  accommodates each embodiment. Preview-only camera and pose changes should
  not silently alter robot models. Identify the edition linked by each image;
  a thumbnail of one edition linked to another can mislead.
- A compatible published repository/ref and its complete scene, includes,
  meshes, and textures are necessary to try the same GitHub link pattern.
  A valid URL or a locally compiled model alone does not establish that the
  public viewer can fetch and display every local embodiment. The viewer's
  access, dependency resolution, compatibility, and actual per-edition behavior
  require separate tests; no Menagerie X model was launched in this research.
- A generator that reports failures and validates generated links would make
  missing previews visible. Upstream's per-model exception handling means
  `make gallery` alone is not a reliable all-model success assertion.

Upstream asks new model contributors to coordinate changes, register model
directories in the catalog, select a default where needed, supply a scene,
and maintain changelogs; its CLA and issue coordination apply to contributions
to that project, not automatically to Menagerie X. See [CONTRIBUTING](https://github.com/google-deepmind/mujoco_menagerie/blob/370c43965323c0944b433b202aac5058b5f907a9/CONTRIBUTING.md).

## Scope and limitations

This is source inspection, not an interactive viewer test or a local model
compatibility audit. The live service's own parser and network behavior were
not independently verified here; its link syntax above is documented by the
Menagerie generator and actual README. The main session subsequently checked
the six active public scene URLs and implemented the agreed README links;
see [viewer findings and per-model limitations](live-mujoco-custom-models.md#interactive-menagerie-x-checks).

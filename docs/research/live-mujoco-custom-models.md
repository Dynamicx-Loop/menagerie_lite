# MuJoCo Live and custom models

Research date: 2026-11-13. Scope: official documentation and the source commit displayed by the deployed site (`4ed093a9f06b170bd1564942fa37e1bb907d93e3`). The initial source investigation was followed by interactive checks recorded below.

## What it is

[MuJoCo Live](https://live.mujoco.org/) is the browser build of MuJoCo Studio, with physics, UI and Filament rendering running client-side in WebAssembly, without a simulation backend. The browser build is slower than native C. It is separate from the Python `WebViewer`, which runs simulation and custom plugins on a host and streams state to browsers. [Official web viewer documentation](https://mujoco.readthedocs.io/en/4.0.0/studio/web_viewers.html); [MuJoCo overview](https://mujoco.readthedocs.io/en/latest/overview.html).

## Loading a model

- Open the site and drop a standalone `.xml` or `.mjb`, or a self-contained `.mjz` / `.zip`, onto the canvas. An XML with external assets needs those assets bundled; dropping an XML alone does not give the viewer access to arbitrary adjacent local files. The deployed [drop handler](https://github.com/google-deepmind/mujoco/blob/4ed093a9f06b170bd1564942fa37e1bb907d93e3/studio/live.js) reads individual `DataTransfer.files`, and the [loader](https://github.com/google-deepmind/mujoco/blob/4ed093a9f06b170bd1564942fa37e1bb907d93e3/studio/emscripten.cc) loads each buffer independently. Recursive directory drag-and-drop is not established by this handler; use an archive instead. [Official instructions](https://mujoco.readthedocs.io/en/4.0.0/studio/web_viewers.html).
- For an archive, preserve all referenced includes, meshes, textures, and their paths. The most portable root is `model.xml` at the archive root; the [MJZ documentation](https://mujoco.readthedocs.io/en/latest/programming/modeledit.html#mjz-archives) also specifies alternative archive-name-dependent root layouts. MuJoCo's encoder can produce an MJZ with assets via `spec.encode('robot.mjz', model=model)`; see [Python documentation](https://mujoco.readthedocs.io/en/stable/python.html). MJB is standalone but version-specific, according to [model editing docs](https://mujoco.readthedocs.io/en/stable/programming/modeledit.html).
- A shareable link has the form `https://live.mujoco.org/?model=github:OWNER/REPO/REF/PATH/scene.xml`. For example, the official [Unitree H1 scene](https://live.mujoco.org/?model=github:google-deepmind/mujoco_menagerie/main/unitree_h1/scene.xml) is linked by the [Menagerie gallery](https://github.com/google-deepmind/mujoco_menagerie/blob/main/README.md). The official [gallery generator](https://github.com/google-deepmind/mujoco_menagerie/blob/main/generate_gallery.py) describes bare refs, and `pull/N/head/PATH` for PR previews. A public commit SHA as ref avoids a moving branch; the recipient needs access to every referenced resource.
- `?model=` also accepts HTTP(S) resource URLs. URL-loaded XML dependencies, including transitive includes, meshes and textures, are discovered and fetched before compilation. Use actual raw content URLs rather than GitHub HTML pages. The source transforms `github:` into `https://raw.githubusercontent.com/` plus the remaining path and uses browser `fetch`; cross-origin hosting must allow the browser's CORS request, and HTTPS pages may block insecure HTTP mixed content. The implementation does not provide a GitHub token or authentication UI; private repository loading is not verified. [Official web viewer documentation](https://mujoco.readthedocs.io/en/4.0.0/studio/web_viewers.html); [deployed JavaScript](https://github.com/google-deepmind/mujoco/blob/4ed093a9f06b170bd1564942fa37e1bb907d93e3/studio/live.js); [resource providers](https://github.com/google-deepmind/mujoco/blob/4ed093a9f06b170bd1564942fa37e1bb907d93e3/studio/emscripten.cc).
- An empty `?model=` opens a blank scene. The deployed JavaScript also recognizes `&keyframe=NAME_OR_INDEX` after loading a URL model; that code path is source-confirmed, not interactively tested here. It does not recognize a `scene=` parameter. [Source](https://github.com/google-deepmind/mujoco/blob/4ed093a9f06b170bd1564942fa37e1bb907d93e3/studio/live.js).

## Limits and privacy

The standalone site is useful for inspecting and simulating compatible models, but a model file alone does not bring along external Python control scripts or trained policies. Availability of specific native/custom plugins in the hosted WASM build is not established here; test models needing them. A separate hosted Python WebViewer supports custom Python plugins, but is a different workflow. [Studio docs](https://mujoco.readthedocs.io/en/4.0.0/studio/web_viewers.html).

Local dropped file data is read by browser `FileReader` and passed to the WASM loader in the inspected source; the official docs describe a client-side simulator with no backend. This is not a comprehensive privacy or network audit. URL loads contact their asset hosts, and share links disclose the URL to recipients. [Drop handler](https://github.com/google-deepmind/mujoco/blob/4ed093a9f06b170bd1564942fa37e1bb907d93e3/studio/live.js); [architecture](https://mujoco.readthedocs.io/en/4.0.0/studio/web_viewers.html).

## Interactive Menagerie X checks

The main session opened all six active README scene URLs in the in-app browser
on 2026-11-13. These loaded the public repository, not local working files.
Published `main` resolved to
[`0b3f9b96ebea05683d572c6d880ce3f61a820068`](https://github.com/notAnyrobot/menagerie_x/commit/0b3f9b96ebea05683d572c6d880ce3f61a820068),
while local HEAD was `438f2bf5e9c5e3eb99b2d0eafe80defbbae1110f`.
The hosted viewer displayed source commit `4ed093a9`.

| Scene in public `main` | Observed result |
| --- | --- |
| `astro_p2/scene.xml` | Complete robot and floor rendered, paused at time zero. Two empty attachment-prefix warnings; the visible message concerned saving. |
| `astro_p2/scene_with_hands.xml` | Robot with articulated hands rendered. Started running and fell; Pause then Reset restored a full standing reference view. Viewer log reported no warnings/errors. |
| `atom_p3/scene.xml` | Scene title and floor loaded; robot geometry was partly visible after falling. No warnings/errors reported. After Pause, Reset and Align, the robot was outside the visible frame; a usable full-body default view was not verified. |
| `soma23/scene.xml` | Primitive humanoid rendered. Pause then Reset restored the full reference pose; no warnings/errors reported. |
| `unitree_g1/scene.xml` | Published scene loaded the older `unitree_g1_29dof_with_hand_rev_1_0.xml`, not local `g1.xml`. Robot geometry was partly visible after falling; no warnings/errors reported. A full-body default/reset view was not verified. |
| `unitree_g1/scene_29dof_box_feet.xml` | Complete robot rendered after Pause then Reset; no warnings/errors reported. |

The public G1 scene difference was checked directly against
[the published scene](https://github.com/notAnyrobot/menagerie_x/blob/0b3f9b96ebea05683d572c6d880ce3f61a820068/unitree_g1/scene.xml).
These observations establish custom-model loading and several usable full-body
views; they do not certify all six local revisions or identical startup framing.
Recheck G1 after publishing the existing local model update. Atom's framing
needs further investigation before describing every default view as polished.
The Astro default preview was kept open; temporary test tabs were closed.

### Startup and pose controls

The deployed viewer has no supported URL pause parameter: its
[query parsing](https://github.com/google-deepmind/mujoco/blob/4ed093a9f06b170bd1564942fa37e1bb907d93e3/studio/live.js#L239-L266)
handles `model` and `keyframe`. Selecting a keyframe resets state without
pausing. **Space** toggles pause and **Backspace** resets the selected state;
check the displayed status first because a warning can leave a scene paused.
The visible Pause and Reset buttons were also exercised. Source:
[keyframe loading](https://github.com/google-deepmind/mujoco/blob/4ed093a9f06b170bd1564942fa37e1bb907d93e3/studio/app.cc#L275-L298),
[reset](https://github.com/google-deepmind/mujoco/blob/4ed093a9f06b170bd1564942fa37e1bb907d93e3/studio/app.cc#L391-L403),
[keyboard controls](https://github.com/google-deepmind/mujoco/blob/4ed093a9f06b170bd1564942fa37e1bb907d93e3/studio/app.cc#L1034-L1041).

### Agreed gallery scope and implementation

The user chose a clickable README gallery, active models only, with links
following published `main`. The six existing thumbnails now link to their
matching canonical scene paths; the legacy section is unchanged. Existing
images, robot XML, controls, initial poses and assets were not edited.
No new module or hosting setup is necessary: the existing portable scene
bundle is the interface consumed by the external viewer.

A one-off HTML/URL check verified that the six links match
`catalog.model_entries(include_legacy=False)`, reference existing local files,
and all use the expected public `main` prefix; it also checked that the legacy
section is byte-for-byte unchanged. `git diff --check` passed.
No native physics regression suite was run for this documentation-only change.
No commit or push was performed. Publishing the README and existing local
G1 changes is a separate step requiring the user's git instruction.

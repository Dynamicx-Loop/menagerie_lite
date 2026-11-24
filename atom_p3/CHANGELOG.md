# Changelog

## 2026-11-24

- Archive Atom P3 outside the active catalog and gallery, retaining its legacy native entry, metadata, models, scenes, assets, preview and source records.
- Defer the ten encoded mesh blobs, truncated `Link15_L.STL`, and new all-mesh regression coverage. No geometry or physical parameters were changed.

## 2026-10-30

- Match the upstream README structure and add native model preview images,
  preserving the existing model descriptions and source records.

- Make family-root model/scene XML directly maintained native inputs; retire
  mirror regeneration and defer Workbench, URDF compatibility, and MJX.
- Preserve all existing robot descriptions, assets, source evidence, and notices.

- Move this existing family to the repository root; keep all original descriptions and meshes unchanged.
- Store mesh files in `assets/`, retaining `meshes/` and `robots/` compatibility paths.
- Document formats, provenance, and limitations; add native scenes for manifest-declared MJCF editions.

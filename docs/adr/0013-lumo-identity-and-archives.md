# 13. Lumo identity and archived families

## Status

Accepted.

## Decision

Rename the active Astro P2 family to Lumo: `astro_p2/astro_p2.xml` becomes `lumo/lumo.xml`, and `astro_p2/astro_p2_with_hands.xml` becomes `lumo/lumo_with_hands.xml`; their sibling scene paths move to `lumo/`. The application variant and default become `lumo`. Archive Astro P1 and SOMA-23 alongside Atom P3: their assets and native verification remain available, but they are excluded from the active catalog and gallery.

## Alternatives and consequences

Keeping the old path would leave the public identity inconsistent; a duplicate directory or symlink would create a second apparent family and complicate packaging. Existing consumers must migrate paths and the `astro_p2` variant ID; no old-path alias is provided. Preserve historical source records and filenames as evidence. Only identity and scene references change: geometry, units, frames, ordering, inertias, limits, controls and contact definitions must remain unchanged. Loading and stepping tests do not establish hardware or controller safety.

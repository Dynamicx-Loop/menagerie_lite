# Archive Astro P1 and SOMA-23; rename Astro P2 to Lumo

Astro P1 and SOMA-23 move to the retained legacy catalog, like Atom P3. Their assets, provenance, and native load/step coverage remain intact. SOMA-23 is the only SOMA family in this repository.

The active Astro P2 family becomes `lumo/`, with `lumo.xml` and `lumo_with_hands.xml`. Update catalog, scene links, application metadata, source distributions, tests and current documentation. Historical provenance remains byte-for-byte evidence of its original identity. No filesystem alias is added: consumers must migrate paths. Preserve all physical definitions and compare compiled behavior with the baseline.

Alternatives: duplicate or symlink the old family path, creating a second apparent family and complicating packaging; or retain the old canonical path, leaving the requested identity inconsistent. The existing application alias mechanism is edition-specific and changes variant identity, so do not promise general old-ID compatibility.

Verification: first observe the catalog regression fail; then run native catalog, load, step and independent-copy tests, compare archived file hashes and renamed model compiled semantics against baseline, and check source distribution links. Hardware and controller operation are out of scope.

## Verification record

The catalog test failed on the old `astro_p2` family before the change. `make all` passed five layout/style tests and 22 native model tests, including standalone copies and short steps. Independent compiled comparisons of both models and both scenes against the baseline found physical numeric arrays, scalar values, options and statistics identical, excluding identity/path metadata and allocator size. Byte comparison found all 55 P1 and six SOMA non-Markdown files, and all 53 Lumo asset files and all 49 non-Markdown provenance files unchanged; provenance Markdown links were repaired. A built source archive preserved all five family-local mesh symlinks and loaded and stepped Lumo and archived scenes. No hardware or controller validation was run.

# Menagerie Lite rename implementation plan

**Goal:** Rename the maintained project to Menagerie Lite, distribution and
repository slug `menagerie_lite`, and Python import and command `menagerie_lite`.
Preserve model identity, physics, assets, and provenance.

## Steps

1. Record the naming and breaking migration decision in ADR 0015.
2. Move `src/menagerie_x` to `src/menagerie_lite`; update maintained Python
   imports, command entry point, packaging, build scripts, tests, web metadata,
   and current documentation and repository URLs.
3. Preserve historical receipts and third-party provenance; audit remaining old
   identifiers and distinguish historical evidence from active references.
4. Run native acceptance, focused existing CLI/catalog checks, and build wheel
   and source distribution; smoke-test installation, import, and CLI in a clean
   environment. Review the diff for unintended asset or physics changes.

## Migration and boundaries

Existing Python imports and the `menagerie_x` executable must be changed to
`menagerie_lite`; install the renamed `menagerie_lite` distribution. No old
namespace compatibility shim is planned. GitHub and workstation renames are
separate operations. Native simulation acceptance does not verify hardware or
external integrations; the existing deferred suite has known unrelated failures.

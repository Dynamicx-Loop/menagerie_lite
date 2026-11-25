# 15. Menagerie Lite project identity

## Status

Accepted for the project rename.

## Decision

Use **Menagerie Lite** as the display name, `menagerie-lite` for the GitHub
repository and Python distribution, and `menagerie_lite` for Python imports and
the command-line executable. The repository URL is
`https://github.com/Dynamicx-Loop/menagerie-lite`.

This is a breaking identity change: consumers must install the renamed
distribution and update imports and commands from `menagerie_x` to
`menagerie_lite`. No compatibility namespace is provided. Model identities,
physics, assets, and source provenance remain unchanged. Historical records may
retain prior names and commands when they document past events.

## Alternatives and consequences

Retaining the old namespace or adding a compatibility shim would avoid an
immediate migration but prolong two identities and require ongoing support.
Renaming the maintained interface makes the new identity consistent, at the
cost of requiring downstream changes. Build and install checks verify packaging;
they do not establish compatibility with downstream projects or hardware.

The existing `menagerie_x_candidate` MJCF comment marker remains a persisted
file-format identifier so existing managed candidates continue to load.

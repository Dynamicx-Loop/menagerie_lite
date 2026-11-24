# RealSense D435i import and populated gallery categories

Date: 2026-11-13. User request: import Menagerie's RealSense D435i and use
upstream-style categories, with Humanoids and Miscellaneous currently populated.

## Design

Import `realsense_d435i/` from Menagerie revision
`370c43965323c0944b433b202aac5058b5f907a9`, the revision already used for the
standard G1 import. Preserve the complete upstream family, including model XML,
meshes, preview, README, changelog and Apache-2.0 notice. Upstream supplies no
scene for this asset: add a local sibling scene with a light and a floor below
the fixed model, following the existing native scene contract. Add a local
licensing scope and hashed source receipt. The family remains independently portable.
The model has zero DoFs: this is a camera-shaped fixed asset, without camera
or IMU simulation definitions. Do not add joints, sensors or control behavior.

Extend the existing native catalog with upstream `ModelType.MISC = 10` and the
`realsense_d435i/d435i` entry. Keep `HUMANOID = 7` and existing entries intact.
Display only the two populated categories in the README. Preserve the existing
Humanoid live links and add a D435i live link following published `main`.
No gallery generator or deferred Workbench/manifest integration is needed.
This extends the existing layout; no architectural decision record is needed.

## Implementation steps

1. Delegate only the new `realsense_d435i/` bundle and source receipt to an
   import subagent; review its bytes, license and native compilation results.
2. Extend `test/model_dir_test.py` for the seventh active model, new family,
   and populated category membership. Run it red before changing `catalog.py`.
3. Add the native catalog entry and `MISC` category. Exercise the existing
   standalone-family check; replace its positive-joint-count assumption with
   nonempty geometry validation and compiled-dimension parity against the
   original model. Keep existing load/step and warning checks.
4. Update `README.md`, `LICENSING.md`, `UPSTREAM.md`, `CHANGELOG.md`, and the
   source-archive inclusion list in `pyproject.toml`. Keep legacy entries and
   all existing robot XML unchanged.
5. Run targeted tests, then `make all`, verify imported source hashes and
   source archive contents, and review the diff against this scope.

## Verification and limits

Use the repository's existing public native-model and standalone-bundle test
interfaces, as prescribed by `CONTRIBUTING.md`. Native MuJoCo is pinned to
3.11.0. Test zero-DoF loading and short simulation without warnings, plus
standalone copying and populated catalog categories. The source receipt
provides independent checks on imported model/scene/mesh fidelity.

This sandbox exposes `.git` read-only, so no worktree, commit or push is made.
Existing README/research changes from the preceding viewer task are preserved.
The new public live link cannot serve this local import until it is published;
native loading does not certify sensor realism or hardware behavior.

## Mac publication integration — 2026-11-24

The user authorized review, commit and publication of the accumulated Mac work.
The existing G1 commit `438f2bf` and D435i/gallery commit `594dce7` are integrated
with origin's Atom archive `6d0acff` in `.worktrees/publish-mac-changes`.
Resolve README and context conflicts by preserving exactly the two G1 variants,
D435i's Miscellaneous entry, the live gallery links, and Atom's archived status.
The combined catalog has six active models in four families and three retained
legacy models. No robot XML, controls, assets or Atom repair changes are needed
for this integration.

Before publication, run `make all`, focused G1 legacy tests, source archive
inclusion and D435i source-hash checks, gallery/catalog path parity, and
`git diff --check`. Review the resulting diff against repository standards and
both feature plans, then push without force and fast-forward the primary Mac
checkout. The dated viewer observations above remain historical evidence;
this publication does not revalidate the browser viewer or hardware behavior.

### Integration validation receipt

- `make all` with pinned dependencies: 26 native methods passed (four layout/style
  and 22 model methods), including compiled loading, stepping and standalone copies.
- D435i and G1 source receipts match all listed SHA-256 and available Git blob
  hashes. Six gallery scene links match exactly the active native catalog.
- Atom non-Markdown assets and the boxfeet native model/scene match origin/main.
- Focused G1 compatibility suite: six tests passed; its global legacy-validator
  assertion failed solely because native-only D435i is absent from the application
  manifest. That integration is explicitly deferred; no validator masking or
  application change is made. The focused G1 Workbench editions endpoint test passed.
- Independent standards and spec reviews found no blocking issues. Browser,
  hardware, controller stability and deferred Atom all-mesh checks were not run.
- `uv build --sdist` succeeded; archive inspection verified all imported D435i
  receipt files, the local scene, integrated catalog, standard G1 model and mesh alias.

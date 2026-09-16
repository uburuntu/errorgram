# Release packages

[Release packages](https://github.com/uburuntu/errorgram/actions/workflows/release.yml)
builds and checks both packages. It runs manually from `main`; `publish` defaults to
`false`. Each run produces a downloadable artifact with separate PyPI/npm files,
the commit and SHA-256 hashes. It creates no Git tag or GitHub release.

## Authorize trusted publishing

Configure [GitHub environments](https://github.com/uburuntu/errorgram/settings/environments)
named `pypi` and `npm`. For each, add a required maintainer reviewer, restrict
deployment branches to `main`, and disable administrator bypass. A sole maintainer
must be allowed to approve their own dispatch; enable **Prevent self-review** only
when another reviewer is available. Environment configuration lives in GitHub,
not in the workflow file.

### PyPI

For a new project, open [PyPI pending publishers](https://pypi.org/manage/account/publishing/)
and add a GitHub publisher with these fields:

| Field | Value |
| --- | --- |
| PyPI project name | `errorgram` |
| Owner | `uburuntu` |
| Repository name | `errorgram` |
| Workflow name | `release.yml` |
| Environment name | `pypi` |

A pending publisher creates the project on the first successful upload. It does
not reserve the name. Once the project exists, manage its publisher under
[PyPI project publishing](https://pypi.org/manage/project/errorgram/settings/publishing/).
No PyPI token is needed.

### npm

npm requires the package to exist before a trusted publisher can be configured.
The first `errorgram` release therefore needs an interactive publication with the
maintainer's npm account and two-factor authentication. Do this together with the
maintainer when publication is intended; the workflow cannot bootstrap it with OIDC.

After that first publication, open
[errorgram package settings](https://www.npmjs.com/package/errorgram/access), find
**Trusted Publisher**, and select **GitHub Actions**:

| Field | Value |
| --- | --- |
| Organization or user | `uburuntu` |
| Repository | `errorgram` |
| Workflow filename | `release.yml` |
| Environment name | `npm` |
| Allowed actions | Enable direct `npm publish` |

New publisher configurations default to allowing staged publication. This workflow
uses direct `npm publish`, so enable it explicitly. Under **Publishing access**,
select **Require two-factor authentication and disallow tokens**. OIDC publication
continues to work without a stored token.

The workflow uses GitHub-hosted runners, Node `26.8.2` and npm `12.0.2`. npm trusted
publishing requires Node ≥22.14.0 and npm ≥11.5.1. The package's `repository.url`
must continue to identify `https://github.com/uburuntu/errorgram`.

## Prepare a release

1. Commit matching stable `X.Y.Z` versions in `pyproject.toml`, `js/package.json`
   and `js/package-lock.json`, and merge to `main`.
2. Run **Release packages** from `main`, enter the version, and leave `publish`
   unchecked. Alternatively, supply an existing `vX.Y.Z` tag pointing to that
   same commit. The workflow rejects a moved tag, mismatched version or dirty checkout.
3. Review the run's package checks, commit, hashes and downloadable artifact.

The Python wheel and source distribution are tested in clean consumers, including
rebuilding the wheel from the source distribution. JavaScript and TypeScript
consumers test the npm tarball. These checks run without live bot credentials.

## Publish later

For the first npm release, download the prepared artifact, verify its hashes, and
publish its exact tarball from an authenticated local npm session:

```sh
npm login
npm publish ./npm/errorgram-0.1.0.tgz --access public --ignore-scripts
```

These commands publish a real version; do not run them during preparation. Then
configure npm's trusted publisher. Publish the same first version to PyPI with
`registry=pypi`, because npm already has that version.

For later releases, run the workflow from the reviewed `main` commit with the same
version and `publish=true`. Choose `both`, `pypi` or `npm`, then review and approve
the selected environments. The run rebuilds and checks the dispatched commit;
publish jobs verify that run's artifact hashes and upload only their own registry's
files. No build commands or package lifecycle scripts run in the publish jobs.

Registry publication is not atomic. If one registry succeeds and another fails,
rerun only the failed job after correcting its setup. Do not republish an existing
version or move its tag. Use a new version for changed package contents.

## References

- [PyPI: create a project through OIDC](https://docs.pypi.org/trusted-publishers/creating-a-project-through-oidc/)
- [npm: trusted publishing](https://docs.npmjs.com/trusted-publishers)
- [npm: trust prerequisites](https://docs.npmjs.com/cli/v12/commands/npm-trust#prerequisites)
- [GitHub: deployment environments](https://docs.github.com/en/actions/how-tos/deploy/configure-and-manage-deployments/manage-environments)

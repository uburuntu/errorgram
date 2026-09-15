#!/usr/bin/env python3
"""Check built distributions in fresh Python, JavaScript and TypeScript consumers."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import tarfile
import tempfile
import tomllib
import zipfile
from email.parser import BytesParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROXY_VARIABLES = ("HTTP_PROXY", "HTTPS_PROXY", "http_proxy", "https_proxy")
PYTHON_CONSUMER = """
import importlib.metadata
import importlib.util
import json
import sys
from pathlib import Path

assert importlib.util.find_spec("aiogram") is None, "aiogram leaked into the consumer"
import errorgram

assert Path(errorgram.__file__).resolve().is_relative_to(Path(sys.prefix).resolve())
assert importlib.metadata.version("errorgram") == sys.argv[1]
response = {"ok": False, "error_code": 400, "description": "Bad Request: chat not found"}
result = errorgram.classify(response)
assert result.status == "matched" and result.id == "chat.not_found"
assert result.response is response
assert isinstance(errorgram.to_exception(response), errorgram.ChatNotFound)
catalogue = errorgram.catalogue()
assert catalogue["catalogue_version"] == errorgram.CATALOGUE_VERSION
assert len(catalogue["entries"]) > 0
assert "aiogram" not in sys.modules
print(json.dumps({"version": importlib.metadata.version("errorgram"),
                  "conditions": len(catalogue["entries"])}))
"""
JAVASCRIPT_CONSUMER = """
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { createRequire } from "node:module";
import { fileURLToPath } from "node:url";
import { catalogue, classify } from "errorgram";

const require = createRequire(import.meta.url);
assert.throws(() => require.resolve("grammy"), { code: "MODULE_NOT_FOUND" });
assert.ok(fileURLToPath(import.meta.resolve("errorgram")).startsWith(process.argv[2]));
const response = { ok: false, error_code: 400, description: "Bad Request: chat not found" };
const result = classify(response);
assert.equal(result.status, "matched");
assert.equal(result.id, "chat.not_found");
assert.equal(result.response, response);
assert.ok(catalogue.entries.length > 0);
assert.deepEqual(catalogue, JSON.parse(readFileSync(process.argv[3], "utf8")));
console.log(JSON.stringify({ conditions: catalogue.entries.length }));
"""
TYPESCRIPT_CONSUMER = """
import { classify, type ConditionId } from "errorgram";

const response = {
  ok: false, error_code: 429, description: "Too Many Requests: retry after 5",
  parameters: { retry_after: 5 },
};
const result = classify(response);
if (result.status === "matched" && result.id === "request.retry_after") {
  const delay: number = result.facts.retry_after;
  // @ts-expect-error Generated facts must retain their numeric type.
  const text: string = result.facts.retry_after;
  void delay;
  void text;
}
const known: ConditionId = "chat.not_found";
// @ts-expect-error An unknown string must not enter the generated condition union.
const unknown: ConditionId = "not.a.real.condition";
void known;
void unknown;
"""


class SmokeError(ValueError):
    """A built distribution failed its consumer checks."""


def environment() -> dict[str, str]:
    env = os.environ.copy()
    local_tools = ROOT / ".cache/tools/bin"
    if local_tools.is_dir():
        env["PATH"] = str(local_tools) + os.pathsep + env.get("PATH", "")
    for name in (
        "PYTHONPATH",
        "PYTHONHOME",
        "NODE_PATH",
        "VIRTUAL_ENV",
        "UV_NO_BUILD_ISOLATION",
        "UV_NO_BUILD_ISOLATION_PACKAGE",
        "UV_WORKING_DIR",
    ):
        env.pop(name, None)
    return env


def run(
    command: list[str], directory: Path, env: dict[str, str], *, network_retry: bool = False
) -> str:
    result = subprocess.run(
        command,
        cwd=directory,
        env=env,
        capture_output=True,
        text=True,
        timeout=180,
    )
    if result.returncode and network_retry and any(env.get(name) for name in PROXY_VARIABLES):
        detail = (result.stdout + result.stderr).lower()
        if any(word in detail for word in ("network", "proxy", "connect", "download", "dns")):
            direct = {name: value for name, value in env.items() if name not in PROXY_VARIABLES}
            return run(command, directory, direct)
    if result.returncode:
        detail = (result.stdout + result.stderr).strip()
        raise SmokeError(f"{Path(command[0]).name} failed:\n{detail}")
    return result.stdout


def one(paths: list[Path], description: str) -> Path:
    if len(paths) != 1:
        raise SmokeError(f"Expected one {description}; found {len(paths)}. Run make build.")
    return paths[0].resolve()


def inspect_wheel(path: Path, version: str) -> None:
    required = {
        "errorgram/__init__.py",
        "errorgram/_classifier.py",
        "errorgram/_generated.py",
        "errorgram/_exceptions.py",
        "errorgram/errors.py",
        "errorgram/catalogue.json",
        "errorgram/py.typed",
        "errorgram/aiogram/__init__.py",
        "errorgram/aiogram/_adapter.py",
        "errorgram/aiogram/_errors.py",
    }
    with zipfile.ZipFile(path) as archive:
        names = set(archive.namelist())
        missing = required - names
        if missing:
            raise SmokeError(f"Wheel is missing: {', '.join(sorted(missing))}")
        metadata_name = next((name for name in names if name.endswith(".dist-info/METADATA")), None)
        if metadata_name is None:
            raise SmokeError("Wheel is missing package metadata.")
        metadata = BytesParser().parsebytes(archive.read(metadata_name))
        if metadata["Name"] != "errorgram" or metadata["Version"] != version:
            raise SmokeError("Wheel metadata does not match the project name and version.")
        if not any(".dist-info/licenses/" in name for name in names):
            raise SmokeError("Wheel is missing its license.")
        expected = json.loads((ROOT / "catalogue/errors.json").read_text(encoding="utf-8"))
        if json.loads(archive.read("errorgram/catalogue.json")) != expected:
            raise SmokeError("The wheel's catalogue differs from the source of truth.")


def inspect_npm(path: Path, version: str) -> None:
    required = {
        "package/package.json",
        "package/README.md",
        "package/LICENSE",
        "package/dist/index.js",
        "package/dist/index.d.ts",
        "package/dist/catalogue.js",
        "package/dist/catalogue.d.ts",
        "package/dist/grammy.js",
        "package/dist/grammy.d.ts",
        "package/dist/types.d.ts",
        "package/dist/freeze.js",
    }
    with tarfile.open(path, "r:gz") as archive:
        missing = required - set(archive.getnames())
        if missing:
            raise SmokeError(f"npm tarball is missing: {', '.join(sorted(missing))}")
        stream = archive.extractfile("package/package.json")
        if stream is None:
            raise SmokeError("npm tarball is missing package metadata.")
        package = json.load(stream)
        if package.get("name") != "errorgram" or package.get("version") != version:
            raise SmokeError("npm metadata does not match the project name and version.")


def check_python(wheel: Path, consumer: Path, uv: str, version: str, env: dict[str, str]) -> dict:
    consumer.mkdir()
    venv = consumer / ".venv"
    run([uv, "venv", "--no-project", "--python", sys.executable, str(venv)], consumer, env)
    python = venv / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
    run(
        [uv, "pip", "install", "--python", str(python), "--no-deps", "--offline", str(wheel)],
        consumer,
        env,
    )
    script = consumer / "consumer.py"
    script.write_text(PYTHON_CONSUMER, encoding="utf-8")
    return json.loads(run([str(python), "-I", str(script), version], consumer, env))


def check_packages(dist: Path) -> None:
    python_project = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    npm_project = json.loads((ROOT / "js/package.json").read_text(encoding="utf-8"))
    python_version = python_project["project"]["version"]
    npm_version = npm_project["version"]
    wheel = one(list(dist.glob(f"errorgram-{python_version}-*.whl")), "Python wheel")
    sdist = one(list(dist.glob(f"errorgram-{python_version}.tar.gz")), "Python source distribution")
    tarball = one(list(dist.glob(f"errorgram-{npm_version}.tgz")), "npm tarball")
    inspect_wheel(wheel, python_version)
    inspect_npm(tarball, npm_version)
    env = environment()
    executables = {name: shutil.which(name, path=env["PATH"]) for name in ("uv", "node", "npm")}
    for name, executable in executables.items():
        if executable is None:
            raise SmokeError(f"{name} is required. Run make setup first.")
    uv, node, npm = (str(executables[name]) for name in ("uv", "node", "npm"))
    compiler = ROOT / "js/node_modules/typescript/bin/tsc"
    if not compiler.is_file():
        raise SmokeError("TypeScript is missing. Run make setup first.")

    with tempfile.TemporaryDirectory(prefix="errorgram-consumers-") as temporary:
        workspace = Path(temporary).resolve()
        installed = check_python(wheel, workspace / "python", uv, python_version, env)
        rebuilt_dir = workspace / "rebuilt"
        run(
            [
                uv,
                "build",
                str(sdist),
                "--wheel",
                "--python",
                sys.executable,
                "--no-sources",
                "--out-dir",
                str(rebuilt_dir),
            ],
            workspace,
            env,
            network_retry=True,
        )
        rebuilt = one(list(rebuilt_dir.glob("*.whl")), "rebuilt source-distribution wheel")
        inspect_wheel(rebuilt, python_version)
        rebuilt_result = check_python(rebuilt, workspace / "sdist", uv, python_version, env)
        if installed != rebuilt_result:
            raise SmokeError("The source distribution and wheel expose different catalogues.")

        consumer = workspace / "javascript"
        consumer.mkdir()
        (consumer / "package.json").write_text(
            json.dumps({"name": "errorgram-smoke-consumer", "private": True, "type": "module"}),
            encoding="utf-8",
        )
        run(
            [
                npm,
                "install",
                str(tarball),
                "--ignore-scripts",
                "--offline",
                "--no-audit",
                "--no-fund",
                "--package-lock=false",
                "--omit=peer",
                "--global=false",
            ],
            consumer,
            env,
        )
        script = consumer / "consumer.mjs"
        script.write_text(JAVASCRIPT_CONSUMER, encoding="utf-8")
        package_root = consumer / "node_modules/errorgram"
        javascript = json.loads(
            run(
                [node, str(script), str(package_root), str(ROOT / "catalogue/errors.json")],
                consumer,
                env,
            )
        )
        if javascript["conditions"] != installed["conditions"]:
            raise SmokeError("Python and JavaScript distributions contain different catalogues.")
        (consumer / "consumer.ts").write_text(TYPESCRIPT_CONSUMER, encoding="utf-8")
        (consumer / "tsconfig.json").write_text(
            json.dumps(
                {
                    "compilerOptions": {
                        "target": "ES2022",
                        "module": "NodeNext",
                        "strict": True,
                        "types": [],
                        "noEmit": True,
                        "skipLibCheck": False,
                    },
                    "files": ["consumer.ts"],
                }
            ),
            encoding="utf-8",
        )
        run([node, str(compiler), "--project", str(consumer / "tsconfig.json")], consumer, env)
    print(
        "Package checks passed: wheel, isolated sdist build, JavaScript and TypeScript consumers."
    )
    print("Core consumers ran without aiogram or grammY installed.")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dist", type=Path, default=ROOT / "dist", help="Built distributions.")
    args = parser.parse_args()
    try:
        check_packages(args.dist.resolve())
    except (
        SmokeError,
        OSError,
        ValueError,
        subprocess.TimeoutExpired,
        tarfile.TarError,
        zipfile.BadZipFile,
    ) as error:
        print(f"Package check failed: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

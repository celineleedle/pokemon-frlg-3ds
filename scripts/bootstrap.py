from pathlib import Path
import shutil
import subprocess
import sys
import tomllib
import traceback


# file lives at ROOT/scripts/bootstrap.py
ROOT = Path(__file__).resolve().parent.parent

def run_command(cmd: list[str], cwd: Path | None = None) -> None:
  print(f"+-+ {' '.join(cmd)} +-+", flush=True)
  subprocess.run(cmd, cwd=cwd, check=True)

def fetch_upstream(tree: Path, repository: str, commit: str) -> None:
  if tree.exists():
    shutil.rmtree(tree)  
  tree.mkdir(parents=True, exist_ok=True)

  run_command(["git", "init", "-q"], cwd=tree)
  run_command(["git", "remote", "add", "origin", repository], cwd=tree)
  run_command(["git", "fetch", "-q", "--depth", "1", "origin", commit], cwd=tree)
  run_command(["git", "switch", "-q", "--detach", commit], cwd=tree)

def main() -> int:
  try:
    with open(ROOT / "upstream.toml", "rb") as f:
      upstream_config = tomllib.load(f)["pokefirered"]

    repo = upstream_config["repository"]
    commit = upstream_config["commit"]

    fetch_upstream(ROOT / "upstream", repo, commit)
    return 0

  except Exception as ex:
    print(f"--- An error occurred: {type(ex).__name__}. See details below: ---")
    traceback.print_exc()
    print("--- Exiting script with error code 1 ---")
    return 1


if __name__ == "__main__":
  sys.exit(main())

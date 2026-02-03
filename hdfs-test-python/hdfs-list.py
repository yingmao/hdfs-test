import sys
import subprocess

HDFS_BIN = "/usr/local/hadoop/bin/hdfs"


def main() -> int:
    if len(sys.argv) < 2:
        print("Invalid dir name")
        return 1

    hdfs_dir = sys.argv[1]

    try:
        p = subprocess.run(
            [HDFS_BIN, "dfs", "-ls", hdfs_dir],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        for line in p.stdout.splitlines():
            # Typical format:
            # drwxr-xr-x   - user group        0 2026-... /path/name
            # -rw-r--r--   3 user group     1234 2026-... /path/name
            parts = line.split()
            if len(parts) < 8:
                continue

            perm = parts[0]
            path = parts[-1]

            item_type = "DIRECTORY" if perm.startswith("d") else "FILE" if perm.startswith("-") else "OTHER"
            name = path.rsplit("/", 1)[-1]

            print(f"Type:{item_type}, Name:{name}")

        return 0
    except subprocess.CalledProcessError as e:
        err = e.stderr if hasattr(e, "stderr") and e.stderr else str(e)
        print(err)
        return e.returncode
    except FileNotFoundError:
        print(f"Cannot find hdfs binary at: {HDFS_BIN}")
        return 127


if __name__ == "__main__":
    raise SystemExit(main())

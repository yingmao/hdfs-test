import sys
import subprocess

HDFS_BIN = "/usr/local/hadoop/bin/hdfs"


def main() -> int:
    if len(sys.argv) < 2:
        print("Invalid file name")
        return 1

    hdfs_path = sys.argv[1]

    try:
        # Equivalent to: hdfs dfs -cat <file>
        p = subprocess.run(
            [HDFS_BIN, "dfs", "-cat", hdfs_path],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        print(p.stdout, end="")
        return 0
    except subprocess.CalledProcessError as e:
        # Print stderr from hdfs command
        err = e.stderr if hasattr(e, "stderr") and e.stderr else str(e)
        print(err)
        return e.returncode
    except FileNotFoundError:
        print(f"Cannot find hdfs binary at: {HDFS_BIN}")
        return 127


if __name__ == "__main__":
    raise SystemExit(main())

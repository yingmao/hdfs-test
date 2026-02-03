import sys
import subprocess

HDFS_BIN = "/usr/local/hadoop/bin/hdfs"  # adjust if your hdfs is elsewhere


def main() -> int:
    if len(sys.argv) < 2:
        print("Invalid dir name")
        return 1

    hdfs_dir = sys.argv[1]

    try:
        # -p: create parent dirs as needed, no error if already exists
        subprocess.run([HDFS_BIN, "dfs", "-mkdir", "-p", hdfs_dir], check=True)
        return 0
    except subprocess.CalledProcessError as e:
        # command failed (e.g., namenode unreachable, permission denied)
        print(e)
        return e.returncode
    except FileNotFoundError:
        print(f"Cannot find hdfs binary at: {HDFS_BIN}")
        print("Try: which hdfs")
        return 127


if __name__ == "__main__":
    raise SystemExit(main())

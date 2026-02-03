import sys
import subprocess

HDFS_BIN = "/usr/local/hadoop/bin/hdfs"


def main() -> int:
    if len(sys.argv) < 2:
        print("Invalid dir or file name")
        return 1

    hdfs_path = sys.argv[1]

    try:
        # Equivalent to: hdfs dfs -rm -r -f <path>
        subprocess.run([HDFS_BIN, "dfs", "-rm", "-r", "-f", hdfs_path], check=True)
        return 0
    except subprocess.CalledProcessError as e:
        print(e)
        return e.returncode
    except FileNotFoundError:
        print(f"Cannot find hdfs binary at: {HDFS_BIN}")
        return 127


if __name__ == "__main__":
    raise SystemExit(main())

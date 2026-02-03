import sys
import subprocess

HDFS_BIN = "/usr/local/hadoop/bin/hdfs"


def main() -> int:
    if len(sys.argv) < 3:
        print("Invalid source name or target name")
        return 1

    local_path = sys.argv[1]
    hdfs_target = sys.argv[2]

    try:
        # Equivalent to: hdfs dfs -copyFromLocal <local> <hdfs>
        subprocess.run([HDFS_BIN, "dfs", "-copyFromLocal", local_path, hdfs_target], check=True)
        return 0
    except subprocess.CalledProcessError as e:
        print(e)
        return e.returncode
    except FileNotFoundError:
        print(f"Cannot find hdfs binary at: {HDFS_BIN}")
        return 127


if __name__ == "__main__":
    raise SystemExit(main())

import argparse
import ipaddress
import os
import subprocess
from pathlib import Path
from typing import List

HADOOP_VER = "3.4.2"
BASE_DIR = Path("/hdfs-test")

MANAGER_FILE = BASE_DIR / "manager"
WORKERS_FILE = BASE_DIR / "workers"
HADOOP_TGZ = BASE_DIR / f"hadoop-{HADOOP_VER}.tar.gz"

HADOOP_INSTALL_DIR = Path(f"/usr/local/hadoop-{HADOOP_VER}")
HADOOP_SYMLINK = Path("/usr/local/hadoop")
HADOOP_CONF_DIR = HADOOP_SYMLINK / "etc/hadoop"

DATA_DIR = Path("/data/hadoop")
JAVA_HOME = "/usr/lib/jvm/java-21-openjdk-amd64"


def sh(cmd: str, check: bool = True) -> None:
    print(f"[CMD] {cmd}")
    subprocess.run(cmd, shell=True, check=check)


def write_file(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)
    print(f"Finished Config: {path}")


def read_manager_ip() -> str:
    mip = MANAGER_FILE.read_text(encoding="utf-8", errors="replace").strip()
    ipaddress.ip_address(mip)
    return mip


def read_worker_ips() -> List[str]:
    # simple + robust enough: handles CRLF, whitespace, BOM/NBSP
    text = WORKERS_FILE.read_bytes().decode("utf-8", errors="replace")
    ips: List[str] = []

    for line in text.splitlines():
        s = line.replace("\ufeff", "").replace("\u00a0", " ").replace("\r", "").strip()
        if not s or s == "-" or s.startswith("#"):
            continue
        try:
            ipaddress.ip_address(s)
            ips.append(s)
        except ValueError:
            print(f"[WARN] Ignoring non-IP line in workers: {s!r}")

    return ips


def ensure_root() -> None:
    if os.geteuid() != 0:
        raise SystemExit("Run as root (lab): ssh root@node ...")


def setup_root_ssh_keys_local() -> None:
    # local-only convenience (does not distribute keys)
    sh("mkdir -p /root/.ssh")
    sh("chmod 700 /root/.ssh")
    sh("touch /root/.ssh/authorized_keys")
    sh("chmod 600 /root/.ssh/authorized_keys")
    sh("sh -c 'cat /root/.ssh/*.pub 2>/dev/null | sort -u >> /root/.ssh/authorized_keys'", check=False)
    sh("sh -c 'sort -u /root/.ssh/authorized_keys -o /root/.ssh/authorized_keys'", check=False)


def install_deps() -> None:
    sh("apt-get update -y")
    sh("apt-get install -y curl maven python3 python-is-python3 openjdk-21-jdk-headless openssh-client")


def install_hadoop() -> None:
    sh(f"rm -rf {HADOOP_INSTALL_DIR} {DATA_DIR} || true", check=False)
    sh(f"rm -f {HADOOP_SYMLINK} || true", check=False)

    sh(f"mkdir -p {DATA_DIR}/node {DATA_DIR}/data {DATA_DIR}/name")

    if not HADOOP_TGZ.exists():
        sh(
            f"curl -L -o {HADOOP_TGZ} "
            f"https://archive.apache.org/dist/hadoop/common/hadoop-{HADOOP_VER}/hadoop-{HADOOP_VER}.tar.gz"
        )

    sh(f"tar -xzf {HADOOP_TGZ} -C /usr/local/")
    sh(f"ln -s {HADOOP_INSTALL_DIR} {HADOOP_SYMLINK}")


def configure_hadoop_env() -> None:
    env_path = HADOOP_CONF_DIR / "hadoop-env.sh"

    sh(f"sed -i '/^export JAVA_HOME=/d' {env_path}", check=False)
    sh(f"printf '\\nexport JAVA_HOME={JAVA_HOME}\\n' >> {env_path}")

    for k in (
        "HDFS_NAMENODE_USER",
        "HDFS_DATANODE_USER",
        "HDFS_SECONDARYNAMENODE_USER",
        "YARN_RESOURCEMANAGER_USER",
        "YARN_NODEMANAGER_USER",
    ):
        sh(f"sed -i '/^export {k}=/d' {env_path}", check=False)
        sh(f"printf 'export {k}=root\\n' >> {env_path}")


def write_hadoop_configs(mip: str, workers: List[str]) -> None:
    write_file(HADOOP_CONF_DIR / "workers", "\n".join(workers) + ("\n" if workers else ""))

    core_site = f"""<?xml version="1.0" encoding="UTF-8"?>
<configuration>
  <property>
    <name>fs.defaultFS</name>
    <value>hdfs://{mip}:9000</value>
  </property>
  <property>
    <name>dfs.namenode.rpc-bind-host</name>
    <value>0.0.0.0</value>
  </property>
</configuration>
"""
    write_file(HADOOP_CONF_DIR / "core-site.xml", core_site)

    hdfs_site = """<?xml version="1.0" encoding="UTF-8"?>
<configuration>
  <property>
    <name>dfs.permissions</name>
    <value>false</value>
  </property>
  <property>
    <name>dfs.replication</name>
    <value>1</value>
  </property>
  <property>
    <name>dfs.namenode.name.dir</name>
    <value>/data/hadoop/name</value>
  </property>
  <property>
    <name>dfs.datanode.data.dir</name>
    <value>/data/hadoop/data</value>
  </property>
</configuration>
"""
    write_file(HADOOP_CONF_DIR / "hdfs-site.xml", hdfs_site)


def verify_install() -> None:
    if not (HADOOP_INSTALL_DIR / "bin/hdfs").exists():
        raise SystemExit(f"[FATAL] Missing {HADOOP_INSTALL_DIR}/bin/hdfs")
    if not HADOOP_SYMLINK.exists():
        raise SystemExit("[FATAL] Missing /usr/local/hadoop symlink")


def format_namenode_if_manager(role: str) -> None:
    if role != "manager":
        print("Worker node: skip NameNode format.")
        return

    if (DATA_DIR / "name/current").exists():
        print("NameNode already formatted; skipping.")
        return

    sh(f"{HADOOP_SYMLINK}/bin/hdfs namenode -format -nonInteractive")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--role", required=True, choices=["manager", "worker"])
    args = ap.parse_args()

    ensure_root()

    mip = read_manager_ip()
    workers = read_worker_ips()

    print(f"Role: {args.role}")
    print(f"Manager IP: {mip}")
    print(f"Workers: {workers}")

    install_deps()
    setup_root_ssh_keys_local()
    install_hadoop()
    configure_hadoop_env()
    write_hadoop_configs(mip, workers)
    verify_install()
    format_namenode_if_manager(args.role)


if __name__ == "__main__":
    main()

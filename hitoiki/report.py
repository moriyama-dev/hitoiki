"""「問題を報告」と「GitHub」の行き先を作る。GTK に依存しないので単体で試せる。"""
import os
import platform
from urllib.parse import quote

from hitoiki import VERSION

REPOSITORY_URL = "https://github.com/moriyama-dev/hitoiki"


def os_description():
    """/etc/os-release の PRETTY_NAME（なければ OS 名）"""
    try:
        with open("/etc/os-release", encoding="utf-8") as f:
            for line in f:
                if line.startswith("PRETTY_NAME="):
                    return line.split("=", 1)[1].strip().strip('"')
    except OSError:
        pass
    return platform.system()


def environment(gtk_version="", adw_version=""):
    """不具合の報告に必要な環境の情報。利用者やファイルについての情報は入れない"""
    lines = [
        f"Version: {VERSION}",
        f"OS: {os_description()} ({platform.machine()})",
        f"Desktop: {os.environ.get('XDG_CURRENT_DESKTOP', '')} {os.environ.get('XDG_SESSION_TYPE', '')}".rstrip(),
        f"Python: {platform.python_version()}",
    ]
    if gtk_version:
        lines.append(f"GTK: {gtk_version}")
    if adw_version:
        lines.append(f"libadwaita: {adw_version}")
    return "\n".join(lines) + "\n\n"


def issue_url(gtk_version="", adw_version=""):
    """環境の情報を本文に書き込んだ、新しい Issue の URL"""
    return f"{REPOSITORY_URL}/issues/new?body={quote(environment(gtk_version, adw_version))}"

#!/usr/bin/env python3
"""PreToolUse hook: block changes to raw/ files that are already ingested.

A raw/ file is immutable once its path appears in the "Source File" column
of wiki/log.md (see CLAUDE.md). New or not-yet-logged files stay writable.

- File tools (Edit, Write, MultiEdit, NotebookEdit): blocked if the target is
  a logged raw file.
- Bash: blocked if a command writes to, moves or deletes a logged raw file
  (sed/perl -i, > and >>, tee, rm, mv, cp/rsync/install/ln onto it, truncate,
  git rm/mv/checkout/restore, Python write calls). Reading or copying *from*
  raw/ stays allowed. This is a heuristic, not a sandbox.

Reads the hook payload as JSON on stdin; prints a deny decision or nothing.
"""
import json
import os
import re
import shlex
import sys
from pathlib import Path

DELETE_CMDS = {"rm", "unlink", "truncate", "shred"}
COPY_CMDS = {"cp", "rsync", "install", "ln"}  # blocked only if raw file is the target
INPLACE_CMDS = {"sed", "gsed", "perl"}
GIT_WRITE_SUBCMDS = {"rm", "mv", "checkout", "restore"}


def logged_sources(log_file: Path) -> set[str]:
    sources = set()
    if not log_file.is_file():
        return sources
    for line in log_file.read_text(encoding="utf-8").splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) >= 2 and cells[1].startswith("raw/"):
            sources.add(cells[1])
    return sources


def to_rel(token: str, root: Path, cwd: Path) -> str | None:
    """Project-relative POSIX path for a path-like token, or None."""
    token = token.strip("'\"")
    if not token or token.startswith("-"):
        return None
    path = Path(os.path.expanduser(token))
    if not path.is_absolute():
        path = cwd / path
    try:
        return Path(os.path.normpath(path)).relative_to(root).as_posix()
    except ValueError:
        return None


def deny(reason: str) -> int:
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": reason,
        }
    }))
    return 0


def check_file_tool(tool_input: dict, root: Path, cwd: Path, logged: set[str]) -> str | None:
    target = tool_input.get("file_path") or tool_input.get("notebook_path")
    rel = to_rel(target, root, cwd) if target else None
    return rel if rel in logged else None


def check_bash(command: str, root: Path, cwd: Path, logged: set[str]) -> str | None:
    def hit(tokens):
        for t in tokens:
            rel = to_rel(t, root, cwd)
            if rel in logged:
                return rel
        return None

    # Redirections anywhere in the command: > file, >> file, &> file
    for m in re.finditer(r"(?:&>|\d?>>?)\s*(\"[^\"]+\"|'[^']+'|[^\s;&|]+)", command):
        rel = to_rel(m.group(1), root, cwd)
        if rel in logged:
            return rel

    # Python-style writes whose target is a logged file given as a quoted string literal
    # (a path merely mentioned in text written elsewhere does not count)
    if re.search(r"write_text|write_bytes|open\([^)]*['\"][wa]", command):
        for path in logged:
            if re.search(r"['\"](?:%s/)?%s['\"]" % (re.escape(str(root)), re.escape(path)), command):
                return path

    for segment in re.split(r"&&|\|\||;|\||\n", command):
        try:
            tokens = shlex.split(segment)
        except ValueError:
            tokens = segment.split()
        while tokens and ("=" in tokens[0] and not tokens[0].startswith("-") or tokens[0] in {"sudo", "command", "env"}):
            tokens = tokens[1:]
        if not tokens:
            continue
        cmd, args = os.path.basename(tokens[0]), tokens[1:]

        if cmd in {"cd", "pushd"}:
            # Follow directory changes so relative paths in later segments resolve correctly
            target = args[0] if args else str(Path.home())
            cwd = Path(os.path.normpath(cwd / os.path.expanduser(target)))
            continue
        if cmd in DELETE_CMDS or cmd == "mv" or cmd == "tee":
            rel = hit(args)
        elif cmd in COPY_CMDS:
            paths = [a for a in args if not a.startswith("-")]
            rel = hit(paths[-1:]) if len(paths) >= 2 else None
        elif cmd in INPLACE_CMDS:
            inplace = any(re.match(r"^-[a-zA-Z]*i", a) or a.startswith("--in-place") for a in args)
            rel = hit(args) if inplace else None
        elif cmd == "git" and args:
            sub = next((a for a in args if not a.startswith("-")), "")
            rel = hit(args) if sub in GIT_WRITE_SUBCMDS else None
        else:
            rel = None
        if rel:
            return rel
    return None


def main() -> int:
    payload = json.load(sys.stdin)
    tool_name = payload.get("tool_name", "")
    tool_input = payload.get("tool_input") or {}
    root = Path(os.environ.get("CLAUDE_PROJECT_DIR") or payload.get("cwd") or ".").resolve()
    cwd = Path(payload.get("cwd") or root)
    logged = logged_sources(root / "wiki" / "log.md")

    if tool_name == "Bash":
        rel = check_bash(tool_input.get("command", ""), root, cwd, logged)
    else:
        rel = check_file_tool(tool_input, root, cwd, logged)

    if rel:
        return deny(
            f"{rel} is already ingested (listed in wiki/log.md) and is immutable. "
            "Put corrections into a new note in raw/ instead."
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())

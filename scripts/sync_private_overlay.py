#!/usr/bin/env python3
"""Synchronize canonical private repo-local skills into Codex and Claude projections."""

from __future__ import annotations

import argparse
import os
import shutil
import stat
import tempfile
from pathlib import Path

from cataloglib import add_claude_explicit_control, directory_hashes, read_skill_metadata


def _safe_target(repo: Path, relative: str) -> Path:
    """Return the projection folder inside repo, refusing any symlinked path.

    Resolving through a symlinked `.agents` or `.claude` parent would let sync remove
    and replace a directory outside the repository, so every component between the
    repository and the target must be a real directory (or not exist yet), and the
    resolved target must stay inside the repository.
    """
    current = repo
    for part in Path(relative).parts:
        current = current / part
        if current.is_symlink():
            raise ValueError(f"unsafe overlay target: {current} is a symlink")
    target = (repo / relative).resolve()
    expected_parent = (repo / Path(relative).parent).resolve()
    if (
        target.parent != expected_parent
        or target.name != "skills"
        or not target.is_relative_to(repo)
    ):
        raise ValueError(f"unsafe overlay target: {target}")
    return target


def _directory_flags() -> int | None:
    """No-follow directory open flags, or None where the platform lacks them (Windows).

    Looked up lazily so importing this module, and running --check, work everywhere.
    """
    directory: int | None = getattr(os, "O_DIRECTORY", None)
    no_follow: int | None = getattr(os, "O_NOFOLLOW", None)
    if directory is None or no_follow is None or not shutil.rmtree.avoids_symlink_attacks:
        return None
    return os.O_RDONLY | directory | no_follow


def _open_directory_path(path: Path) -> int:
    """Open an absolute directory by walking every component with no-follow opens.

    O_NOFOLLOW on the final component alone would still follow a symlinked ancestor,
    so each component is opened relative to its parent's handle, starting at "/".
    """
    flags = _directory_flags()
    if flags is None:
        raise ValueError("overlay synchronization requires no-follow directory support")
    if not path.is_absolute():
        raise ValueError(f"repository path must be absolute: {path}")
    fd = os.open(path.anchor, flags)
    try:
        for part in path.parts[1:]:
            next_fd = os.open(part, flags, dir_fd=fd)
            os.close(fd)
            fd = next_fd
    except BaseException:
        os.close(fd)
        raise
    return fd


def _open_directory(name: str, dir_fd: int, create: bool = False) -> int:
    """Open a directory relative to dir_fd without following a symlink at name."""
    flags = _directory_flags()
    if flags is None:
        raise ValueError("overlay synchronization requires no-follow directory support")
    try:
        return os.open(name, flags, dir_fd=dir_fd)
    except FileNotFoundError:
        if not create:
            raise
        os.mkdir(name, 0o755, dir_fd=dir_fd)
        return os.open(name, flags, dir_fd=dir_fd)


def _copy_tree_into(source: Path, name: str, dir_fd: int) -> None:
    """Copy a trusted rendered tree to name under dir_fd, creating every entry exclusively."""
    os.mkdir(name, 0o755, dir_fd=dir_fd)
    target_fd = _open_directory(name, dir_fd)
    try:
        for entry in sorted(source.iterdir()):
            if entry.is_symlink():
                raise ValueError(f"rendered overlay contains a symlink: {entry}")
            if entry.is_dir():
                _copy_tree_into(entry, entry.name, target_fd)
                continue
            no_follow: int = getattr(os, "O_NOFOLLOW", 0)
            flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | no_follow
            output = os.open(entry.name, flags, stat.S_IMODE(entry.stat().st_mode), dir_fd=target_fd)
            try:
                data = memoryview(entry.read_bytes())
                while data:
                    data = data[os.write(output, data):]
            finally:
                os.close(output)
    finally:
        os.close(target_fd)


def _replace_projection(repo_fd: int, relative: str, expected: Path) -> None:
    """Replace repo/relative with expected, bound to directory handles, never following links.

    The parent (.agents or .claude) is opened with O_NOFOLLOW, and every later step
    works relative to that handle, so a symlink swapped in after validation cannot
    redirect the delete or the copy outside the repository. The old projection is
    renamed aside and removed with the symlink-safe fd-based rmtree.
    """
    parent_name, leaf = Path(relative).parts
    token = f"{os.getpid()}-{os.urandom(4).hex()}"
    staging, retired = f".{leaf}.sync-{token}", f".{leaf}.old-{token}"
    parent_fd = _open_directory(parent_name, repo_fd, create=True)
    try:
        _copy_tree_into(expected, staging, parent_fd)
        try:
            existing = os.stat(leaf, dir_fd=parent_fd, follow_symlinks=False)
        except FileNotFoundError:
            existing = None
        if existing is not None:
            if not stat.S_ISDIR(existing.st_mode):
                shutil.rmtree(staging, dir_fd=parent_fd)
                raise ValueError(f"unsafe overlay target: {relative} is not a directory")
            os.rename(leaf, retired, src_dir_fd=parent_fd, dst_dir_fd=parent_fd)
            shutil.rmtree(retired, dir_fd=parent_fd)
        os.rename(staging, leaf, src_dir_fd=parent_fd, dst_dir_fd=parent_fd)
    finally:
        os.close(parent_fd)


def _exists_no_follow(name: str, dir_fd: int) -> bool:
    try:
        os.stat(name, dir_fd=dir_fd, follow_symlinks=False)
    except FileNotFoundError:
        return False
    return True


def _snapshot_tree(dir_fd: int, destination: Path) -> None:
    """Copy the directory open at dir_fd into destination, refusing any symlink."""
    destination.mkdir(parents=True)
    with os.scandir(dir_fd) as entries:
        names = sorted((entry.name, entry.is_symlink(), entry.is_dir(follow_symlinks=False)) for entry in entries)
    for name, is_link, is_dir in names:
        if is_link:
            raise ValueError(f"canonical overlay source contains a symlink: {name}")
        if is_dir:
            child = _open_directory(name, dir_fd)
            try:
                _snapshot_tree(child, destination / name)
            finally:
                os.close(child)
            continue
        source = os.open(name, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0), dir_fd=dir_fd)
        try:
            mode = stat.S_IMODE(os.fstat(source).st_mode)
            with os.fdopen(os.dup(source), "rb") as handle:
                data = handle.read()
        finally:
            os.close(source)
        target = destination / name
        target.write_bytes(data)
        target.chmod(mode)


def _snapshot_source(repo_fd: int, destination: Path) -> Path:
    """Snapshot .agent-skills/skills through the bound repository handle."""
    agent_fd = _open_directory(".agent-skills", repo_fd)
    try:
        skills_fd = _open_directory("skills", agent_fd)
        try:
            _snapshot_tree(skills_fd, destination)
        finally:
            os.close(skills_fd)
    finally:
        os.close(agent_fd)
    return destination


def _check_existing_conventions_fd(repo_fd: int) -> list[str]:
    """Handle-bound version of _check_existing_conventions for the mutating path."""
    if _exists_no_follow(".agent-skills", repo_fd):
        return []
    for parent, leaf in ((".claude", "skills"), (".agents", "skills")):
        if not _exists_no_follow(parent, repo_fd):
            continue
        parent_fd = _open_directory(parent, repo_fd)
        try:
            if _exists_no_follow(leaf, parent_fd):
                return [
                    f"{parent}/{leaf} exists without .agent-skills/; follow the existing repo-local "
                    "skill convention instead of this synchronizer"
                ]
        finally:
            os.close(parent_fd)
    return []


def _validate_target_fd(repo_fd: int, relative: str) -> None:
    """Refuse a projection whose parent or leaf is a symlink or not a directory."""
    parent_name, leaf = Path(relative).parts
    try:
        parent = os.stat(parent_name, dir_fd=repo_fd, follow_symlinks=False)
    except FileNotFoundError:
        return
    if not stat.S_ISDIR(parent.st_mode):
        raise ValueError(f"unsafe overlay target: {parent_name} is a symlink or not a directory")
    parent_fd = _open_directory(parent_name, repo_fd)
    try:
        try:
            existing = os.stat(leaf, dir_fd=parent_fd, follow_symlinks=False)
        except FileNotFoundError:
            return
        if not stat.S_ISDIR(existing.st_mode):
            raise ValueError(f"unsafe overlay target: {relative} is a symlink or not a directory")
    finally:
        os.close(parent_fd)


def _render_from(source: Path, output: Path) -> tuple[Path, Path]:
    codex = output / ".agents" / "skills"
    claude = output / ".claude" / "skills"
    codex.mkdir(parents=True, exist_ok=True)
    claude.mkdir(parents=True, exist_ok=True)
    for skill_dir in sorted(path for path in source.iterdir() if path.is_dir()):
        metadata = read_skill_metadata(skill_dir)
        name = metadata["name"]
        if name != skill_dir.name:
            raise ValueError(f"overlay skill directory and name differ: {skill_dir}")
        shutil.copytree(skill_dir, codex / name)
        (claude / name).mkdir(parents=True)
        for item in sorted(skill_dir.iterdir()):
            if item.name == "agents":
                continue
            destination = claude / name / item.name
            if item.is_dir():
                shutil.copytree(item, destination)
            elif item.name == "SKILL.md" and metadata["invocation"] == "explicit":
                destination.write_text(add_claude_explicit_control(item.read_text(encoding="utf-8")), encoding="utf-8")
            else:
                shutil.copy2(item, destination)
    return codex, claude


def _render(repo: Path, output: Path) -> tuple[Path, Path]:
    source = repo / ".agent-skills" / "skills"
    if not source.is_dir():
        raise FileNotFoundError(f"missing canonical overlay source: {source}")
    return _render_from(source, output)


def _check_existing_conventions(repo: Path) -> list[str]:
    """Refuse repositories whose client skill folders are not projections of .agent-skills/."""
    if (repo / ".agent-skills").exists():
        return []
    for relative in (".claude/skills", ".agents/skills"):
        if (repo / relative).exists():
            return [
                f"{relative} exists without .agent-skills/; follow the existing repo-local "
                "skill convention instead of this synchronizer"
            ]
    return []


def sync(repo: Path, check_only: bool) -> list[str]:
    if check_only:
        return _check(repo.resolve())
    # Mutating path: bind the repository first by walking every component of the
    # absolute, unresolved path with no-follow opens, so any symlink in --repo or a
    # later rename of the repository or an ancestor is refused rather than followed.
    # Every read and write then goes through that one handle.
    repo_path = Path(os.path.abspath(repo))
    try:
        repo_fd = _open_directory_path(repo_path)
    except (NotADirectoryError, OSError) as error:
        raise ValueError(
            f"unsafe repository path {repo_path}: it must be a real directory with no symlinked "
            "component; pass its real path"
        ) from error
    try:
        return _sync_bound(repo_fd)
    finally:
        os.close(repo_fd)


def _check(repo: Path) -> list[str]:
    """Read-only drift check; it never deletes or writes inside the repository."""
    errors = _check_existing_conventions(repo)
    if errors:
        return errors
    with tempfile.TemporaryDirectory(prefix="private-overlay-") as temporary:
        expected_codex, expected_claude = _render(repo, Path(temporary))
        for expected, relative in ((expected_codex, ".agents/skills"), (expected_claude, ".claude/skills")):
            actual = _safe_target(repo, relative)
            if directory_hashes(expected) != directory_hashes(actual):
                errors.append(f"private overlay projection drifted: {actual.relative_to(repo)}")
    return errors


def _sync_bound(repo_fd: int) -> list[str]:
    errors = _check_existing_conventions_fd(repo_fd)
    if errors:
        return errors
    if not _exists_no_follow(".agent-skills", repo_fd):
        raise FileNotFoundError("missing canonical overlay source: .agent-skills/skills")
    with tempfile.TemporaryDirectory(prefix="private-overlay-") as temporary:
        snapshot = _snapshot_source(repo_fd, Path(temporary) / "source")
        expected_codex, expected_claude = _render_from(snapshot, Path(temporary) / "rendered")
        targets = ((expected_codex, ".agents/skills"), (expected_claude, ".claude/skills"))
        # Validate every target before changing any, so a bad second target cannot
        # leave the first one already replaced.
        for _expected, relative in targets:
            _validate_target_fd(repo_fd, relative)
        for expected, relative in targets:
            _replace_projection(repo_fd, relative, expected)
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    try:
        errors = sync(args.repo, args.check)
    except (ValueError, OSError) as error:
        print(f"ERROR: {error}")
        return 1
    if errors:
        print("\n".join(f"ERROR: {error}" for error in errors))
        return 1
    print("Private overlay projections match canonical sources." if args.check else "Private overlay projections synchronized.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

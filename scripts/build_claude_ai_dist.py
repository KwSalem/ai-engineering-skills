#!/usr/bin/env python3
"""
Rebuilds the claude.ai upload zips (dist/claude-ai/*.zip) from the canonical
skills/ source tree, replacing each skill's long-form description with the
short version required by claude.ai's upload limit (<=200 chars).

Usage: python3 scripts/build_claude_ai_dist.py
Run from the repository root.
"""
import json
import pathlib
import shutil
import zipfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
SKILLS_DIR = ROOT / "skills"
DIST_DIR = ROOT / "dist" / "claude-ai"
DESCRIPTIONS = json.loads((ROOT / "scripts" / "short_descriptions.json").read_text())

CHAR_LIMIT = 200


def find_skill_dirs():
    for group_dir in sorted(SKILLS_DIR.iterdir()):
        if not group_dir.is_dir():
            continue
        for skill_dir in sorted(group_dir.iterdir()):
            if (skill_dir / "SKILL.md").exists():
                yield skill_dir


def build_one(skill_dir: pathlib.Path, tmp_root: pathlib.Path):
    name = skill_dir.name
    if name not in DESCRIPTIONS:
        raise SystemExit(
            f"No short description registered for '{name}' in "
            f"scripts/short_descriptions.json — add one before building."
        )
    desc = DESCRIPTIONS[name]
    if len(desc) > CHAR_LIMIT:
        raise SystemExit(
            f"Short description for '{name}' is {len(desc)} chars, "
            f"over the {CHAR_LIMIT} char claude.ai limit. Trim it."
        )

    dest = tmp_root / name
    shutil.copytree(skill_dir, dest)

    skill_md = dest / "SKILL.md"
    text = skill_md.read_text()
    end = text.index("\n---\n", 4)
    new_frontmatter = f"---\nname: {name}\ndescription: {desc}\n---"
    skill_md.write_text(new_frontmatter + text[end + 4 :])

    zip_path = DIST_DIR / f"{name}.zip"
    if zip_path.exists():
        zip_path.unlink()
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for file in dest.rglob("*"):
            if file.is_file():
                zf.write(file, arcname=file.relative_to(tmp_root))

    print(f"  {name}: {len(desc)}/{CHAR_LIMIT} chars -> {zip_path.relative_to(ROOT)}")


def main():
    DIST_DIR.mkdir(parents=True, exist_ok=True)
    tmp_root = ROOT / ".build_tmp"
    if tmp_root.exists():
        shutil.rmtree(tmp_root)
    tmp_root.mkdir()

    skill_dirs = list(find_skill_dirs())
    print(f"Building {len(skill_dirs)} claude.ai upload zips...")
    for skill_dir in skill_dirs:
        build_one(skill_dir, tmp_root)

    shutil.rmtree(tmp_root)
    print(f"\nDone. {len(skill_dirs)} zips in {DIST_DIR.relative_to(ROOT)}/")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Bulk rename utility: globex_ → chroma_
Recursively renames files and updates symbol references.
Skips .git, node_modules, __pycache__, and .pyc files.
"""

import re
import sys
import argparse
import logging
from pathlib import Path
from typing import Tuple

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s: %(message)s'
)
logger = logging.getLogger(__name__)

SKIP_DIRS = {'.git', 'node_modules', '__pycache__', '.venv', 'venv'}
SKIP_EXTENSIONS = {'.pyc', '.pyo', '.pyd', '.so', '.dll', '.exe'}


def should_skip(path: Path) -> bool:
    """Return True if path should be skipped."""
    if path.is_dir() and path.name in SKIP_DIRS:
        return True
    if path.suffix in SKIP_EXTENSIONS:
        return True
    return False


def rename_file(file_path: Path, dry_run: bool = False) -> bool:
    """Rename file if it contains 'globex_'. Return True if renamed."""
    if 'globex_' not in file_path.name:
        return False
    
    new_name = file_path.name.replace('globex_', 'chroma_')
    new_path = file_path.parent / new_name
    
    if dry_run:
        logger.info(f"  [DRY-RUN] Would rename: {file_path.name} → {new_name}")
        return True
    
    try:
        file_path.rename(new_path)
        logger.info(f"  📄 {file_path.name} → {new_name}")
        return True
    except Exception as e:
        logger.error(f"  ❌ Failed to rename {file_path.name}: {e}")
        return False


def update_file_content(file_path: Path, dry_run: bool = False) -> Tuple[int, int]:
    """Update globex_ references in file content. Return (replacements, errors)."""
    try:
        content = file_path.read_text(encoding='utf-8')
    except (UnicodeDecodeError, Exception):
        return (0, 1)
    
    original = content
    # Replace globex_ identifiers (case-sensitive)
    content = re.sub(r'\bglobex_', 'chroma_', content)
    # Replace GlobexService, GlobexUtil, etc. (camel case)
    content = re.sub(r'\bGlobex(?=[A-Z])', 'Chroma', content)
    # Replace Globex in documentation/comments (word boundary)
    content = re.sub(r'\bGlobex\b', 'Chroma', content)
    
    if content == original:
        return (0, 0)
    
    replacements = content.count('chroma_') - original.count('chroma_')
    
    if dry_run:
        logger.info(f"  [DRY-RUN] Would update {file_path.name}: {replacements} replacements")
        return (replacements, 0)
    
    try:
        file_path.write_text(content, encoding='utf-8')
        return (replacements, 0)
    except Exception as e:
        logger.error(f"  ❌ Failed to write {file_path.name}: {e}")
        return (0, 1)


def process_directory(root_path: Path, dry_run: bool = False) -> Tuple[int, int, int, int]:
    """Recursively process directory. Return (files_renamed, content_updates, errors, dirs_skipped)."""
    files_renamed = 0
    content_updates = 0
    errors = 0
    dirs_skipped = 0
    
    try:
        for item in root_path.rglob('*'):
            if should_skip(item):
                if item.is_dir():
                    dirs_skipped += 1
                continue
            
            if item.is_file():
                # Rename file if needed
                if rename_file(item, dry_run):
                    files_renamed += 1
                    # Update content after rename (read from new path)
                    if not dry_run:
                        item = item.parent / item.name.replace('globex_', 'chroma_')
                
                # Update content
                updates, errs = update_file_content(item, dry_run)
                if updates > 0:
                    content_updates += updates
                    if not dry_run:
                        logger.info(f"    ✏️  {item.name}: {updates} replacements")
                if errs > 0:
                    errors += errs
    
    except Exception as e:
        logger.error(f"❌ Error processing {root_path}: {e}")
        errors += 1
    
    return (files_renamed, content_updates, errors, dirs_skipped)


def main() -> None:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Bulk rename utility: globex_ → chroma_"
    )
    parser.add_argument(
        '--check',
        action='store_true',
        help='Dry-run mode: show what would be changed without making changes'
    )
    parser.add_argument(
        '--path',
        type=Path,
        default=None,
        help='Root path to process (default: parent directory of this script)'
    )
    parser.add_argument(
        '--verbose',
        '-v',
        action='store_true',
        help='Enable verbose logging'
    )
    
    args = parser.parse_args()
    
    # Set logging level
    if args.verbose:
        logger.setLevel(logging.DEBUG)
    
    # Determine root path
    root = args.path if args.path else Path(__file__).parent.parent
    
    mode = "[DRY-RUN MODE]" if args.check else ""
    logger.info(f"🔄 Starting bulk rename: globex_ → chroma_ {mode}")
    logger.info(f"📁 Root: {root}\n")
    
    if args.check:
        logger.warning("⚠️  Dry-run mode enabled - no changes will be made")
    
    files_renamed, content_updates, errors, dirs_skipped = process_directory(root, args.check)
    
    logger.info("\n" + "=" * 60)
    logger.info("✅ Summary:")
    logger.info(f"   Files {'that would be ' if args.check else ''}renamed:      {files_renamed}")
    logger.info(f"   Content updates:    {content_updates}")
    logger.info(f"   Directories skipped: {dirs_skipped}")
    logger.info(f"   Errors:             {errors}")
    logger.info("=" * 60)
    
    if args.check:
        logger.info("\n💡 Run without --check to apply changes")
    
    if errors > 0:
        sys.exit(1)


if __name__ == '__main__':
    main()
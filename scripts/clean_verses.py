#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate a "clean" version of zhonglun-modern.md:
- Keep only chapter titles, original verses, and translations
- Remove all philosophical commentary, introductions, and conclusions
- Strip labels like 【破自生】and section headers like "现代逐句翻译"
- Output as a single merged markdown file
"""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "zhonglun-modern.md"
OUT = ROOT / "zhonglun-modern-clean.md"

# Header detection patterns
INTRO_RE = re.compile(r'^#{1,3}\s*(?:一、|二、|三、|四、|五、)?(?:引言|开头|前言)')
ORIGINAL_RE = re.compile(r'^#{1,3}\s*(?:一、|二、|三、|四、|五、)?(?:原文|原文：|原文：龙树偈颂|龙树偈颂原文|龙树偈颂原文|纯净偈颂|原文与逐颂现代翻译)')
TRANSLATION_RE = re.compile(r'^#{1,3}\s*(?:一、|二、|三、|四、|五、)?(?:现代逐句翻译|现代逐句翻译：|逐句翻译|译文)')
CONCLUSION_RE = re.compile(r'^#{1,3}\s*(?:一、|二、|三、|四、|五、|六、|七、)?(?:综合论述|综合性结尾论述|结尾综合论述|综合结尾论述|结尾论述|结语|结论|五、结语|四、结语|总结)')
REFS_RE = re.compile(r'^\*?\*?参考文献')
CHAPTER_MARKER_RE = re.compile(r'^<!-- ch\d+\.md -->$')

# Content cleaning patterns
LABEL_RE = re.compile(r'^【[^】]+】\s*')
SECTION_LABEL_RE = re.compile(r'^\*\*(?:第[一二三四五六七八九十\d]+颂|【颂[一二三四五六七八九十\d]+】|【第[一二三四五六七八九十\d]+颂)[^*]*\*\*\s*$')
INLINE_BOLD_LABEL_RE = re.compile(r'^\*\*(?:第[一二三四五六七八九十\d]+颂|【颂[一二三四五六七八九十\d]+】|【第[一二三四五六七八九十\d]+颂)[^*]*\*\*\s*')
ORIGINAL_TAG_RE = re.compile(r'^\*\*原文\*\*[:：]?\s*$')
TRANSLATION_TAG_RE = re.compile(r'^\*\*现代逐句翻译\*\*[:：]?\s*$')
VERSE_HEADER_RE = re.compile(r'^#{1,3}\s*第\d+颂')


def process_chapter(lines):
    """Process lines of a single chapter. Returns cleaned lines."""
    state = 'SKIP'  # SKIP, ORIGINAL, TRANSLATION
    result = []
    i = 0
    n = len(lines)

    while i < n:
        line = lines[i]
        stripped = line.strip()

        if not stripped:
            i += 1
            continue

        # State transitions based on headers
        if INTRO_RE.match(stripped):
            state = 'SKIP'
            i += 1
            continue

        if ORIGINAL_RE.match(stripped):
            state = 'ORIGINAL'
            i += 1
            continue

        if TRANSLATION_RE.match(stripped):
            state = 'TRANSLATION'
            i += 1
            continue

        if CONCLUSION_RE.match(stripped) or REFS_RE.match(stripped):
            state = 'SKIP'
            i += 1
            continue

        # Horizontal rules: keep in ORIGINAL/TRANSLATION as separators
        if stripped == '---' or stripped == '***':
            if state in ('ORIGINAL', 'TRANSLATION'):
                # Add blank line instead of rule for cleaner output
                result.append('')
            i += 1
            continue

        # Skip sub-headers within original/translation (like ### 第1颂)
        if VERSE_HEADER_RE.match(stripped):
            i += 1
            continue

        # Skip "译注" lines (translator's notes) anywhere
        if '译注' in stripped:
            i += 1
            continue

        # Chapter title: always keep
        if stripped.startswith('# ') and not stripped.startswith('## '):
            result.append(line)
            i += 1
            continue

        # In SKIP state: ignore everything else
        if state == 'SKIP':
            i += 1
            continue

        # In ORIGINAL state: collect verse text
        if state == 'ORIGINAL':
            # Check for inline translation tag -> switch to TRANSLATION
            if TRANSLATION_TAG_RE.match(stripped):
                state = 'TRANSLATION'
                i += 1
                continue
            # Skip "**原文**：" tag line
            if ORIGINAL_TAG_RE.match(stripped):
                i += 1
                continue
            # Skip section labels
            if SECTION_LABEL_RE.match(stripped):
                i += 1
                continue
            # Skip "**观XX品第X**" style
            if stripped.startswith('**') and stripped.endswith('**') and not stripped.startswith('**原文'):
                i += 1
                continue
            # Keep blockquotes (verses) and plain verse lines
            result.append(line)
            i += 1
            continue

        # In TRANSLATION state: collect translations
        if state == 'TRANSLATION':
            # Check for inline original tag -> switch to ORIGINAL (ch01 mixed format)
            if ORIGINAL_TAG_RE.match(stripped):
                state = 'ORIGINAL'
                i += 1
                continue
            # Skip translation tag line
            if TRANSLATION_TAG_RE.match(stripped):
                i += 1
                continue
            # Skip section labels
            if SECTION_LABEL_RE.match(stripped):
                i += 1
                continue
            # Skip "**第X颂：...**" headers
            if re.match(r'^\*\*第[一二三四五六七八九十\d]+颂[:：]', stripped):
                i += 1
                continue
            # Skip "**【颂X】**" headers
            if re.match(r'^\*\*【颂[一二三四五六七八九十\d]+】\*\*\s*$', stripped):
                i += 1
                continue
            # Skip empty blockquote markers
            if stripped == '>':
                i += 1
                continue

            # Remove 【标签】prefixes
            cleaned = LABEL_RE.sub('', line)
            # Remove inline bold labels at start
            cleaned = INLINE_BOLD_LABEL_RE.sub('', cleaned)

            if cleaned.strip():
                result.append(cleaned)
            i += 1
            continue

        i += 1

    return result


def main():
    src_text = SRC.read_text(encoding='utf-8')
    all_lines = src_text.splitlines()

    output_lines = []
    chapter_lines = []
    in_front_matter = True

    for line in all_lines:
        stripped = line.strip()

        if CHAPTER_MARKER_RE.match(stripped):
            # Process previous chapter (or front matter)
            if in_front_matter:
                # Front matter: keep only title
                for fl in chapter_lines:
                    if fl.strip().startswith('# '):
                        output_lines.append(fl.strip())
                        output_lines.append('')
                        output_lines.append('> 龙树《中论》现代汉语译本')
                        output_lines.append('')
                        output_lines.append('---')
                        break
                in_front_matter = False
            else:
                # Process chapter
                cleaned = process_chapter(chapter_lines)
                if cleaned:
                    output_lines.append('')
                    output_lines.append(stripped)  # chapter marker
                    output_lines.append('')
                    output_lines.extend(cleaned)

            chapter_lines = []
            continue

        chapter_lines.append(line)

    # Process last chapter
    if chapter_lines:
        if in_front_matter:
            for fl in chapter_lines:
                if fl.strip().startswith('# '):
                    output_lines.append(fl.strip())
                    break
        else:
            cleaned = process_chapter(chapter_lines)
            if cleaned:
                output_lines.append('')
                output_lines.extend(cleaned)

    # Join and clean up whitespace
    output = '\n'.join(output_lines)
    # Collapse 3+ consecutive blank lines to 2
    output = re.sub(r'\n{3,}', '\n\n', output)

    OUT.write_text(output, encoding='utf-8')
    print(f"[OK] Clean version -> {OUT}")
    print(f"      Lines: {len(output.splitlines())}")
    print(f"      Chars: {len(output)}")


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Remove突兀 English words from translations in zhonglun-modern-clean.md.
Preserves Sanskrit/Pali terms and original verses (blockquote lines).
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "zhonglun-modern-clean.md"
OUT = ROOT / "zhonglun-modern-clean.md"

replacements = [
    # (old, new, description)
    ('（production）', '', 'remove redundant English after Chinese 生成'),
    ('（unthinkable）', '', 'remove redundant English after Chinese 不可思的'),
    ('ontological anchoring', '本体论锚定', 'translate English philosophical term'),
    ('ontological leverage', '本体论依托', 'translate English philosophical term'),
    ('ontological trace', '本体论痕迹', 'translate English philosophical term'),
    ('ontological register', '本体论层面', 'translate English philosophical term'),
    (' supposedly ', '  supposedly ', 'translate English adverb (context:  supposedly 后续才会出现)'),
    ('（contradictory）', '（自相矛盾的）', 'translate English philosophical term'),
    ('postponed', '推迟', 'translate English adjective'),
    ('naive realism（朴素实在论）', '朴素实在论', 'remove English, keep Chinese term'),
    ('likewise', '同样', 'translate English adverb'),
    ('bind', '束缚', 'translate English noun'),
    ('（emergence）', '', 'remove redundant English after Chinese 涌现'),
    ('loosened', '松动', 'translate English verb'),
]

def main():
    text = SRC.read_text(encoding='utf-8')
    lines = text.splitlines()
    changed = 0

    for old, new, desc in replacements:
        count = text.count(old)
        if count > 0:
            text = text.replace(old, new)
            changed += count
            print(f'  [{count}x] {desc}: "{old}" → "{new}"')

    OUT.write_text(text, encoding='utf-8')
    print(f'\n[OK] Total replacements: {changed}')
    print(f'      Output: {OUT}')

if __name__ == '__main__':
    main()

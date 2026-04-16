"""Sarasa Mono TC glyph width overrides.

Pre-computed from SarasaMonoTC-Regular.ttf hmtx table (threshold=750),
then calibrated against Notepad++ rendering (2026-04-16).
Only stores codepoints where the font disagrees with Unicode EAW heuristic.
"""

_WIDE_RANGES = [
    # Latin-1 Supplement — calibrated w2 in Sarasa Mono TC
    (0x00A7, 0x00A7),  # § SECTION SIGN
    (0x00B1, 0x00B1),  # ± PLUS-MINUS SIGN
    (0x00B2, 0x00B2),  # ² SUPERSCRIPT TWO
    (0x00B7, 0x00B7),  # · MIDDLE DOT
    (0x00D7, 0x00D7),  # × MULTIPLICATION SIGN
    (0x00F7, 0x00F7),  # ÷ DIVISION SIGN
    # Greek letters — calibrated w2
    (0x0391, 0x03C9),  # Α..ω Greek capital + small letters
    (0x1160, 0x11FF),  # ᅠ..ᇿ (160)
    (0x2001, 0x2001),  #   EM QUAD
    (0x2003, 0x2003),  #   EM SPACE
    (0x2014, 0x2015),  # —..― (2)
    (0x2016, 0x2016),  # ‖ DOUBLE VERTICAL LINE
    (0x2022, 0x2022),  # • BULLET
    (0x2024, 0x2026),  # ․..… (3)
    (0x2030, 0x2031),  # ‰..‱ (2)
    (0x203B, 0x203B),  # ※ REFERENCE MARK
    (0x2042, 0x2042),  # ⁂ ASTERISM
    (0x2053, 0x2053),  # ⁓ SWUNG DASH
    (0x212E, 0x212E),  # ℮ ESTIMATED SYMBOL
    (0x2140, 0x2140),  # ⅀ DOUBLE-STRUCK N-ARY SUMMATION
    (0x214F, 0x214F),  # ⅏ SYMBOL FOR SAMARITAN SOURCE
    (0x2190, 0x21FF),  # ←..⇿ (112)
    # Math symbols — calibrated w2
    (0x2200, 0x2200),  # ∀ FOR ALL
    (0x2203, 0x2203),  # ∃ THERE EXISTS
    (0x2208, 0x2209),  # ∈..∉ ELEMENT OF
    (0x220F, 0x2211),  # ∏..∑ (3)
    (0x2219, 0x221E),  # ∙..∞ (6) — includes √(221A) ∝(221D) ∞(221E)
    (0x2227, 0x2228),  # ∧..∨ LOGICAL AND/OR
    (0x2248, 0x2248),  # ≈ ALMOST EQUAL TO
    (0x2260, 0x2260),  # ≠ NOT EQUAL TO
    (0x2264, 0x2265),  # ≤..≥ (2)
    (0x223E, 0x223E),  # ∾ INVERTED LAZY S
    (0x22C0, 0x22C3),  # ⋀..⋃ (4)
    (0x22EE, 0x22F1),  # ⋮..⋱ (4)
    (0x2301, 0x2301),  # ⌁ ELECTRIC ARROW
    (0x2303, 0x2304),  # ⌃..⌄ (2)
    (0x230C, 0x230F),  # ⌌..⌏ (4)
    (0x2311, 0x2318),  # ⌑..⌘ (8)
    (0x231C, 0x231F),  # ⌜..⌟ (4)
    (0x2324, 0x2328),  # ⌤..⌨ (5)
    (0x232B, 0x232B),  # ⌫ ERASE TO THE LEFT
    (0x232D, 0x2335),  # ⌭..⌵ (9)
    (0x237B, 0x237B),  # ⍻ NOT CHECK MARK
    (0x2384, 0x238B),  # ⎄..⎋ (8)
    (0x2394, 0x2394),  # ⎔ SOFTWARE-FUNCTION SYMBOL
    (0x23B2, 0x23B3),  # ⎲..⎳ (2)
    (0x23C0, 0x23CA),  # ⏀..⏊ (11)
    (0x23CE, 0x23CF),  # ⏎..⏏ (2)
    (0x23E2, 0x23E2),  # ⏢ WHITE TRAPEZIUM
    (0x23E4, 0x23E5),  # ⏤..⏥ (2)
    (0x23ED, 0x23EF),  # ⏭..⏯ (3)
    (0x23F1, 0x23F2),  # ⏱..⏲ (2)
    (0x23F4, 0x23FE),  # ⏴..⏾ (11)
    (0x2460, 0x24FF),  # ①..⓿ (160)
    (0x25A0, 0x25CB),  # ■..○ (44)
    (0x25CD, 0x25E5),  # ◍..◥ (25)
    (0x25E7, 0x25FC),  # ◧..◼ (22)
    (0x25FF, 0x2603),  # ◿..☃ (5)
    (0x2605, 0x2607),  # ★..☇ (3)
    (0x2609, 0x2609),  # ☉ SUN
    (0x260E, 0x2613),  # ☎..☓ (6)
    (0x2616, 0x2617),  # ☖..☗ (2)
    (0x261C, 0x261F),  # ☜..☟ (4)
    (0x2626, 0x2626),  # ☦ ORTHODOX CROSS
    (0x2628, 0x2628),  # ☨ CROSS OF LORRAINE
    (0x262F, 0x262F),  # ☯ YIN YANG
    (0x2639, 0x263C),  # ☹..☼ (4)
    (0x2668, 0x2668),  # ♨ HOT SPRINGS
    (0x2672, 0x267E),  # ♲..♾ (13)
    (0x2680, 0x2689),  # ⚀..⚉ (10)
    (0x2699, 0x2699),  # ⚙ GEAR
    (0x269B, 0x269B),  # ⚛ ATOM SYMBOL
    (0x26AC, 0x26AF),  # ⚬..⚯ (4)
    (0x26CB, 0x26CB),  # ⛋ WHITE DIAMOND IN SQUARE
    (0x26DA, 0x26DA),  # ⛚ DRIVE SLOW SIGN
    (0x26DD, 0x26DE),  # ⛝..⛞ (2)
    (0x26ED, 0x26EF),  # ⛭..⛯ (3)
    (0x26F6, 0x26F6),  # ⛶ SQUARE FOUR CORNERS
    (0x2702, 0x2702),  # ✂ BLACK SCISSORS
    (0x2713, 0x2718),  # ✓..✘ (6)
    (0x271A, 0x271D),  # ✚..✝ (4)
    (0x2720, 0x2727),  # ✠..✧ (8)
    (0x2731, 0x2734),  # ✱..✴ (4)
    (0x2736, 0x274B),  # ✶..❋ (22)
    (0x2756, 0x2756),  # ❖ BLACK DIAMOND MINUS WHITE X
    (0x2758, 0x275A),  # ❘..❚ (3)
    (0x2764, 0x2764),  # ❤ HEAVY BLACK HEART
    (0x2776, 0x2794),  # ❶..➔ (31)
    (0x279C, 0x279E),  # ➜..➞ (3)
    (0x27A1, 0x27A7),  # ➡..➧ (7)
    (0x27CB, 0x27CB),  # ⟋ MATHEMATICAL RISING DIAGONAL
    (0x27CD, 0x27CD),  # ⟍ MATHEMATICAL FALLING DIAGONAL
    (0x27D8, 0x27D9),  # ⟘..⟙ (2)
    (0x27DD, 0x27DE),  # ⟝..⟞ (2)
    (0x27E0, 0x27E1),  # ⟠..⟡ (2)
    (0x27F0, 0x27FF),  # ⟰..⟿ (16)
    (0x2900, 0x2926),  # ⤀..⤦ (39)
    # Block elements — calibrated w2
    (0x2588, 0x2588),  # █ FULL BLOCK
    (0x2934, 0x2935),  # ⤴..⤵ (2)
    (0x2940, 0x2941),  # ⥀..⥁ (2)
    (0x2947, 0x2948),  # ⥇..⥈ (2)
    (0x294A, 0x2965),  # ⥊..⥥ (28)
    (0x296E, 0x296F),  # ⥮..⥯ (2)
    (0x2981, 0x2981),  # ⦁ Z NOTATION SPOT
    (0x29C9, 0x29CB),  # ⧉..⧋ (3)
    (0x29CD, 0x29CD),  # ⧍ TRIANGLE WITH SERIFS AT BOTTOM
    (0x29E8, 0x29E9),  # ⧨..⧩ (2)
    (0x29EB, 0x29EB),  # ⧫ BLACK LOZENGE
    (0x2A00, 0x2A02),  # ⨀..⨂ (3)
    (0x2A05, 0x2A06),  # ⨅..⨆ (2)
    (0x2A09, 0x2A09),  # ⨉ N-ARY TIMES OPERATOR
    (0x2A1D, 0x2A1E),  # ⨝..⨞ (2)
    (0x2B00, 0x2B19),  # ⬀..⬙ (26)
    (0x2B1D, 0x2B3E),  # ⬝..⬾ (34)
    (0x2B45, 0x2B46),  # ⭅..⭆ (2)
    (0x2B4D, 0x2B4D),  # ⭍ DOWNWARDS TRIANGLE-HEADED ZIGZAG ARROW
    (0x2B51, 0x2B54),  # ⭑..⭔ (4)
    (0x2B58, 0x2B59),  # ⭘..⭙ (2)
    (0x2B60, 0x2B73),  # ⭠..⭳ (20)
    (0x2B7A, 0x2B87),  # ⭺..⮇ (14)
    (0x2B8C, 0x2B95),  # ⮌..⮕ (10)
    (0x2BA0, 0x2BA7),  # ⮠..⮧ (8)
    (0x2BB8, 0x2BC8),  # ⮸..⯈ (17)
    (0x2BCA, 0x2BD0),  # ⯊..⯐ (7)
    (0x2BE8, 0x2BEF),  # ⯨..⯯ (8)
    (0x2E3A, 0x2E3B),  # ⸺..⸻ (2)
    (0x2E43, 0x2E43),  # ⹃ DASH WITH LEFT UPTURN
    (0x303F, 0x303F),  # 〿 IDEOGRAPHIC HALF FILL SPACE
    (0x31E4, 0x31E5),  # ㇤..㇥ (2)
    (0x3248, 0x324F),  # ㉈..㉏ (8)
    (0xD7B0, 0xD7C6),  # ힰ..ퟆ (23)
    (0xD7CB, 0xD7FB),  # ퟋ..ퟻ (49)
    (0xEE06, 0xEE0B),  # .. (6)
    (0xF881, 0xF881),  #  ?
    (0xFB00, 0xFB04),  # ﬀ..ﬄ (5)
    (0xFFA0, 0xFFBE),  # ﾠ..ﾾ (31)
    (0xFFC2, 0xFFC7),  # ￂ..ￇ (6)
    (0xFFCA, 0xFFCF),  # ￊ..ￏ (6)
    (0xFFD2, 0xFFD7),  # ￒ..ￗ (6)
    (0xFFDA, 0xFFDC),  # ￚ..ￜ (3)
    (0xFFFC, 0xFFFC),  # ￼ OBJECT REPLACEMENT CHARACTER
]

_NARROW_RANGES = [
    (0x2329, 0x232A),  # 〈..〉 (2)
    (0x26A1, 0x26A1),  # ⚡ HIGH VOLTAGE SIGN
    (0x302A, 0x302F),  # 〪..〯 (6)
    (0x3099, 0x309A),  # ゙..゚ (2)
    (0x31B4, 0x31B7),  # ㆴ..ㆷ (4)
    (0x31BB, 0x31BB),  # ㆻ BOPOMOFO FINAL LETTER G
]

# Codepoints where FE0F (VS-16) changes rendering to emoji presentation (w2).
# The base char alone may be w1, but base+FE0F as a unit = w2.
EMOJI_VS16 = frozenset([
    0x26A0,  # ⚠ WARNING SIGN (⚠️ = w2)
])

def _expand(ranges):
    s = set()
    for lo, hi in ranges:
        s.update(range(lo, hi + 1))
    return frozenset(s)

WIDE_OVERRIDES = _expand(_WIDE_RANGES)
NARROW_OVERRIDES = _expand(_NARROW_RANGES)

# Comprehensive ASCII Rendering Calibration

## 1. 基準標尺 (Scale)
```
[1234567890123456789012345678901234567890] (40 ASCII)
[                                        ] (40 Spaces)
[----------------------------------------] (40 Dashes)
```

## 2. 邊框字元 (Box Drawing - Single)
```
[┌─┬─┐] (5 chars)
[│ │ │] (5 chars)
[├─┼─┤] (5 chars)
[└─┴─┘] (5 chars)
[───] (3 horizontal)
[│││] (3 vertical)
```

## 3. 危險箭頭區 (Arrows - Unicode vs ASCII)
```
[→] (Unicode Single Right)
[→→→→→] (5 Unicode Right)
[->->->->->] (10 ASCII Right)
[←→] (Unicode Double Horizontal)
[<->] (3 ASCII Double)
[▲▼◀▶] (Geometric Arrows)
[>>] (ASCII Double Right)
[=>] (ASCII Fat Right)
```

## 4. 幾何與狀態符號 (Geometric & Status)
```
[●○] (Circles)
[■□] (Squares)
[◆◇] (Diamonds)
[✓✗] (Check/Cross)
[⚠️] (Emoji Warning - VERY DANGEROUS)
[❌] (Emoji Cross - VERY DANGEROUS)
```

## 5. CJK 比例測試 (CJK vs ASCII 1:2)
```
[1234567890] (10 ASCII)
[中文測試五字] (5 CJK)
[┌──┐] (4 Box - 2 chars inside)
[│測試│] (2 Box + 2 CJK = 6 width?)
[│test│] (2 Box + 4 ASCII = 6 width?)
```

## 6. 特殊銜接測試 (Junctions)
```
[───┬───] (Horizontal with Top Junction)
[   │   ] (Vertical Alignment)
[───┴───] (Horizontal with Bottom Junction)
```

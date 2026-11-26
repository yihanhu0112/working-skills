#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Excel 表结构体检：分表名、行列数、前几行表头与样例。

用法:
    python -I profile_excel.py "C:\\path\\book.xlsx"
    python -I profile_excel.py "book.xlsx" --sheet "总明细" --rows 10

只读、不改原文件。用于动手前确认：分表名是否有空格、表头在第几行、
列名是否重复、关键列是否存在、值是不是被 Excel 转成了日期。
"""
import argparse
import sys

try:
    import openpyxl
except ImportError:
    sys.exit("需要 openpyxl：pip install openpyxl")

# Windows 控制台默认 GBK，中文表名/表头会乱码
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass


def brief(v):
    if v is None:
        return ""
    s = str(v).replace("\n", " ").replace("\t", " ")
    return (s[:60] + "…") if len(s) > 60 else s


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("path")
    ap.add_argument("--sheet", default=None, help="只看指定分表（名称需完全一致，含空格）")
    ap.add_argument("--rows", type=int, default=6, help="每个分表打印前 N 行，默认 6")
    a = ap.parse_args()

    wb = openpyxl.load_workbook(a.path, read_only=True, data_only=True)
    print("FILE:", a.path)
    print("SHEETS:", len(wb.sheetnames))
    for s in wb.sheetnames:
        print("  -", repr(s))
    print()

    for name in wb.sheetnames:
        if a.sheet is not None and name != a.sheet:
            continue
        ws = wb[name]
        print(f"=== SHEET {name!r}  dims={ws.max_row}x{ws.max_column} ===")
        for i, row in enumerate(
            ws.iter_rows(min_row=1, max_row=min(ws.max_row, a.rows), values_only=True), 1
        ):
            print(f"R{i}: " + " | ".join(brief(v) for v in row))
        print()

    wb.close()


if __name__ == "__main__":
    main()

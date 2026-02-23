#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import csv
from collections import defaultdict

def convert_csv_to_lowercase(input_csv, output_csv):
    """Convert all content of CSV file to lowercase"""
    with open(input_csv, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        lines = list(reader)
    
    lowercase_lines = []
    for line in lines:
        lowercase_line = [cell.lower() for cell in line]
        lowercase_lines.append(lowercase_line)
    
    with open(output_csv, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(lowercase_lines)
    
    print(f"CSV file converted to lowercase successfully: {output_csv}")

def generate_column_mapping(csv_file, json_file):
    """Generate column mapping from CSV file and save as JSON"""
    table_mappings = defaultdict(dict)
    
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)  # Skip header row
        
        for line in reader:
            if len(line) >= 6:
                new_tbl_nm = line[1]
                new_col_nm = line[2]
                bf_tbl_nm = line[3]
                bf_col_nm = line[4]
                
                table_mappings[bf_tbl_nm][bf_col_nm] = new_col_nm
    
    # Load existing JSON file
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            existing_mappings = json.load(f)
    except FileNotFoundError:
        existing_mappings = {}
    
    # Update existing mappings with new data
    for table, mappings in table_mappings.items():
        if table not in existing_mappings:
            existing_mappings[table] = {}
        for bf_col, new_col in mappings.items():
            existing_mappings[table][bf_col] = new_col
    
    # Convert all keys to lowercase for consistency
    lowercase_mappings = {}
    for table, mappings in existing_mappings.items():
        lowercase_table = table.lower()
        lowercase_mappings[lowercase_table] = {}
        for bf_col, new_col in mappings.items():
            lowercase_bf_col = bf_col.lower()
            lowercase_new_col = new_col.lower()
            lowercase_mappings[lowercase_table][lowercase_bf_col] = lowercase_new_col
    
    # Save to JSON file
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(lowercase_mappings, f, ensure_ascii=False, indent=2)
    
    print(f"Column mapping file updated successfully: {json_file}")
    
    # Print generated mappings for verification
    print("\n=== Generated Column Mapping ===")
    for table, mappings in lowercase_mappings.items():
        print(f"\n{table}:")
        for bf_col, new_col in mappings.items():
            print(f"  {bf_col} -> {new_col}")

def main():
    csv_file = 'DDL/data/tb_col_mapp.csv'
    json_file = 'msys/column_mapping.json'
    
    print("Column mapping consistency correction started")
    
    # 1. CSV 파일 소문자로 변환
    convert_csv_to_lowercase(csv_file, csv_file)
    
    # 2. 컬럼 매핑 JSON 파일 생성
    generate_column_mapping(csv_file, json_file)
    
    print("\nAll tasks completed successfully!")

if __name__ == "__main__":
    main()
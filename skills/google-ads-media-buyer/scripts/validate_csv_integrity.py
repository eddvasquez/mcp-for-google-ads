import csv

def validate_master_csv(path, name):
    print(f"\n--- Validating {name} ({path}) ---")
    with open(path, "r", encoding="utf-8-sig") as f:
        reader = csv.reader(f)
        headers = next(reader)
        header_len = len(headers)
        print(f"Header columns: {header_len}")
        
        pos_keywords = set()
        neg_keywords = set()
        row_count = 0
        errors = []
        
        for idx, row in enumerate(reader, start=2):
            row_count += 1
            if len(row) != header_len:
                errors.append(f"Row {idx} has {len(row)} columns, expected {header_len}")
            
            camp = row[0].strip()
            ag = row[12].strip()
            status = row[13].strip()
            kw = row[14].strip().lower()
            ct = row[15].strip()
            
            if ct in ["Phrase", "Exact"]:
                key = (ag, kw, ct)
                if key in pos_keywords:
                    errors.append(f"Duplicate positive keyword in Row {idx}: {key}")
                pos_keywords.add(key)
            elif ct == "Campaign negative":
                clean_neg = kw.strip('"').strip('[').strip(']').strip()
                neg_keywords.add(clean_neg)
        
        # Check conflict: is any exact positive in campaign negatives?
        conflicts = []
        for ag, kw, ct in pos_keywords:
            clean_pos = kw.strip('"').strip('[').strip(']').strip()
            if clean_pos in neg_keywords:
                conflicts.append((ag, kw, ct))
                
        print(f"Total data rows: {row_count}")
        print(f"Total positive keywords: {len(pos_keywords)}")
        print(f"Total campaign negatives: {len(neg_keywords)}")
        print(f"Errors found: {len(errors)}")
        if errors:
            for e in errors[:5]:
                print(f"  ERROR: {e}")
        print(f"Direct conflicts found: {len(conflicts)}")
        if conflicts:
            for c in conflicts[:5]:
                print(f"  CONFLICT: {c}")
        
        assert len(errors) == 0, f"Validation failed with {len(errors)} errors!"
        print(f"SUCCESS: {name} validated 100% OK!")

validate_master_csv(r"c:\Users\PC\Documents\ChatGPT\Otros\Ana Maria Tre\templates\google_ads_activos\google_ads_editor_import_campaign.csv", "Master Retorno")
validate_master_csv(r"c:\Users\PC\Documents\ChatGPT\Otros\Ana Maria Tre\templates\google_ads_activos\google_ads_editor_import_high_volume.csv", "Master HighVolume")

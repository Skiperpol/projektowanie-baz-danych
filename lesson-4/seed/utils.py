import re
from typing import List, Dict

def escape_csv_value(val) -> str:
    """
    Escapes special characters for safe usage in PostgreSQL COPY CSV format.

    Rules:
    - None    → "\\N"   (PostgreSQL NULL literal)
    - "\\"    → "\\\\"  (escape backslash)
    - ","     → "\\,"   (escape column separator)
    - newline → "\\n"   (escape row separator)
    - bool    → "True"/"False" (COPY understands booleans natively)
    """
    if val is None:
        return "\\N"
    if isinstance(val, bool):
        return str(val)
    s = str(val)
    s = s.replace("\\", "\\\\").replace(",", "\\,").replace("\n", "\\n")
    return s

def columns_excluding_generated(columns: List[Dict]) -> List[Dict]:
    out = []
    for col in columns:
        cons = " ".join([c.upper() for c in col.get("constraints", [])])
        if "GENERATED" in cons or ("PRIMARY KEY" in cons and "GENERATED" in cons):
            continue
        out.append(col)
    return out

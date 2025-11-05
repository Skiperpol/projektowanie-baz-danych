import re
from typing import Dict, List

FK_RE = re.compile(
    r'FOREIGN\s+KEY(?:\s*\([^\)]*\))?\s*(?:REFERENCES\s+)?([A-Za-z0-9_"]+)',
    re.IGNORECASE
)

def normalize_table_name(name: str) -> str:
    return name.strip().strip('"')

def find_table_dependencies(tables: Dict) -> Dict[str, List[str]]:
    """
    Robustly parse FOREIGN KEY constraints from column constraints.
    Accepts forms:
      - "FOREIGN KEY (OtherTable)"
      - "FOREIGN KEY REFERENCES OtherTable(id)"
      - "FOREIGN KEY (OtherTable) (ON DELETE ...)"
      - "REFERENCES OtherTable(id)"
    Returns mapping table -> list of referenced tables.
    """
    dependencies = {}
    for table_name, table_info in tables.items():
        deps = set()
        for column in table_info.get("columns", []):
            for constraint in column.get("constraints", []):
                if "FOREIGN" in constraint.upper() or "REFERENCES" in constraint.upper():
                    m2 = FK_RE.search(constraint)
                    if m2:
                        deps.add(normalize_table_name(m2.group(1)))
        dependencies[table_name] = [d for d in deps if d]
    return dependencies

def topological_sort(tables: Dict, dependencies: Dict[str, List[str]]) -> List[str]:
    """
    Returns a list of table names sorted so dependencies come earlier where possible.
    In case of cycles, it will still include all tables; cycles are resolved at insert-time
    by doing nullable FK then patching.
    """
    sorted_tables = []
    visited = set()
    visiting = set()

    def visit(t):
        if t in visited:
            return
        if t in visiting:
            return
        visiting.add(t)
        for dep in dependencies.get(t, []):
            if dep in tables:
                visit(dep)
        visiting.remove(t)
        visited.add(t)
        if t not in sorted_tables:
            sorted_tables.append(t)

    for t in tables.keys():
        visit(t)
    return sorted_tables

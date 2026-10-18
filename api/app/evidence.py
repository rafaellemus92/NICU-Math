import re
from typing import Dict

_year_re = re.compile(r'\b(19|20)\d{2}\b')
_n_re = re.compile(r'\bN\s*[=:\-]\s*(\d{2,5})\b', re.I)
_or_rr_re = re.compile(r'\b(OR|RR|HR)\s*[=:\-]\s*([0-9]+\.?[0-9]*)', re.I)
_study_type_re = re.compile(r'\b(randomi[sz]ed|randomized|cohort|case[- ]control|meta[- ]analysis|systematic review|retrospective|prospective)\b', re.I)

def pico_lite(snippet: str) -> Dict[str, str]:
    year = _year_re.search(snippet)
    n = _n_re.search(snippet)
    effect = _or_rr_re.search(snippet)
    stype = _study_type_re.search(snippet)
    return {
        "year": year.group(0) if year else "",
        "n": n.group(1) if n else "",
        "effect": f"{effect.group(1)}={effect.group(2)}" if effect else "",
        "study_type": stype.group(0).title() if stype else ""
    }

import re

wage_test = "Starts at $859.00 for the season. pay based on experience"
def parse_wage(wage_str: str) -> float:
    x = re.findall(r'\d+|\.', wage_str)
    if len(x) > 1:
        avg = sum(x) / len(x)
        return avg
    else:
        return float(x[0]) if x else 0.0
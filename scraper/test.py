import re

wage_test = "Starts at $859.00 for the season. pay based on experience"


def parse_wage(wage_str: str) -> float:
    x = re.findall(r'[\d,\.]+(?<=\d)', wage_str)
    x = [item.replace(',', '') for item in x]
    print(x)
    wages = [float(item) for item in x]
    if len(wages) > 1:
        avg = sum(wages) / len(wages)
        return avg
    else:
        return float(x[0]) if x else 0.0
    
print(parse_wage(wage_test))
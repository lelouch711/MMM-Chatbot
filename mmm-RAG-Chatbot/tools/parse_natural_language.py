import re

def parse_natural_language(query):
    """
    Parses queries like:
    - 'Increase TV spend by 10%'
    - 'Increase TV National by 15%'
    - 'Reallocate 30% of budget to Digital'
    - 'Allocate 40% to TV Regional'
    Returns: formatted string 'channel,sub_channel,value'
    """
    # Try to parse for increase
    inc_match = re.search(
        r'(increase|raise|boost)\s+(\w+)(?:\s+(\w+))?.*?(\d+(\.\d+)?)\s*%', query, re.IGNORECASE
    )
    if inc_match:
        channel = inc_match.group(2)
        sub_channel = inc_match.group(3) or ""
        value = inc_match.group(4)
        return f"{channel},{sub_channel},{value}"

    # Try to parse for reallocate
    realloc_match = re.search(
        r'(reallocate|allocate|put)\s+(\d+(\.\d+)?)\s*%\s*(?:of\s+budget\s*)?(?:to\s+)?(\w+)(?:\s+(\w+))?', query, re.IGNORECASE
    )
    if realloc_match:
        value = float(realloc_match.group(2)) / 100  # convert % to fraction
        channel = realloc_match.group(4)
        sub_channel = realloc_match.group(5) or ""
        return f"{channel},{sub_channel},{value}"

    return "Could not parse your query. Please use a phrase like 'Increase TV spend by 10%' or 'Reallocate 30% to Digital'."

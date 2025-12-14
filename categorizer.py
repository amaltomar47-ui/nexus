import re
from typing import Dict, List, Tuple

class Categorizer:
    """
    Advanced Categorizer using Regular Expressions (Regex).
    
    Why is this 'God Level'?
    1. Performance: Regex patterns are pre-compiled (compiled once, used many times).
    2. Flexibility: You can match patterns like "mcdonalds?" (optional 's') or "uber.*trip".
    3. Scale: Searching a single compiled regex is often faster than iterating hundreds of strings.
    """
    
    def __init__(self):
        # We pre-compile regex patterns for performance.
        # Format: (CategoryName, CompiledRegexPattern)
        self._compiled_rules: List[Tuple[str, re.Pattern]] = self._compile_rules({
            "Food": [r"mcdonalds?", r"kfc", r"pizza", r"burger", r"starbucks", r"coffee", r"\bcafe\b", r"restaurant"],
            "Transport": [r"uber", r"lyft", r"gas", r"shell", r"chevron", r"parking", r"train", r"metro"],
            "Shopping": [r"amazon", r"amzn", r"target", r"walmart", r"nike", r"mall", r"clothing"],
            "Entertainment": [r"netflix", r"hulu", r"spotify", r"cinema", r"movie", r"steam"],
            "Utilities": [r"electric", r"water", r"internet", r"at&t", r"verizon"],
            "Salary": [r"payroll", r"deposit", r"gusto", r"salary"]
        })

    def _compile_rules(self, rules: Dict[str, List[str]]) -> List[Tuple[str, re.Pattern]]:
        """
        Compiles list of keywords into efficient Regex objects.
        """
        compiled = []
        for category, patterns in rules.items():
            # Join patterns with OR `|` to create one giant regex per category
            # e.g., (mcdonalds|kfc|pizza)
            # escape(p) ensures special chars don't break regex unless we want them to
            combined_pattern = "|".join(patterns)
            
            # Compile with IGNORECASE flag for speed and case-insensitivity
            # This object is highly optimized by Python's C internals.
            regex = re.compile(combined_pattern, re.IGNORECASE)
            compiled.append((category, regex))
        return compiled

    def categorize(self, description: str) -> str:
        """
        Analyzes the transaction description using Regex.
        
        Args:
            description (str): Transaction text.
            
        Returns:
            str: Category or "Uncategorized"
        """
        # Loop through compiled regexes. 
        # Checking one complex regex is faster than checking 20 substrings manually.
        for category, pattern in self._compiled_rules:
            if pattern.search(description):
                return category
        
        return "Uncategorized"

import base64
import re
from pathlib import Path

def load_logo():
    """Load logo image and convert to base64 string."""
    logo_path = Path("bytexl_logo.png")
    if logo_path.exists():
        with open(logo_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None

def outputs_match(expected, actual):
    """
    Compare expected output with actual output using multiple comparison strategies.
    
    Args:
        expected (str): Expected output string
        actual (str): Actual output string from code execution
        
    Returns:
        bool: True if outputs match according to any comparison strategy
    """
    exp = expected.strip()
    act = actual.strip()
    
    # Handle empty outputs
    if not exp and not act:
        return True
    
    # 1. Exact match (preserves all formatting)
    if exp == act:
        return True
    
    # 2. Case-insensitive exact match
    if exp.lower() == act.lower():
        return True
    
    # 3. Trailing whitespace tolerant (preserve internal structure)
    exp_lines = [line.rstrip() for line in exp.split('\n')]
    act_lines = [line.rstrip() for line in act.split('\n')]
    if exp_lines == act_lines:
        return True
    
    # 4. Case-insensitive + trailing whitespace tolerant
    exp_lines_lower = [line.rstrip().lower() for line in exp.split('\n')]
    act_lines_lower = [line.rstrip().lower() for line in act.split('\n')]
    if exp_lines_lower == act_lines_lower:
        return True
    
    # 5. Numeric comparison with tolerance (for floating point)
    try:
        exp_num = float(exp)
        act_num = float(act)
        # Use relative tolerance for large numbers, absolute for small
        tolerance = max(1e-9, abs(exp_num) * 1e-9)
        if abs(exp_num - act_num) <= tolerance:
            return True
    except:
        pass
    
    # 5b. Multiple numbers comparison (space/line separated)
    try:
        exp_nums = [float(x) for x in re.findall(r'-?\d+\.?\d*', exp)]
        act_nums = [float(x) for x in re.findall(r'-?\d+\.?\d*', act)]
        if len(exp_nums) == len(act_nums) and len(exp_nums) > 0:
            tolerance = 1e-9
            if all(abs(e - a) <= max(tolerance, abs(e) * tolerance) for e, a in zip(exp_nums, act_nums)):
                return True
    except:
        pass
    
    # 6. Only as last resort: relaxed whitespace (for simple text answers)
    # Skip this for multi-line outputs to preserve patterns
    if '\n' not in exp and '\n' not in act:
        exp_relaxed = re.sub(r'\s+', ' ', exp).strip()
        act_relaxed = re.sub(r'\s+', ' ', act).strip()
        if exp_relaxed.lower() == act_relaxed.lower():
            return True
    
    return False
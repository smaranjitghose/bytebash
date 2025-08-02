import streamlit as st
import sys
from io import StringIO
import base64
from pathlib import Path

# Load logo as base64
def load_logo():
    logo_path = Path("bytexl_logo.png")
    if logo_path.exists():
        with open(logo_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None

logo_base64 = load_logo()

st.set_page_config(page_title="ByteBash v1 Py 🐍", page_icon="🚀", layout="wide")

# Title & caption
st.title("🚀 ByteBash v1 Py")
st.caption("A python code validation tool built by Smaranjit Ghose")

# Example problems
EXAMPLE_PROBLEMS = {
    "Beginner: Sum of Two Numbers": {
        "description": "Read two integers and calculate their sum - Entry level problem for new learners",
        "code": "# Read two integers and print their sum\na = int(input())\nb = int(input())\nprint(a + b)",
        "test_cases": [
            ("5\n3", "8"),
            ("10\n-2", "8"),
            ("0\n0", "0"),
            ("-5\n7", "2"),
            ("100\n200", "300"),
            ("15\n-15", "0"),
            ("999\n1", "1000")
        ]
    },
    "Intermediate: Even or Odd": {
        "description": "Determine if a given number is even or odd - Logic and conditionals practice",
        "code": "# Check if a number is even or odd\nn = int(input())\nif n % 2 == 0:\n    print(\"Even\")\nelse:\n    print(\"Odd\")",
        "test_cases": [
            ("4", "Even"),
            ("7", "Odd"),
            ("0", "Even"),
            ("1", "Odd"),
            ("100", "Even"),
            ("999", "Odd"),
            ("-2", "Even")
        ]
    },
    "Advanced: Maximum of Three": {
        "description": "Find the largest among three numbers - Multiple comparisons and edge case handling",
        "code": "# Find the maximum of three numbers\na = int(input())\nb = int(input())\nc = int(input())\nprint(max(a, b, c))",
        "test_cases": [
            ("5\n8\n3", "8"),
            ("10\n10\n10", "10"),
            ("1\n2\n3", "3"),
            ("100\n50\n75", "100"),
            ("-1\n-5\n-3", "-1"),
            ("0\n1\n-1", "1"),
            ("999\n1000\n998", "1000")
        ]
    }
}

# Output comparison function
def outputs_match(expected, actual):
    exp = expected.strip()
    act = actual.strip()
    if exp.lower() == act.lower():
        return True
    try:
        if float(exp) == float(act):
            return True
    except:
        pass
    return False

# Initialize session state
if 'test_cases' not in st.session_state:
    st.session_state.test_cases = [("", "") for _ in range(7)]

# Dark-mode friendly styles & scroll styling
st.markdown("""
<style>
.test-case-header {
    background: linear-gradient(90deg, #444 0%, #333 100%);
    padding: 6px 10px;
    border-radius: 6px;
    border-left: 4px solid #ff4b4b;
    margin: 8px 0;
    font-weight: 600;
    color: #fff;
}
.stTextArea > div > div > textarea {
    background-color: #1e1e1e !important;
    border: 1px solid #555 !important;
    border-radius: 6px !important;
    color: #eaeaea !important;
    font-family: 'Courier New', monospace !important;
    font-size: 14px !important;
}
.stTextArea > div > div > textarea:focus {
    border-color: #ff4b4b !important;
    box-shadow: 0 0 0 1px rgba(255, 75, 75, 0.4) !important;
}
.scrollable-test-cases {
    max-height: 520px;
    overflow-y: auto;
    padding-right: 8px;
}
.scrollable-test-cases::-webkit-scrollbar {
    width: 8px;
}
.scrollable-test-cases::-webkit-scrollbar-thumb {
    background: #555;
    border-radius: 4px;
}
.scrollable-test-cases::-webkit-scrollbar-thumb:hover {
    background: #777;
}
</style>
""", unsafe_allow_html=True)

# Layout with adjusted column ratio
col_code, col_tests = st.columns([1.2, 0.8])

# Code column
with col_code:
    st.subheader("Your Solution")
    col_example, col_clear = st.columns([3, 1])
    with col_example:
        selected_example = st.selectbox(
            "Load Example Problem:",
            ["Select an example..."] + list(EXAMPLE_PROBLEMS.keys()),
            key="example_selector"
        )
        if st.button("📥 Load Example") and selected_example != "Select an example...":
            problem = EXAMPLE_PROBLEMS[selected_example]
            st.session_state.code = problem["code"]
            st.session_state.test_cases = problem["test_cases"]
            st.session_state.example_description = problem["description"]
            st.rerun()
    with col_clear:
        if st.button("🗑️ Clear All"):
            st.session_state.code = ""
            st.session_state.test_cases = [("", "") for _ in range(7)]
            if 'example_description' in st.session_state:
                del st.session_state.example_description
            st.rerun()

    if 'example_description' in st.session_state:
        st.info(f"**Problem:** {st.session_state.example_description}")

    code = st.text_area(
        "Enter your Python code here:",
        height=400,
        placeholder="# Example:\na = int(input())\nb = int(input())\nprint(a+b)",
        value=st.session_state.get('code', ''),
        key="code_input"
    )

# Test case column
with col_tests:
    st.subheader("Test Cases")
    run_tests = st.button("▶️ Run Tests", type="primary")

    st.markdown('<div class="scrollable-test-cases">', unsafe_allow_html=True)
    test_cases = []
    for i in range(7):
        st.markdown(f'<div class="test-case-header">Test Case {i+1}</div>', unsafe_allow_html=True)
        default_input = st.session_state.test_cases[i][0]
        default_output = st.session_state.test_cases[i][1]
        test_input = st.text_area(
            f"Input {i+1}:",
            height=80,
            key=f"input_{i}",
            placeholder="One input per line",
            value=default_input
        )
        expected_output = st.text_area(
            f"Expected Output {i+1}:",
            height=80,
            key=f"expected_{i}",
            placeholder="Expected output here",
            value=default_output
        )
        test_cases.append((test_input, expected_output))
    st.markdown('</div>', unsafe_allow_html=True)

# Run tests logic
if run_tests:
    if not code.strip():
        st.error("Please enter your Python code first.")
    else:
        results, passed_count = [], 0
        for idx, (test_input, expected_output) in enumerate(test_cases, start=1):
            old_stdout = sys.stdout
            sys.stdout = StringIO()
            try:
                input_lines = iter(test_input.strip().split('\n')) if test_input.strip() else iter([])
                def mock_input(prompt=""):
                    try:
                        return next(input_lines)
                    except StopIteration:
                        return ""
                namespace = {"input": mock_input, "__builtins__": __builtins__}
                exec(code, namespace)
                output = sys.stdout.getvalue().strip()
                passed = outputs_match(expected_output, output)
                if passed:
                    passed_count += 1
                results.append((test_input, expected_output, output, passed))
            except Exception as e:
                results.append((test_input, expected_output, f"Error: {e}", False))
            finally:
                sys.stdout = old_stdout

        # Summary
        st.subheader(f"Results: {passed_count}/7 Tests Passed")
        if passed_count == 7:
            st.success(f"🎉 All tests passed! Great job!")
        elif passed_count >= 5:
            st.warning(f"⚠️ {passed_count} out of 7 tests passed. Almost there!")
        else:
            st.error(f"❌ {passed_count} out of 7 tests passed. Keep trying!")

        # Details
        for idx, (inp, exp, out, passed) in enumerate(results, start=1):
            status = "✅ Passed" if passed else "❌ Failed"
            with st.expander(f"Test Case {idx} — {status}", expanded=not passed):
                col_inp, col_exp, col_act = st.columns(3)
                col_inp.write("**Input:**")
                col_inp.code(inp if inp else "(no input)", language="text")
                col_exp.write("**Expected:**")
                col_exp.code(exp if exp else "(no expected output)", language="text")
                col_act.write("**Actual:**")
                col_act.code(out if out else "(no output)", language="text")

# Footer
st.markdown("---")
col_tips, col_branding = st.columns([2, 1])
with col_tips:
    st.markdown("""
    **💡 Development Tips:**
    - Use `input()` for interactive problems
    - Use `print()` for outputs
    - Match the expected format exactly
    """)
with col_branding:
    if logo_base64:
        st.markdown(f"""
        <div style="
            text-align: center;
            font-family: 'Segoe UI', sans-serif;
            padding: 10px;
            border-radius: 10px;
            border: 1px solid rgba(128,128,128,0.3);
            backdrop-filter: blur(4px);
        ">
            <img src="data:image/png;base64,{logo_base64}" 
                 style="width: 120px; margin-bottom: 8px;">
            <div style="font-size: 18px; font-weight: 600;">🏢 ByteXL Internal Tool</div>
            <div style="font-size: 14px;">Version: 1.0</div>
            <div style="font-size: 14px; color: #aaa;">Validating code. Empowering content.</div>
        </div>
        """, unsafe_allow_html=True)

# Save state
if code != st.session_state.get('code', ''):
    st.session_state.code = code
for i, (inp, exp) in enumerate(test_cases):
    st.session_state.test_cases[i] = (inp, exp)

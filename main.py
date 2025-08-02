import streamlit as st
import sys
from io import StringIO
import base64
from pathlib import Path

# Convert local image to base64 so it can be embedded in HTML
def load_logo():
    logo_path = Path("bytexl_logo.png")
    if logo_path.exists():
        with open(logo_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None

logo_base64 = load_logo()

st.set_page_config(page_title="ByteBash v1 Py 🐍", page_icon="🚀", layout="wide")

# App Title with ByteXL branding
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

# Simple flexible match function
def outputs_match(expected, actual):
    exp = expected.strip()
    act = actual.strip()

    # Ignore case for comparison
    if exp.lower() == act.lower():
        return True

    # Try numeric comparison
    try:
        if float(exp) == float(act):
            return True
    except:
        pass

    return False

# Initialize session state for test cases if not exists
if 'test_cases' not in st.session_state:
    st.session_state.test_cases = [("", "") for _ in range(7)]

# Split into two columns
col_code, col_tests = st.columns([1, 1])

with col_code:
    st.subheader("Your Solution")
    
    # Example problems dropdown and load button
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
    
    # Show example description if loaded
    if 'example_description' in st.session_state:
        st.info(f"**Problem:** {st.session_state.example_description}")
    
    code = st.text_area(
        "Enter your Python code here:",
        height=400,
        placeholder="# Example:\na = int(input())\nb = int(input())\nprint(a+b)",
        value=st.session_state.get('code', ''),
        key="code_input"
    )

with col_tests:
    st.subheader("Test Cases")
    run_tests = st.button("▶️ Run Tests", type="primary")  # Button at top of test case section
    
    # Add custom CSS for scrollable container
    st.markdown("""
    <style>
    .test-cases-container {
        max-height: 600px;
        overflow-y: auto;
        padding: 15px;
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        background-color: #fafafa;
        margin: 10px 0;
    }
    .test-cases-container::-webkit-scrollbar {
        width: 8px;
    }
    .test-cases-container::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 4px;
    }
    .test-cases-container::-webkit-scrollbar-thumb {
        background: #c1c1c1;
        border-radius: 4px;
    }
    .test-cases-container::-webkit-scrollbar-thumb:hover {
        background: #a8a8a8;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Create scrollable container using st.container with height
    with st.container(height=600):
        test_cases = []
        for i in range(7):
            st.write(f"**Test Case {i+1}**")
            
            # Use session state values if they exist
            default_input = st.session_state.test_cases[i][0] if i < len(st.session_state.test_cases) else ""
            default_output = st.session_state.test_cases[i][1] if i < len(st.session_state.test_cases) else ""
            
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

# Run logic
if run_tests:
    if not code.strip():
        st.error("Please enter your Python code first.")
    else:
        results = []
        passed_count = 0
        
        for idx, (test_input, expected_output) in enumerate(test_cases, start=1):
            old_stdout = sys.stdout
            sys.stdout = StringIO()
            try:
                input_lines = iter(test_input.strip().split('\n')) if test_input.strip() else iter([])

                def mock_input(prompt=""):
                    try:
                        value = next(input_lines)
                        return value
                    except StopIteration:
                        return ""
                        
                namespace = {"input": mock_input, "__builtins__": __builtins__}
                exec(code, namespace)
                output = sys.stdout.getvalue().strip()

                # Flexible match check
                passed = outputs_match(expected_output, output)
                if passed:
                    passed_count += 1
                results.append((test_input, expected_output, output, passed))
            except Exception as e:
                results.append((test_input, expected_output, f"Error: {e}", False))
            finally:
                sys.stdout = old_stdout

        # Display score prominently
        st.subheader(f"Results: {passed_count}/7 Tests Passed")
        
        # Score color coding
        if passed_count == 7:
            st.success(f"🎉 All tests passed! Great job!")
        elif passed_count >= 5:
            st.warning(f"⚠️ {passed_count} out of 7 tests passed. Almost there!")
        else:
            st.error(f"❌ {passed_count} out of 7 tests passed. Keep trying!")

        # Detailed results
        for idx, (inp, exp, out, passed) in enumerate(results, start=1):
            status = "✅ Passed" if passed else "❌ Failed"
            
            with st.expander(f"Test Case {idx} — {status}", expanded=not passed):
                col_inp, col_exp, col_act = st.columns(3)
                
                with col_inp:
                    st.write("**Input:**")
                    st.code(inp if inp else "(no input)", language="text")
                
                with col_exp:
                    st.write("**Expected:**")
                    st.code(exp if exp else "(no expected output)", language="text")
                
                with col_act:
                    st.write("**Actual:**")
                    st.code(out if out else "(no output)", language="text")

# Footer with ByteXL branding and tips
st.markdown("---")
col_tips, col_branding = st.columns([2, 1])

with col_tips:
    st.markdown("""
    **💡 Development Tips:**
    - Use `input()` to read user input for interactive problems
    - Print your output using `print()` statements
    - Test with provided examples to understand the format
    - Ensure output format exactly matches expected results
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
            <div style="font-size: 18px; font-weight: 600; margin-bottom: 4px;">
                🏢 ByteXL Internal Tool
            </div>
            <div style="font-size: 14px; font-weight: normal; margin-top: 2px;">
                Version: 1.0
            </div>
            <div style="font-size: 14px; color: #666; margin-top: 2px;">
                Validating code. Empowering content.
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        # Fallback when logo is not available
        st.markdown("""
        **🏢 ByteXL Internal Tool**  
        *Content Strategy Team*  
        ByteBash v1 Py | 2025
        """)

# Team information
st.markdown("---")
st.info("🎯 **For ByteXL Team:** This tool helps validate coding solutions for our educational content. Use it to test problem sets before publishing to students.")

# Save current state
if code != st.session_state.get('code', ''):
    st.session_state.code = code

# Update test cases in session state
for i, (inp, exp) in enumerate(test_cases):
    if i < len(st.session_state.test_cases):
        st.session_state.test_cases[i] = (inp, exp)
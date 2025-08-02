# main.py - Main application for ByteBash v1 Py

import streamlit as st
import sys
from io import StringIO
from streamlit_ace import st_ace
from problems import EXAMPLE_PROBLEMS
from utils import load_logo, outputs_match, truncate_output

def main():
    logo_base64 = load_logo()

    st.set_page_config(page_title="ByteBash v1 Py 🐍", page_icon="🚀", layout="wide")

    # Title & caption
    st.title("🚀 ByteBash v1 Py")
    st.caption("A python code validation tool built by Smaranjit Ghose")

    # Initialize session state
    if 'test_cases' not in st.session_state:
        st.session_state.test_cases = [("", "") for _ in range(7)]
    if 'editor_key' not in st.session_state:
        st.session_state.editor_key = "code_editor_0"
    if 'current_code' not in st.session_state:
        st.session_state.current_code = ""
    if 'num_test_cases' not in st.session_state:
        st.session_state.num_test_cases = 7

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
    /* Style the ace editor container to match the dark theme */
    .ace_editor {
        border: 1px solid #555 !important;
        border-radius: 6px !important;
    }
    .ace_gutter {
        background: #2d2d2d !important;
        border-right: 1px solid #555 !important;
    }
    </style>
    """, unsafe_allow_html=True)

    # Sidebar for Problem Selection
    with st.sidebar:
        st.header("Problem Selection")
        
        selected_example = st.selectbox(
            "Load Example Problem:",
            ["Select an example..."] + list(EXAMPLE_PROBLEMS.keys()),
            key="example_selector"
        )
        
        if st.button("📥 Load Example") and selected_example != "Select an example...":
            problem = EXAMPLE_PROBLEMS[selected_example]
            st.session_state.current_code = problem["code"]
            st.session_state.test_cases = problem["test_cases"]
            st.session_state.num_test_cases = len(problem["test_cases"])
            st.session_state.example_description = problem["description"]
            # Change the editor key to force recreation
            current_key_num = int(st.session_state.editor_key.split("_")[-1])
            st.session_state.editor_key = f"code_editor_{current_key_num + 1}"
            st.rerun()
        
        if st.button("🗑️ Clear All"):
            st.session_state.current_code = ""
            st.session_state.test_cases = [("", "") for _ in range(7)]
            st.session_state.num_test_cases = 7
            if 'example_description' in st.session_state:
                del st.session_state.example_description
            # Change the editor key to force recreation
            current_key_num = int(st.session_state.editor_key.split("_")[-1])
            st.session_state.editor_key = f"code_editor_{current_key_num + 1}"
            st.rerun()

    # Layout with adjusted column ratio
    col_code, col_tests = st.columns([1.2, 0.8])

    # Code column
    with col_code:
        st.subheader("Your Solution")

        if 'example_description' in st.session_state:
            st.info(f"**Problem:** {st.session_state.example_description}")

        st.write("**Enter your Python code:**")
        code = st_ace(
            value=st.session_state.current_code,
            language='python',
            theme='monokai',
            key=st.session_state.editor_key,  # Dynamic key
            height=400,
            auto_update=True,
            font_size=14,
            tab_size=4,
            show_gutter=True,
            show_print_margin=True,
            wrap=False,
            annotations=None
        )
        
        # Update current_code when user types
        st.session_state.current_code = code

    # Test case column
    with col_tests:
        st.subheader("Test Cases")
        
        # Test case management controls
        col_controls1, col_controls2, col_controls3 = st.columns([1, 1, 1])
        
        with col_controls1:
            if st.button("➕ Add Test Case"):
                st.session_state.test_cases.append(("", ""))
                st.session_state.num_test_cases += 1
                st.rerun()
        
        with col_controls2:
            if st.button("➖ Remove Test Case") and st.session_state.num_test_cases > 2:
                st.session_state.test_cases.pop()
                st.session_state.num_test_cases -= 1
                st.rerun()
        
        with col_controls3:
            run_tests = st.button("▶️ Run Tests", type="primary")
        
        # Display current count
        st.caption(f"Total Test Cases: {st.session_state.num_test_cases} (Min: 2)")

        st.markdown('<div class="scrollable-test-cases">', unsafe_allow_html=True)
        test_cases = []
        
        # Ensure we have at least the current number of test cases in session state
        while len(st.session_state.test_cases) < st.session_state.num_test_cases:
            st.session_state.test_cases.append(("", ""))
        
        # Display test cases dynamically
        for i in range(st.session_state.num_test_cases):
            st.markdown(f'<div class="test-case-header">Test Case {i+1}</div>', unsafe_allow_html=True)
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
                    raw_output = sys.stdout.getvalue()
                    output = truncate_output(raw_output).strip()
                    passed = outputs_match(expected_output, output)
                    if passed:
                        passed_count += 1
                    results.append((test_input, expected_output, output, passed))
                except Exception as e:
                    results.append((test_input, expected_output, f"Error: {e}", False))
                finally:
                    sys.stdout = old_stdout

            # Summary
            total_tests = len(test_cases)
            st.subheader(f"Results: {passed_count}/{total_tests} Tests Passed")
            if passed_count == total_tests:
                st.success(f"🎉 All {total_tests} tests passed! Great job!")
            elif passed_count >= total_tests * 0.7:  # 70% threshold
                st.warning(f"⚠️ {passed_count} out of {total_tests} tests passed. Almost there!")
            else:
                st.error(f"❌ {passed_count} out of {total_tests} tests passed. Keep trying!")

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
                    
                    # Color-coded output based on pass/fail
                    if passed:
                        # Green background for passed tests
                        col_act.markdown(f"""
                        <div style="
                            background-color: rgba(0, 255, 0, 0.1);
                            border-left: 4px solid #00ff00;
                            padding: 10px;
                            border-radius: 5px;
                            font-family: monospace;
                            white-space: pre-wrap;
                        ">{out if out else "(no output)"}</div>
                        """, unsafe_allow_html=True)
                    else:
                        # Red background for failed tests
                        col_act.markdown(f"""
                        <div style="
                            background-color: rgba(255, 0, 0, 0.1);
                            border-left: 4px solid #ff0000;
                            padding: 10px;
                            border-radius: 5px;
                            font-family: monospace;
                            white-space: pre-wrap;
                            color: #ff4444;
                        ">{out if out else "(no output)"}</div>
                        """, unsafe_allow_html=True)

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
                <div style="font-size: 14px;">Version: 1.6</div>
                <div style="font-size: 14px; color: #aaa;">Validating code. Empowering content.</div>
            </div>
            """, unsafe_allow_html=True)

    # Save state - code is already saved above
    for i, (inp, exp) in enumerate(test_cases):
        if i < len(st.session_state.test_cases):
            st.session_state.test_cases[i] = (inp, exp)

if __name__ == "__main__":
    main()
import io
import sys
import traceback
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

def execute_user_code(df, code):
    local_vars = {"df": df, "plt": plt, "sns": sns}
    stdout = io.StringIO()
    sys_stdout = sys.stdout
    sys.stdout = stdout

    result = None  # Default result

    try:
        # Check if it's a single-line evaluable expression
        if code.strip().startswith(("import", "def", "for", "if", "while", "plt", "sns")) or "\n" in code:
            raise SyntaxError("Treating as statement block")

        compiled_code = compile(code, "<string>", "eval")
        result = eval(compiled_code, {}, local_vars)

    except SyntaxError:
        try:
            compiled_code = compile(code, "<string>", "exec")
            exec(compiled_code, {}, local_vars)

            # If any figure is created, show it
            if plt.get_fignums():
                st.pyplot(plt.gcf())
                plt.clf()  # Clear for next chart
                result = None  # No need to return additional output
            else:
                output = stdout.getvalue().strip()
                result = output if output else "✅ Code executed successfully."

        except Exception:
            result = f"❌ Error during execution:\n{traceback.format_exc()}"

    except Exception:
        result = f"❌ Error during evaluation:\n{traceback.format_exc()}"

    finally:
        sys.stdout = sys_stdout

    return result

import io
import sys
import traceback
import matplotlib.pyplot as plt
import seaborn as sns

def execute_user_code(df, code):
    local_vars = {"df": df, "plt": plt, "sns": sns}
    stdout = io.StringIO()
    sys_stdout = sys.stdout
    sys.stdout = stdout

    try:
        # Treat as evaluable expression unless it's a known statement
        if code.strip().startswith(("import", "def", "for", "if", "while", "plt", "sns")) or "\n" in code:
            raise SyntaxError("Treating as statement block")

        compiled_code = compile(code, "<string>", "eval")
        result = eval(compiled_code, {}, local_vars)

    except SyntaxError:
        try:
            compiled_code = compile(code, "<string>", "exec")
            exec(compiled_code, {}, local_vars)

            if plt.get_fignums():  # Check if any figure was generated
                fig = plt.gcf()
                result = fig
                plt.clf()  # Clear the figure after capturing it
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

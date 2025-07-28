from jinja2 import Template
import os

def generate_report(questions_answers: list, summary: dict, save_path="outputs/report.md"):
    # Read the template with UTF-8 encoding
    with open("templates/report_template.md", "r", encoding="utf-8") as f:
        template = Template(f.read())

    rendered = template.render(summary=summary, interactions=questions_answers)

    # Write the rendered markdown with UTF-8 encoding
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    with open(save_path, "w", encoding="utf-8") as f:
        f.write(rendered)

    return save_path

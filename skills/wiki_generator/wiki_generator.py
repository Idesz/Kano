import json
import os

class WikiGenerator:
    def execute(self, project_name: str, roadmap: dict, skills: list):
        wiki_dir = f"wiki/{project_name}"
        os.makedirs(wiki_dir, exist_ok=True)

        html_content = f"""
        <html>
        <head><title>{project_name} Wiki</title></head>
        <body style="background: #000; color: #0f0; font-family: monospace;">
            <h1>{project_name} - Project Wiki</h1>
            <h2>Roadmap</h2>
            <pre>{json.dumps(roadmap, indent=4)}</pre>
            <h2>Available Skills</h2>
            <ul>
                {"".join([f"<li>{s['name']}: {s['description']}</li>" for s in skills])}
            </ul>
        </body>
        </html>
        """

        with open(os.path.join(wiki_dir, "index.html"), "w") as f:
            f.write(html_content)

        return f"Wiki generated at {wiki_dir}/index.html"

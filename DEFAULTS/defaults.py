EDITOR = "nvim"  # Change this to your preferred editor command (e.g., "code", "nano", "vim", etc.)

DEFAULT_TODO_TEMPLATE = """# TODO

## High Priority
- [x] (This is a template)
- [ ] (This is a template)

## Medium Priority
- [x] (This is a template)
- [ ] (This is a template)

## Low Priority
- [x] (This is a template)
- [ ] (This is a template)
"""

DEFAULT_ISSUES_TRACKER = {
    "issues": [
        {
            "id": 0,
            "title": "This is a template issue",
            "status": "open/closed",
            "priority": "high/medium/low",
            "created": "YYYY-MM-DD",
            "labels": ["bug/feature/enhancement"],
            "assignee": "username/undifined",
            "description": "This is a template issue description. You can provide more details about the issue here, including steps to reproduce, expected behavior, and any relevant screenshots or logs.",
        }
    ]
}

DEFAULT_PROJECT_METADATA = {
    "project": {
        "name": " ",
        "description": " ",
        "language": " ",
        "version": " ",
        "license": " ",
        "author": " ",
        "created": "YYYY-MM-DD",
    },
    "dependencies": [{"name": " ", "version": " "}, {"name": " ", "version": " "}],
}

DEFAULT_PROJECT_INDEX_HTML = r"""<!doctype html>
<html lang="en">

<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Project</title>
    <link rel="stylesheet" href="../styles.css" />
    <style>
        body {
            min-height: 100vh;
        }

        .page {
            display: grid;
            grid-template-columns: 25% minmax(0, 1fr) 33%;
            gap: 1.5rem;
            padding: 2rem 0rem;
            max-width: 90%;
            margin: 0 auto;
            align-items: start;
        }

        .project-info {
            display: flex;
            flex-direction: column;
            gap: 1.5rem;
        }

        .project-info h1 {
            margin: 0;
            font-size: 1.6rem;
            font-weight: 600;
            word-break: break-word;
        }

        .project-info .description {
            margin: 0;
            color: var(--text-dim);
            line-height: 1.5;
        }

        dl.meta {
            margin: 0;
            display: flex;
            flex-direction: column;
            gap: 0.7rem;
        }

        dl.meta div {
            display: flex;
            justify-content: space-between;
            gap: 0.75rem;
            border-bottom: 1px solid var(--border);
            padding-bottom: 0.5rem;
        }

        dl.meta dt {
            color: var(--text-dim);
            font-size: 0.85rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }

        dl.meta dd {
            margin: 0;
            font-weight: 500;
            text-align: right;
            word-break: break-word;
        }

        .deps-section h2,
        .card h2 {
            font-size: 1rem;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            color: var(--text-dim);
            margin: 0 0 1rem;
        }

        .deps-section ul {
            list-style: none;
            margin: 0;
            padding: 0;
            display: flex;
            flex-direction: column;
            gap: 0.4rem;
        }

        .deps-section li {
            display: flex;
            justify-content: space-between;
            font-size: 0.9rem;
        }

        .back-link {
            color: var(--accent);
            text-decoration: none;
            font-size: 0.9rem;
            margin-top: auto;
            padding-top: 1rem;
        }

        .back-link:hover {
            text-decoration: underline;
        }

        .card {
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 14px;
            padding: 1.5rem 1.7rem;
        }

        .issues-card h2,
        .readme-card h2,
        .todo-card h2 {
            text-align: center;
            font-size: 1.3rem;
            text-transform: none;
            letter-spacing: normal;
            color: var(--text);
            margin-bottom: 1.5rem;
        }

        .todo-card h3 {
            font-size: 1.05rem;
            font-weight: 600;
            margin: 1.5rem 0 0.75rem;
        }

        .todo-card h3:first-of-type {
            margin-top: 0;
        }

        .todo-columns {
            display: grid;
            gap: 2rem;
        }

        .todo-column h3 {
            font-size: 1.05rem;
            font-weight: 600;
            margin: 0 0 0.75rem;
            text-align: center;
        }

        .todo-extra {
            margin-top: 1.5rem;
            border-top: 1px solid var(--border);
            padding-top: 1rem;
        }

        @media (max-width: 640px) {
            .todo-columns {
                grid-template-columns: 1fr;
            }
        }

        ul.todo-list {
            list-style: none;
            margin: 0 0 0.5rem;
            padding: 0;
            display: flex;
            flex-direction: column;
            gap: 0.6rem;
        }

        ul.todo-list li {
            display: flex;
            align-items: flex-start;
            gap: 0.6rem;
            line-height: 1.4;
        }

        ul.todo-list li .checkbox {
            flex-shrink: 0;
        }

        ul.todo-list li.done {
            color: var(--text-dim);
            text-decoration: line-through;
        }

        .right-col {
            display: flex;
            flex-direction: column;
            gap: 1.5rem;
        }

        .issues-card,
        .readme-card {
            max-height: 420px;
            overflow-y: auto;
        }

        details.issue {
            border-bottom: 1px solid var(--border);
            padding: 0.75rem 0;
        }

        details.issue:last-child {
            border-bottom: none;
        }

        details.issue summary {
            cursor: pointer;
            display: flex;
            align-items: center;
            flex-wrap: wrap;
            gap: 0.5rem;
            list-style: none;
        }

        details.issue summary::-webkit-details-marker {
            display: none;
        }

        .issue-title {
            font-weight: 500;
        }

        .pill {
            font-size: 0.72rem;
            padding: 0.15rem 0.55rem;
            border-radius: 999px;
            border: 1px solid var(--border);
            color: var(--text-dim);
            text-transform: capitalize;
        }

        .pill.status-open {
            color: #7ee787;
            border-color: #2ea44344;
        }

        .pill.status-closed {
            color: #f85149;
            border-color: #f8514944;
        }

        .pill.priority-high {
            color: #f85149;
        }

        .pill.priority-medium {
            color: #e3b341;
        }

        .pill.priority-low {
            color: #6ea8fe;
        }

        .issue-body {
            margin-top: 0.5rem;
            color: var(--text-dim);
            font-size: 0.9rem;
            display: flex;
            flex-direction: column;
            gap: 0.5rem;
        }

        .issue-body p {
            margin: 0;
        }

        .issue-meta {
            display: flex;
            flex-wrap: wrap;
            align-items: center;
            gap: 0.4rem;
            font-size: 0.8rem;
        }

        .chip {
            background: var(--surface-hover);
            border: 1px solid var(--border);
            border-radius: 6px;
            padding: 0.1rem 0.5rem;
            font-size: 0.75rem;
        }

        .readme-card h1,
        .readme-card h3 {
            margin: 1.2rem 0 0.5rem;
        }

        .readme-card h1:first-child,
        .readme-card h2:first-child,
        .readme-card h3:first-child {
            margin-top: 0;
        }

        .readme-card p {
            margin: 0 0 0.75rem;
            line-height: 1.5;
            color: var(--text);
        }

        .readme-card ul {
            margin: 0 0 0.75rem;
            padding-left: 1.3rem;
        }

        .readme-card code {
            background: var(--surface-hover);
            border-radius: 4px;
            padding: 0.1rem 0.35rem;
            font-size: 0.9em;
        }

        .readme-card pre {
            background: var(--surface-hover);
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 0.8rem;
            overflow-x: auto;
        }

        .readme-card pre code {
            background: none;
            padding: 0;
        }

        .dim {
            color: var(--text-dim);
        }

        .load-error {
            font-size: 0.85rem;
            line-height: 1.5;
        }

        @media (max-width: 980px) {
            .page {
                grid-template-columns: 1fr;
                padding: 1.5rem;
            }

            .issues-card,
            .readme-card {
                max-height: none;
            }
        }
    </style>
</head>

<body>
    <div class="page">
        <aside class="project-info">
            <div>
                <h1 id="proj-name">Project name</h1>
                <p class="description" id="proj-desc">Project description</p>
            </div>

            <dl class="meta">
                <div>
                    <dt>language</dt>
                    <dd id="meta-language">—</dd>
                </div>
                <div>
                    <dt>version</dt>
                    <dd id="meta-version">—</dd>
                </div>
                <div>
                    <dt>license</dt>
                    <dd id="meta-license">—</dd>
                </div>
                <div>
                    <dt>author</dt>
                    <dd id="meta-author">—</dd>
                </div>
                <div>
                    <dt>created</dt>
                    <dd id="meta-created">—</dd>
                </div>
            </dl>

            <div class="deps-section" id="deps-section">
                <h2>Dependencies</h2>
                <ul id="deps-list"></ul>
            </div>

            <a class="back-link" href="../WebUI.html">&larr; All projects</a>
        </aside>

        <section class="card todo-card">
            <h2>TODO</h2>
            <div id="todo-content"></div>
        </section>

        <div class="right-col">
            <section class="card issues-card">
                <h2>Issues</h2>
                <div id="issues-content"></div>
            </section>

            <section class="card readme-card">
                <h2>README.md</h2>
                <div id="readme-content"></div>
            </section>
        </div>
    </div>

    <script>
        function escapeHtml(str) {
            return String(str ?? "").replace(
                /[&<>"']/g,
                (c) =>
                    ({
                        "&": "&amp;",
                        "<": "&lt;",
                        ">": "&gt;",
                        '"': "&quot;",
                        "'": "&#39;",
                    })[c],
            );
        }

        function setText(id, value) {
            document.getElementById(id).textContent = value;
        }

        function setHtml(id, value) {
            document.getElementById(id).innerHTML = value;
        }

        function loadErrorMessage(filename) {
            return (
                '<p class="dim load-error">Couldn\'t load ' +
                escapeHtml(filename) +
                ". If you're opening this page directly from disk, browsers " +
                "block that kind of local file access. Serve the folder with " +
                "a local server (e.g. <code>python -m http.server</code>) and " +
                "open it through http://localhost instead.</p>"
            );
        }

        async function loadJson(path) {
            const res = await fetch(path);
            if (!res.ok) throw new Error(`${path}: ${res.status}`);
            return res.json();
        }

        async function loadText(path) {
            const res = await fetch(path);
            if (!res.ok) throw new Error(`${path}: ${res.status}`);
            return res.text();
        }

        function renderProject(data) {
            const p = (data && data.project) || {};
            const name = (p.name || "").trim();
            const desc = (p.description || "").trim();

            document.title = name || "Project";
            setText("proj-name", name || "Untitled project");
            setText("proj-desc", desc || "No description yet.");
            setText("meta-language", (p.language || "").trim() || "—");
            setText("meta-version", (p.version || "").trim() || "—");
            setText("meta-license", (p.license || "").trim() || "—");
            setText("meta-author", (p.author || "").trim() || "—");
            setText("meta-created", (p.created || "").trim() || "—");

            const deps = ((data && data.dependencies) || []).filter((d) =>
                (d.name || "").trim(),
            );
            const depsSection = document.getElementById("deps-section");
            if (deps.length) {
                setHtml(
                    "deps-list",
                    deps
                        .map(
                            (d) =>
                                `<li><span>${escapeHtml(d.name)}</span><span class="dim">${escapeHtml(
                                    d.version || "",
                                )}</span></li>`,
                        )
                        .join(""),
                );
            } else {
                depsSection.style.display = "none";
            }
        }

        function parseTodo(markdown) {
            const sections = {};
            const order = [];
            let current = null;

            // Normalize CRLF/CR line endings before splitting. Files written
            // by Python's Path.write_text() on Windows end up as \r\n, and a
            // leftover \r on each line breaks the regexes below entirely:
            // "." never matches \r, and "$" (no /m flag) needs the true end
            // of the string, so a match that should succeed silently fails.
            markdown
                .replace(/\r\n?/g, "\n")
                .split("\n")
                .forEach((line) => {
                    const heading = line.match(/^#{1,3}\s+(.*)$/);
                    if (heading) {
                        current = heading[1].trim();
                        if (!sections[current]) {
                            sections[current] = [];
                            order.push(current);
                        }
                        return;
                    }
                    const item = line.match(/^\s*-\s*\[( |x|X)\]\s*(.*)$/);
                    if (item && current) {
                        sections[current].push({
                            done: item[1].toLowerCase() === "x",
                            text: item[2].trim(),
                        });
                    }
                });

            return order.map((title) => ({
                title,
                items: sections[title],
            }));
        }

        // Renders High/Medium/Low priority sections as three side-by-side
        // columns. Any other headings the file happens to contain (besides
        // the top-level "TODO" title) are rendered below as a fallback so
        // nothing is silently dropped. Read-only: no done-toggle behavior.
        function renderTodoColumn(title, items) {
            if (!items.length) {
                return `<h3>${escapeHtml(title)}</h3><p class="dim">Nothing here.</p>`;
            }
            const list = items
                .map(
                    (i) =>
                        `<li class="${i.done ? "done" : ""}"><span class="checkbox">${i.done ? "[x]" : "[ ]"
                        }</span><span>${escapeHtml(i.text)}</span></li>`,
                )
                .join("");
            return `<h3>${escapeHtml(title)}</h3><ul class="todo-list">${list}</ul>`;
        }

        function renderTodo(markdown) {
            const sections = parseTodo(markdown).filter(
                (s) => s.title.toLowerCase() !== "todo",
            );

            const priorityKeys = ["high priority", "medium priority", "low priority"];
            const byKey = {};
            sections.forEach((s) => {
                byKey[s.title.toLowerCase()] = s;
            });

            const columnsHtml = priorityKeys
                .map((key) => {
                    const found = byKey[key];
                    const title = found
                        ? found.title
                        : key.replace(/\b\w/g, (c) => c.toUpperCase());
                    const items = found ? found.items : [];
                    return `<div class="todo-column">${renderTodoColumn(title, items)}</div>`;
                })
                .join("");

            const extraSections = sections.filter(
                (s) => !priorityKeys.includes(s.title.toLowerCase()),
            );
            const extraHtml = extraSections.length
                ? `<div class="todo-extra">${extraSections
                    .map((s) => renderTodoColumn(s.title, s.items))
                    .join("")}</div>`
                : "";

            return `<div class="todo-columns">${columnsHtml}</div>${extraHtml}`;
        }

        function renderIssues(data) {
            const issues = (data && data.issues) || [];
            if (!issues.length) return '<p class="dim">No issues.</p>';

            return issues
                .map((issue) => {
                    const status = (issue.status || "").trim().toLowerCase();
                    const priority = (issue.priority || "").trim().toLowerCase();
                    const labels = issue.labels || [];
                    return `
                        <details class="issue">
                            <summary>
                                <span class="issue-title">${escapeHtml(issue.title || "Untitled issue")}</span>
                                ${status ? `<span class="pill status-${escapeHtml(status)}">${escapeHtml(status)}</span>` : ""}
                                ${priority ? `<span class="pill priority-${escapeHtml(priority)}">${escapeHtml(priority)}</span>` : ""}
                            </summary>
                            <div class="issue-body">
                                <p>${escapeHtml(issue.description || "No description.")}</p>
                                <div class="issue-meta">
                                    ${labels.map((l) => `<span class="chip">${escapeHtml(l)}</span>`).join("")}
                                    <span class="dim">#${escapeHtml(issue.id ?? "")} &middot; ${escapeHtml(
                        issue.assignee || "unassigned",
                    )} &middot; ${escapeHtml(issue.created || "")}</span>
                                </div>
                            </div>
                        </details>`;
                })
                .join("");
        }

        function renderMarkdown(markdown) {
            if (!markdown || !markdown.trim()) {
                return '<p class="dim">No README yet.</p>';
            }

            let html = escapeHtml(markdown);

            const codeBlocks = [];
            html = html.replace(/```([\s\S]*?)```/g, (_, code) => {
                codeBlocks.push(code.replace(/^\n/, ""));
                return `\u0000CODEBLOCK${codeBlocks.length - 1}\u0000`;
            });

            html = html
                .replace(/^###### (.*)$/gm, "<h6>$1</h6>")
                .replace(/^##### (.*)$/gm, "<h5>$1</h5>")
                .replace(/^#### (.*)$/gm, "<h4>$1</h4>")
                .replace(/^### (.*)$/gm, "<h3>$1</h3>")
                .replace(/^## (.*)$/gm, "<h2>$1</h2>")
                .replace(/^# (.*)$/gm, "<h1>$1</h1>");

            html = html
                .replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>")
                .replace(/\*(.+?)\*/g, "<em>$1</em>")
                .replace(/`([^`]+)`/g, "<code>$1</code>")
                .replace(
                    /\[([^\]]+)\]\(([^)]+)\)/g,
                    '<a href="$2" target="_blank" rel="noopener">$1</a>',
                );

            html = html.replace(
                /(^|\n)((?:\s*-\s+.*(?:\n|$))+)/g,
                (match, pre, block) => {
                    const items = block
                        .trim()
                        .split("\n")
                        .map((line) => `<li>${line.replace(/^\s*-\s+/, "")}</li>`)
                        .join("");
                    return `${pre}<ul>${items}</ul>`;
                },
            );

            html = html
                .split(/\n{2,}/)
                .map((block) => {
                    const trimmed = block.trim();
                    if (!trimmed) return "";
                    if (/^<(h\d|ul|pre|\u0000)/.test(trimmed)) return trimmed;
                    if (/^\u0000CODEBLOCK\d+\u0000$/.test(trimmed)) return trimmed;
                    return `<p>${trimmed.replace(/\n/g, "<br>")}</p>`;
                })
                .join("\n");

            html = html.replace(/\u0000CODEBLOCK(\d+)\u0000/g, (_, i) => {
                return `<pre><code>${codeBlocks[Number(i)]}</code></pre>`;
            });

            return html;
        }

        async function loadAll() {
            await Promise.all([
                loadJson("./Project.json")
                    .then(renderProject)
                    .catch(() => renderProject(null)),
                loadJson("./Issues.json")
                    .then((data) => setHtml("issues-content", renderIssues(data)))
                    .catch(() =>
                        setHtml("issues-content", loadErrorMessage("Issues.json")),
                    ),
                loadText("./TODO.md")
                    .then((text) => setHtml("todo-content", renderTodo(text)))
                    .catch(() => setHtml("todo-content", loadErrorMessage("TODO.md"))),
                loadText("./README.md")
                    .then((text) => setHtml("readme-content", renderMarkdown(text)))
                    .catch(() =>
                        setHtml("readme-content", loadErrorMessage("README.md")),
                    ),
            ]);
        }

        onload = loadAll;
    </script>
</body>

</html>
"""

DEFAULT_TEMPLATE = {
    "folders": {
        "src": True,  # src is a folder for source code
    },
    "files": {
        "index.html": True,  # index.html is a file for the webUI manager
        "Notes.md": False,  # Notes.md is a file for taking free-form notes
        "Project.json": True,  # Project.json is a file for storing project metadata
        "Issues.json": True,  # Issues.json is a file for tracking issues
        "TODO.md": True,  # TODO.md is a file for tracking tasks
        "README.md": True,  # README.md is a file for project documentation
        ".gitignore": False,
    },
    "init-git-repo": False,
}

DEFAULT_STYLES_CSS = """:root {
    --bg: #0f1115;
    --surface: #1a1d24;
    --surface-hover: #232833;
    --border: #2a2f3a;
    --text: #e8eaed;
    --text-dim: #9aa0ab;
    --accent: #6ea8fe;
}

* {
    box-sizing: border-box;
}

body {
    margin: 0;
    font-family: "Segoe UI", system-ui, -apple-system, sans-serif;
    background: var(--bg);
    color: var(--text);
}

header {
    padding: 2rem 2.5rem 1rem;
    border-bottom: 1px solid var(--border);
}

header h1 {
    margin: 0;
    font-size: 1.6rem;
    font-weight: 600;
}

main {
    padding: 2rem 2.5rem;
    max-width: 900px;
    margin: 0 auto;
}

#projects h2 {
    font-size: 1rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: var(--text-dim);
    margin-bottom: 1rem;
}

#project-list {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
    gap: 0.9rem;
}

.project-item {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 10px;
    transition: background 0.15s ease, transform 0.15s ease, border-color 0.15s ease;
}

.project-item:hover {
    background: var(--surface-hover);
    border-color: var(--accent);
    transform: translateY(-2px);
}

.project-item a {
    display: block;
    padding: 1.1rem 1.2rem;
    color: var(--text);
    text-decoration: none;
    font-weight: 500;
}

.project-item a::before {
    content: "\\1F4C1";
    margin-right: 0.5rem;
}

.empty-state {
    color: var(--text-dim);
    font-style: italic;
    padding: 1rem 0;
}
"""

DEFAULT_WEBUI_HTML = """<!doctype html>
<html lang="en">
    <head>
        <meta charset="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <title>Just Manage My Projects</title>
        <link rel="stylesheet" href="styles.css" />
    </head>
    <body>
        <header>
            <h1>Just Manage My Projects</h1>
        </header>
        <main>
            <section id="projects">
                <h2>Projects</h2>
                <div id="project-list">
                    <!-- Project items will be dynamically added here -->
                </div>
            </section>
        </main>
        <script>
            // This list is auto-generated by main.py every time a project is
            // created or deleted. Don't edit it by hand — it will be
            // overwritten. Edit main.py's regenerate_webui() if you need to
            // change how it's built.
            function loadProjects() {
                const projectList = document.getElementById("project-list");

                // AUTO-GENERATED-PROJECTS-START
                const projects = [];
                // AUTO-GENERATED-PROJECTS-END

                if (projects.length === 0) {
                    projectList.innerHTML = '<p class="empty-state">No projects yet. Create one with main.py.</p>';
                    return;
                }

                projects.forEach((project) => {
                    // Folder names can contain characters like '#' or '+'
                    // that break a plain href, so each path segment is
                    // percent-encoded before being used as a link target.
                    const encodedPath = project.path
                        .split("/")
                        .map(encodeURIComponent)
                        .join("/");

                    const projectItem = document.createElement("div");
                    projectItem.className = "project-item";
                    const link = document.createElement("a");
                    link.href = `${encodedPath}/index.html`;
                    link.target = "_blank";
                    link.textContent = project.name;
                    projectItem.appendChild(link);
                    projectList.appendChild(projectItem);
                });
            }

            onload = loadProjects;
        </script>
    </body>
</html>
"""
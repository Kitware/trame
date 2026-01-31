#!/usr/bin/env python3
"""
Generate an index.md file from blog posts in the blogs/ directory.
Extracts: first image, first H1 title, date, and authors from each blog.
"""

import re
import json
from pathlib import Path
from dataclasses import dataclass

BLOG_DIRECTORY = Path(__file__).with_name("blogs")
BLOG_INDEX = BLOG_DIRECTORY / "index.md"
BLOG_MENU = Path(__file__).with_name(".vitepress") / "blogs.json"

if BLOG_INDEX.exists():
    BLOG_INDEX.unlink()


@dataclass
class BlogInfo:
    title: str
    date: str
    authors: str
    image: str
    filename: str


def to_xy(index, n_cols=6):
    x = index
    y = 0
    delta = -1
    while x >= n_cols:
        x -= n_cols
        n_cols += delta
        delta *= -1
        y += 1

    if delta > 0:
        x += 0.5

    return x, y


def parse_blog(filepath: Path) -> BlogInfo | None:
    """Parse a markdown blog file and extract metadata."""
    try:
        content = filepath.read_text(encoding="utf-8")
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return None

    lines = content.split("\n")

    title = ""
    date = ""
    authors = ""
    image = ""

    for i, line in enumerate(lines):
        # Find first H1 title
        if not title and line.startswith("# "):
            title = line[2:].strip()
            continue

        # Find date (line after title, format like "January 13, 2026")
        if title and not date:
            # Date pattern: Month Day, Year
            date_match = re.match(
                r"^(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},\s+\d{4}$",
                line.strip(),
            )
            if date_match:
                date = line.strip()
                continue

        # Find authors (line with markdown links to author pages)
        if not authors and "kitware.com/author/" in line:
            # Extract author names from markdown links
            author_matches = re.findall(
                r"\[([^\]]+)\]\(https://www\.kitware\.com/author/", line
            )
            if author_matches:
                authors = ", ".join(author_matches)
                continue

        # Find first image
        if not image:
            # Markdown image: ![alt](url)
            img_match = re.search(r"!\[[^\]]*\]\(([^)]+)\)", line)
            if img_match:
                image = img_match.group(1)
                continue

            # HTML img tag
            img_tag_match = re.search(r'<img[^>]+src=["\']([^"\']+)["\']', line)
            if img_tag_match:
                image = img_tag_match.group(1)
                continue

        # Stop if we have all info
        if title and date and authors and image:
            break

    if not title:
        return None

    return BlogInfo(
        title=title,
        date=date or "Unknown",
        authors=authors or "Unknown",
        image=image or "",
        filename=filepath.name,
    )


def generate_index(blogs_dir: Path, output_file: Path, columns: int = 3):
    """Generate index.md with a table of blog posts."""
    blog_files = sorted(blogs_dir.glob("*.md"))
    blogs = []

    for blog_file in blog_files:
        info = parse_blog(blog_file)
        if info:
            blogs.append(info)

    # Sort by date (newest first) - parse date for sorting
    def parse_date_for_sort(date_str: str) -> tuple:
        months = {
            "January": 1,
            "February": 2,
            "March": 3,
            "April": 4,
            "May": 5,
            "June": 6,
            "July": 7,
            "August": 8,
            "September": 9,
            "October": 10,
            "November": 11,
            "December": 12,
        }

        match = re.match(r"(\w+)\s+(\d+),\s+(\d+)", date_str)
        if match:
            month, day, year = match.groups()
            return (int(year), months.get(month, 0), int(day))

        return (0, 0, 0)

    blogs.sort(key=lambda b: parse_date_for_sort(b.date), reverse=True)

    # {
    #   text: "Core functionalities",
    #   items: [
    #     { text: "Basics", link: "/examples/core/basics" },
    #     { text: "Files", link: "/examples/core/files" },
    #     { text: "Jupyter", link: "/examples/core/jupyter" },
    #     { text: "Plotly", link: "/examples/core/plotly" },
    #     { text: "Docker", link: "/examples/core/docker" },
    #     // router, docker
    #   ],
    # },
    #
    years = {}

    for blog in blogs:
        year = blog.date.split(" ").pop()
        container = years.setdefault(year, [])
        container.append({"text": blog.title, "link": f"/blogs/{blog.filename[:-3]}"})

    final_structure = []
    for year, items in years.items():
        final_structure.append(
            {
                "text": year,
                "items": items,
            }
        )

    BLOG_MENU.write_text(json.dumps(final_structure, indent=2), encoding="utf-8")

    # # Generate markdown
    # md_lines = [
    #     "# Blogs",
    #     "<table>",
    # ]

    # # Create rows with specified columns
    # for i in range(0, len(blogs), columns):
    #     md_lines.append("  <tr>")
    #     for j in range(columns):
    #         if i + j < len(blogs):
    #             blog = blogs[i + j]
    #             cell_content = []
    #             cell_content.append(f"<small>{blog.date}</small><br>")
    #             if blog.image:
    #                 cell_content.append(f'<img src="{blog.image}" width="200"><br>')
    #             cell_content.append(
    #                 f'<strong><a href="{Path(blog.filename).stem}">{blog.title}</a></strong>'
    #             )
    #             md_lines.append(
    #                 f'    <td align="center" width="{100 // columns}%" valign="top">'
    #             )
    #             md_lines.append("      " + "".join(cell_content))
    #             md_lines.append("    </td>")
    #         else:
    #             md_lines.append(f'    <td width="{100 // columns}%"></td>')
    #     md_lines.append("  </tr>")

    # md_lines.append("</table>")
    # md_lines.append("")

    # BLOG_INDEX.write_text("\n".join(md_lines), encoding="utf-8")

    # ------------------------------------------
    # Generate Hex gallery
    # ------------------------------------------

    items = []
    max_y = 0
    for i, blog in enumerate(blogs):
        x, y = to_xy(i, 5)
        max_y = y
        items.append(
            """<div class="blog-item">"""
            f"""<a class="blog-link" title="{blog.title}" href="/trame/blogs/{blog.filename[:-3]}" """
            f""" style="--x: {x}; --y: {y};">"""
            f"""<img src="{blog.image}" alt="{blog.title}"/>"""
            """</a></div>"""
        )

    BLOG_INDEX.write_text(
        f"""# Blogs

<div class="blog-hex-gallery" style="--max-blog-y: {max_y}">
    {"\n".join(items)}
</div>

""",
        encoding="utf-8",
    )

    print(f"Generated {output_file} with {len(blogs)} blog entries")


if __name__ == "__main__":
    script_dir = Path(__file__).parent
    blogs_dir = script_dir / "blogs"
    output_file = script_dir / "index.json"

    if not blogs_dir.exists():
        print(f"Error: blogs directory not found at {blogs_dir}")
        exit(1)

    generate_index(blogs_dir, output_file, columns=3)

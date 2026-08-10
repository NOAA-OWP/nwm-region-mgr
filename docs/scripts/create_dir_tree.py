"""Build and render S3 directory tree as markdown text for documentation."""

import argparse
import csv
from collections import defaultdict
from pathlib import Path

import boto3


def build_tree(bucket, prefix):
    """Build a nested dictionary representing the S3 directory structure under the given prefix."""
    s3 = boto3.client("s3")
    paginator = s3.get_paginator("list_objects_v2")
    tree = lambda: defaultdict(tree)
    root = tree()

    for page in paginator.paginate(Bucket=bucket, Prefix=prefix):
        for obj in page.get("Contents", []):
            key = obj["Key"]
            rel = key[len(prefix) :].strip("/")
            if not rel:
                continue
            parts = rel.split("/")
            current = root
            for part in parts:
                current = current[part]

    return root


def load_comments(csv_file):
    """Load comments from a CSV file into a dictionary mapping paths to comments."""
    comments = {}
    with open(csv_file, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            path = row["path"].strip().rstrip("/")
            comments[path] = row["comment"].strip()
    return comments


def render_tree(tree, comments, current_path="", depth=1, max_depth=None):
    """Recursively render the tree as a list of markdown lines with comments."""
    lines = []
    entries = sorted(tree.keys())

    for i, entry in enumerate(entries):
        connector = "└── " if i == len(entries) - 1 else "├── "
        full_path = f"{current_path}/{entry}".strip("/")
        comment = comments.get(full_path, "")

        line = f"{connector}{entry}"
        if comment:
            line = f"{line:<60} # {comment}"

        indent = "│   " * (depth - 1)
        lines.append(f"{indent}{line}")

        if max_depth is None or depth < max_depth:
            lines.extend(
                render_tree(
                    tree[entry],
                    comments,
                    current_path=full_path,
                    depth=depth + 1,
                    max_depth=max_depth,
                )
            )

    return lines


def generate_md(bucket, prefix, comments, max_depth=None):
    """Generate markdown text for the directory tree under the given S3 prefix."""
    tree = build_tree(bucket, prefix)
    lines = ["```bash"]
    header = "inputs" if "inputs" in prefix.lower() else "outputs"
    lines.append(f"{header}")

    rendered = render_tree(
        tree, comments, current_path="", depth=1, max_depth=max_depth
    )
    lines.extend(rendered)
    lines.append("```")
    lines.append("")
    return "\n".join(lines)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--bucket", default="ngwpc-dev", help="S3 bucket name")
    parser.add_argument(
        "--prefixes",
        nargs="*",
        default=[
            "regionalization/data/inputs/",
            "regionalization/data/outputs/",
        ],
        help="S3 prefixes to include",
    )

    parser.add_argument(
        "--comments",
        default="folder_file_desc.csv",
        help="CSV file containing path,comment columns",
    )

    parser.add_argument(
        "--max-depth",
        type=int,
        default=3,
        help="Maximum directory depth to display (default: no limit)",
    )

    args = parser.parse_args()
    comments = load_comments(args.comments)

    for prefix in args.prefixes:
        depth = 3 if "inputs" in prefix.lower() else None
        md_content = generate_md(args.bucket, prefix, comments, max_depth=depth)
        file_stem = "input_tree" if "inputs" in prefix else "output_tree"
        file_name = f"{file_stem}.md"
        file_path = (
            Path(__file__).parent.parent / "source" / "tech_reference" / file_name
        )

        # Add header
        header_str = "Input" if "inputs" in prefix.lower() else "Output"
        header = f"## {header_str} Directory Structure\n\n"
        desc = (
            f"The {header_str.lower()} directory contains three subdirectories: `region`, `ngen`, and `eval`, "
            f"which store the respective {header_str.lower()} files for the regionalization, ngen simulation, and "
            f"evaluation steps.\n\n"
        )
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(header + desc + md_content)

        print(f"Saved {prefix} tree to {file_path}")

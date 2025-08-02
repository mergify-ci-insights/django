#!/usr/bin/env python3
"""
Script to merge multiple JUnit XML files into
a single file with <testsuites> root.
"""

import sys
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path


def merge_junit_xml_files(input_dir: str, output_file: str) -> None:
    """
    Merge all JUnit XML files in a directory into a single file.

    Args:
        input_dir: Directory containing individual JUnit XML files
        output_file: Path for the merged output file
    """
    input_path = Path(input_dir)

    if not input_path.exists():
        print(f"Error: Directory {input_dir} does not exist", file=sys.stderr)
        sys.exit(1)

    # Find all XML files
    xml_files = list(input_path.glob("*.xml"))

    if not xml_files:
        print(f"Error: No XML files found in {input_dir}", file=sys.stderr)
        sys.exit(1)

    print(f"Found {len(xml_files)} XML files to merge")

    # Create the root testsuites element
    testsuites = ET.Element("testsuites")

    total_tests = 0
    total_failures = 0
    total_errors = 0
    total_skipped = 0
    total_time = 0.0

    # Process each XML file
    for xml_file in sorted(xml_files):
        print(f"Processing: {xml_file.name}")

        try:
            # Parse the individual XML file
            tree = ET.parse(xml_file)
            root = tree.getroot()

            # Ensure it's a testsuite element
            if root.tag != "testsuite":
                print(
                    f"Warning: {xml_file.name} does not have "
                    "'testsuite' as root element, skipping"
                )
                continue

            # Add this testsuite to our testsuites collection
            testsuites.append(root)

            # Accumulate statistics
            try:
                total_tests += int(root.get("tests", 0))
                total_failures += int(root.get("failures", 0))
                total_errors += int(root.get("errors", 0))
                total_skipped += int(root.get("skipped", 0))
                total_time += float(root.get("time", 0.0))
            except (ValueError, TypeError) as e:
                print(f"Warning: Could not parse statistics from {xml_file.name}: {e}")

        except ET.ParseError as e:
            print(f"Error parsing {xml_file.name}: {e}", file=sys.stderr)
            continue
        except Exception as e:
            print(f"Unexpected error processing {xml_file.name}: {e}", file=sys.stderr)
            continue

    # Set attributes on the testsuites element
    testsuites.set("tests", str(total_tests))
    testsuites.set("failures", str(total_failures))
    testsuites.set("errors", str(total_errors))
    testsuites.set("skipped", str(total_skipped))
    testsuites.set("time", f"{total_time:.3f}")
    testsuites.set("timestamp", datetime.now().isoformat())

    # Create the tree and write to file
    merged_tree = ET.ElementTree(testsuites)

    # Indent for pretty printing
    ET.indent(merged_tree, space="  ", level=0)

    # Write the merged XML
    with open(output_file, "wb") as f:
        f.write(b'<?xml version="1.0" encoding="UTF-8"?>\n')
        merged_tree.write(f, encoding="UTF-8", xml_declaration=False)

    print(f"\nMerged {len(testsuites)} test suites into {output_file}")
    print("Total statistics:")
    print(f"  Tests: {total_tests}")
    print(f"  Failures: {total_failures}")
    print(f"  Errors: {total_errors}")
    print(f"  Skipped: {total_skipped}")
    print(f"  Time: {total_time:.3f}s")


def main():
    if len(sys.argv) < 2:
        print("Usage: python merge_junit_xml.py <input_directory> [output_file]")
        print(
            "Example: python merge_junit_xml.py tests/test-results merged-results.xml"
        )
        sys.exit(1)

    input_dir = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else "merged-junit-results.xml"

    merge_junit_xml_files(input_dir, output_file)


if __name__ == "__main__":
    main()

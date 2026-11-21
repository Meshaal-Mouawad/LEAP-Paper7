#!/usr/bin/env python3
"""Audit frozen figure data and export the retained SVG artwork.

Created for the 18 November 2026 Gold review. Reads archived decisions without
executing study code. The retained SVGs are the authoritative artwork inputs;
their original Matplotlib metadata is recorded separately from this export.
Requires Python 3, Inkscape, and pypdf; Poppler is needed for --previews.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import xml.etree.ElementTree as ET
import zipfile

from pypdf import PdfReader

LOCKED_ARCHIVE_SHA256 = "b55949d177b3355bda1f49442015141ac382e84345b4cc283a7fc4a811a9db48"
ARCHIVE_ROOT = "Paper7_Reproduction/"
SVG_NS = {"s": "http://www.w3.org/2000/svg"}
METHODS = [
    ("bound", "Full monitor"),
    ("timer_only", "Timers only"),
    ("no_evidence_binding", "Ignore observation version"),
    ("no_suppression_binding", "Ignore suppression version"),
    ("no_freshness", "Remove stale-age check"),
]
DECISION_FIELDS = ("state", "active", "severity")


def require(condition, message):
    if not condition:
        raise ValueError(message)


def sha_bytes(data):
    return hashlib.sha256(data).hexdigest()


def sha_file(path):
    return sha_bytes(path.read_bytes())


def intervals(outputs):
    runs, start = [], None
    for index, output in enumerate(outputs):
        if output["active"] and start is None:
            start = index
        if not output["active"] and start is not None:
            runs.append((start, index))
            start = None
    if start is not None:
        runs.append((start, len(outputs)))
    return runs


def decision_sequence(outputs):
    return [tuple(output[field] for field in DECISION_FIELDS) for output in outputs]


def json_rows(archive, name):
    with archive.open(ARCHIVE_ROOT + name) as stream:
        for line in stream:
            if line.strip():
                yield json.loads(line)


def svg_texts(root):
    return ["".join(node.itertext()) for node in root.findall(".//s:text", SVG_NS)]


def by_id(root, identifier):
    node = root.find(f".//*[@id='{identifier}']")
    require(node is not None, f"Missing SVG element: {identifier}")
    return node


def audit_data(archive):
    traces = {
        row["id"]: row
        for row in json_rows(archive, "study/benchmark/traces.jsonl")
        if row["split"] == "heldout" and row["variant"] == "base"
    }
    require(len(traces) == 987, "Held-out base-trace denominator changed")
    references = {
        row["id"]: row["outputs"]
        for row in json_rows(archive, "study/benchmark/reference.jsonl")
        if row["id"] in traces
    }
    require(set(references) == set(traces), "Missing reference for selected trace")
    methods = {name for name, _ in METHODS}
    counts = {
        name: {"complete_decision_mismatches": 0, "active_interval_mismatches": 0, "seen": set()}
        for name in methods
    }
    for row in json_rows(archive, "saved_run/results/predictions.jsonl"):
        name, trace_id = row["method"], row["id"]
        if name not in methods or trace_id not in traces:
            continue
        result = counts[name]
        require(trace_id not in result["seen"], f"Duplicate saved prediction: {name}/{trace_id}")
        result["seen"].add(trace_id)
        actual, reference = row["outputs"], references[trace_id]
        require(len(actual) == len(reference), f"Event count differs: {name}/{trace_id}")
        result["complete_decision_mismatches"] += decision_sequence(actual) != decision_sequence(reference)
        result["active_interval_mismatches"] += intervals(actual) != intervals(reference)

    archived_csv = list(csv.DictReader(io.StringIO(archive.read(ARCHIVE_ROOT + "analysis/endpoint_metrics.csv").decode())))
    selected_csv = {row["method"]: row for row in archived_csv if row["split"] == "heldout" and row["stratum"] == "base_only"}
    output = []
    for name, label in METHODS:
        result = counts[name]
        require(result.pop("seen") == set(traces), f"Missing saved prediction: {name}")
        csv_row = selected_csv[name]
        require(int(csv_row["traces"]) == 987, f"CSV denominator differs: {name}")
        require(result["complete_decision_mismatches"] == 987 - int(csv_row["trace_agreement"]), f"CSV decision count differs: {name}")
        require(result["active_interval_mismatches"] == 987 - int(csv_row["episode_agreement"]), f"CSV interval count differs: {name}")
        output.append({"method": name, "figure_label": label, "traces": 987, **result})

    witness_records = json.loads(archive.read(ARCHIVE_ROOT + "study/benchmark/witness_references.json"))
    witnesses = [row for row in witness_records if row["id"] == "privacy/o.c"]
    require(len(witnesses) == 1, "Expected exactly one privacy/o.c witness")
    witness = witnesses[0]
    for side in ("left", "right"):
        require([event["t"] for event in witness[side]] == [0, 2, 3, 5], f"Witness times changed: {side}")
        require(all(event["unit"] == "s" for event in witness[side]), "Witness unit is not seconds")
    for left, right in zip(witness["left"], witness["right"], strict=True):
        lcopy, rcopy = json.loads(json.dumps(left)), json.loads(json.dumps(right))
        lcopy["o"].pop("c")
        rcopy["o"].pop("c")
        require(lcopy == rcopy, "Witness differs after observation-context deletion")
    return {
        "calculation": "Compare saved state/activity/severity sequences and contiguous active event-index intervals against the frozen reference; select heldout/base records.",
        "study_execution": False,
        "heldout_base_traces": len(traces),
        "heldout_base_events": sum(len(row["trace"]) for row in traces.values()),
        "rows": output,
        "witness": {
            "id": witness["id"],
            "times_s": [event["t"] for event in witness["left"]],
            "left_states": [row["state"] for row in witness["left_reference"]],
            "right_states": [row["state"] for row in witness["right_reference"]],
            "projection_identical": True,
        },
    }


def audit_svg(stem, path, data):
    root = ET.parse(path).getroot()
    texts = svg_texts(root)
    require(not root.findall(".//s:image", SVG_NS), f"Unexpected raster image in {stem}")
    require(not root.findall(".//s:script", SVG_NS), f"Unexpected script in {stem}")
    titles = root.findall(".//{http://purl.org/dc/elements/1.1/}title")
    creators = [node.text for node in titles]
    require(creators == ["Matplotlib v3.10.8, https://matplotlib.org/"], f"Unexpected creator metadata: {stem}")
    result = {
        "svg": str(path.resolve()),
        "svg_sha256": sha_file(path),
        "creator_metadata": creators[0],
        "width": root.attrib["width"],
        "height": root.attrib["height"],
        "viewBox": root.attrib["viewBox"],
        "text_elements": len(texts),
        "raster_images": 0,
    }
    if stem == "trace_mismatches":
        expected = []
        for row in data["rows"]:
            require(row["figure_label"] in texts, f"Missing chart row: {row['figure_label']}")
            expected += [row["complete_decision_mismatches"], row["active_interval_mismatches"]]
        number_texts = [node for node in root.findall(".//s:text", SVG_NS) if re.search(r"fill: #(28566d|ac592b)", node.attrib.get("style", ""))]
        require([int(node.text) for node in number_texts] == expected, "Plotted count labels differ from frozen predictions")
        require("Base traces with a mismatch (out of 987)" in texts, "Missing figure denominator")
        ticks = []
        for index in range(1, 7):
            node = by_id(root, f"xtick_{index}").find(".//s:text", SVG_NS)
            ticks.append((int(node.text), float(node.attrib["x"])))
        require([value for value, _ in ticks] == [0, 20, 40, 60, 80, 100], "Unexpected x ticks")
        zero, slope = ticks[0][1], (ticks[-1][1] - ticks[0][1]) / 100
        for value, x in ticks:
            require(abs(x - zero - slope * value) < 2e-6, "Nonlinear or inconsistent tick positions")
        coordinates = []
        for index, value in enumerate(expected, start=1):
            point = by_id(root, f"PathCollection_{index}").find(".//s:use", SVG_NS)
            require(point is not None, f"Missing plotted point {index}")
            x = float(point.attrib["x"])
            require(abs(x - zero - slope * value) < 2e-6, f"Plotted x position differs: point {index}")
            coordinates.append({"value": value, "x_svg_pt": x, "y_svg_pt": float(point.attrib["y"])})
        result.update({"data_labels_verified": 10, "data_coordinates_verified": 10, "data_coordinates": coordinates})
    elif stem == "necessity_witness":
        states = [text for text in texts if text in {"PENDING", "ACTIVE", "UNKNOWN"}]
        expected = data["witness"]["left_states"] + data["witness"]["right_states"]
        require(states == expected, "Witness state labels differ from frozen reference")
        timestamps = [int(re.fullmatch(r"t = (\d+) s", text).group(1)) for text in texts if re.fullmatch(r"t = (\d+) s", text)]
        require(timestamps == data["witness"]["times_s"], "Witness time labels differ")
        result.update({"frozen_witness_id": data["witness"]["id"], "state_labels_verified": 8, "timestamp_labels_verified": 4})
    else:
        required = ["Optional observation", "1  Reset when required", "2  Update the episode", "3  Set displayed state", "Suppress only if active, both", "versions match, and t < expiry.", "Displayed state · episode activity · severity · reason"]
        for label in required:
            require(label in texts, f"Missing documented mechanism label: {label}")
        result["mechanism_label_inventory_verified"] = required
        result["semantic_basis"] = "Retained contract and monitor source; mechanistic diagram, with no plotted numerical result."
    return result


def run(args):
    require(sha_file(args.archive) == LOCKED_ARCHIVE_SHA256, "Archive differs from the frozen release")
    args.output_dir.mkdir(parents=True, exist_ok=True)
    source_names = [
        "study/benchmark/traces.jsonl", "study/benchmark/reference.jsonl",
        "saved_run/results/predictions.jsonl", "analysis/endpoint_metrics.csv",
        "study/benchmark/witness_references.json", "study/protocol/SEMANTICS.md",
        "study/implementation/monitor.py",
    ]
    with zipfile.ZipFile(args.archive) as archive:
        require(len(archive.namelist()) == 188, "Archive entry count changed")
        require(archive.testzip() is None, "Archive CRC failure")
        data = audit_data(archive)
        sources = {name: sha_bytes(archive.read(ARCHIVE_ROOT + name)) for name in source_names}
    inkscape = shutil.which("inkscape")
    require(inkscape is not None, "Inkscape is required for SVG export")
    renderer_version = subprocess.run([inkscape, "--version"], check=True, text=True, capture_output=True).stdout.strip()
    figures = {}
    for stem in ("method_pipeline", "necessity_witness", "trace_mismatches"):
        svg = args.svg_dir / f"{stem}.svg"
        figure = audit_svg(stem, svg, data)
        pdf = args.output_dir / f"{stem}.pdf"
        command = [inkscape, str(svg.resolve()), "--export-type=pdf", "--export-area-page", "--export-filename=" + str(pdf.resolve())]
        subprocess.run(command, check=True, text=True, capture_output=True)
        reader = PdfReader(pdf)
        require(len(reader.pages) == 1, f"Expected single-page figure PDF: {stem}")
        page = reader.pages[0]
        size = [float(page.mediabox.width), float(page.mediabox.height)]
        expected_size = [float(figure[key].removesuffix("pt")) for key in ("width", "height")]
        require(all(abs(a-b) < 0.001 for a, b in zip(size, expected_size)), f"Figure page size changed: {stem}")
        figure.update({"pdf": str(pdf.resolve()), "pdf_sha256": sha_file(pdf), "pdf_size_pt": size, "export_command": command})
        if args.previews:
            poppler = shutil.which("pdftoppm")
            require(poppler is not None, "pdftoppm is required for previews")
            subprocess.run([poppler, "-singlefile", "-scale-to", "1600", "-png", str(pdf.resolve()), str((args.output_dir / stem).resolve())], check=True, text=True, capture_output=True)
        figures[stem] = figure
    report = {
        "status": "PASS",
        "archive": str(args.archive.resolve()),
        "archive_sha256": LOCKED_ARCHIVE_SHA256,
        "archive_entries": 188,
        "frozen_source_sha256": sources,
        "data": data,
        "svg_export": {"renderer": renderer_version, "python": sys.version, "authoritative_artwork": "Unchanged retained SVGs", "figures": figures},
        "historical_ai_provenance": {"tools": ["OpenAI ChatGPT", "Codex"], "exact_original_model_build": None, "original_model_build_status": "Unavailable in retained activity records", "original_matplotlib_plotter_status": "Not retained; current reproduction exports the retained SVG source"},
        "new_study_execution": False,
    }
    (args.output_dir / "Figure_Data_and_Render_Verification.json").write_text(json.dumps(report, indent=2) + "\n")
    with (args.output_dir / "Figure3_Data.csv").open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(data["rows"][0]))
        writer.writeheader()
        writer.writerows(data["rows"])
    print(json.dumps({"status": "PASS", "figure3_rows": data["rows"], "renderer": renderer_version, "output_dir": str(args.output_dir.resolve())}, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--archive", type=Path, required=True, help="Frozen LEAP_Paper7_Reproduction_20261118.zip")
    parser.add_argument("--svg-dir", type=Path, required=True, help="Directory containing the three retained SVGs")
    parser.add_argument("--output-dir", type=Path, required=True, help="A separate directory for PDF exports and audit records")
    parser.add_argument("--previews", action="store_true", help="Render figure PNG previews with Poppler")
    run(parser.parse_args())

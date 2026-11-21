# Figure reproduction and production evidence

`reproduce_figures.py` reads the preserved research archive, independently
recalculates the two plotted mismatch endpoints from saved outputs, verifies
the retained SVG labels and coordinates, and exports the SVGs with Inkscape.
It does not execute the research implementations or edit the source artwork.

Requirements: Python 3, `pypdf`, Inkscape; Poppler `pdftoppm` for PNG previews.
The verified environment used Python 3.12.14, pypdf 6.21.4 and Inkscape 1.4
(e7c3feb100, 2024-10-09).

```sh
python reproduce_figures.py \
  --archive /path/to/LEAP_Paper7_Reproduction_20261118.zip \
  --svg-dir /path/to/figures \
  --output-dir /path/to/figure-reproduction \
  --previews
```

The archive must have the frozen SHA-256
`b55949d177b3355bda1f49442015141ac382e84345b4cc283a7fc4a811a9db48`.
The three SVGs are `method_pipeline.svg`, `necessity_witness.svg` and
`trace_mismatches.svg`. The output directory is separate from those inputs.

Outputs: three figure PDFs, optional PNGs, `Figure3_Data.csv`, and
`Figure_Data_and_Render_Verification.json`. The verification record identifies
the inputs, actual exporter, commands and output hashes. PDF metadata can vary
between renderings. The verification checks scientific content, point positions,
labels, figure dimensions and source identity.

`Figure_Provenance_and_Production_Review.md` records the source history,
publisher-policy interpretation, proposed manuscript disclosures, actual checks,
and the original model-version information that is unavailable.

# Archived asset provenance and limitations

These sources document artwork from the previous profile-v4 design. The current
`README.md` does not display these icons.

Product names and marks belong to their respective owners. No endorsement is
implied. This file distinguishes source-derived art, reconstructed art, and
representative symbols; these are not all original upstream logo files.

## Source-derived and retained assets

- Most technology outlines retain the Simple Icons-derived geometry supplied in
  the earlier profile. Some colors differ from official brand colors.
  https://github.com/simple-icons/simple-icons
- Matplotlib retains the artwork from the earlier kit, sourced from its project.
  https://github.com/matplotlib/matplotlib
- The verl geometry is retained from the earlier supplied organization-avatar
  interpretation. https://github.com/verl-project
- vLLM uses the yellow/blue two-path V symbol from Lobe Icons' Color component.
  Its exact geometry was available as source text and is bundled here.
  https://raw.githubusercontent.com/lobehub/lobe-icons/master/src/Vllm/components/Color.tsx
  The corresponding Lobe Icons license notice is included.

## Locally reconstructed marks — NOT original downloaded files

Network access did not permit downloading the original binary image files into
this workspace. Rather than present text-and-dot placeholders as official logos,
the following local vector reconstructions reproduce recognizable elements of
source images inspected through the web tool. They are not pixel-identical copies.

- JAX: reconstructed isometric colored-letter mark.
  Reference: https://raw.githubusercontent.com/jax-ml/jax/main/images/jax_logo_250px.png
- NumPyro: reconstructed red/orange/yellow Pyro monogram.
  Reference: https://raw.githubusercontent.com/pyro-ppl/numpyro/master/docs/source/_static/img/pyro_logo.png

These entries are documented explicitly so that they are not mistaken for
unmodified official assets. Their editable vectors are in design/legacy-logos/.

## Representative symbols

Slurm/HPC and SQL use general cluster/database symbols. The Bash/Zsh entry uses
Bash-related artwork. Seaborn retains the earlier simplified wave mark. These are
representations of the tools, not newly verified official brand artwork.

## New profile design

The console, navigation shapes, project numbering, and decorative research motifs
were created for this profile. They do not display empirical data or live metrics.
All final display assets are local; no font files, external image references,
tracking counters, or external animation services are required by the README.

## Navigation artwork added in this revision

Google Scholar, LinkedIn, and GitHub navigation icons are the SVG artwork from the
locally available Font Awesome Free 6.7.2 `brands` set (not hand-drawn substitutes).
The geometry is scaled to the 14-pixel icon box; the fill is adapted to each theme.
Original SVGs, attribution comments, and the license notice are retained in
`design/navigation-icons/` and `LICENSE-FONT-AWESOME.txt`.

- https://github.com/FortAwesome/Font-Awesome
- https://fontawesome.com/license/free

The JAX, NumPyro, and representative toolchain marks described above have
not been replaced or reclassified in this layout revision.

## MATLAB-only correction

The previous hand-drawn MATLAB approximation has been replaced by theSVG's
source-provided MATLAB vector icon. The geometry, gradients, and source colors
are retained; the mark is uniformly scaled into the existing 56 x 32 pixel logo
box, above the existing MATLAB caption. This is theSVG's vector rendition, not
MathWorks' official raster PNG. No other tool marks or profile layout changed.

Source: https://thesvg.org/icon/matlab
Upstream SVG: https://github.com/glincker/thesvg/blob/main/public/icons/matlab/default.svg
License: MIT, as identified by the upstream icon page. The license notice is
in LICENSE-THESVG.txt. MATLAB remains a trademark of The MathWorks, Inc.

The source is bundled at design/legacy-logos/logo-matlab.svg. The two
pre-rendered local image files are assets/profile-v4/tool-matlab-light.png and
assets/profile-v4/tool-matlab-dark.png. No external image request is needed.

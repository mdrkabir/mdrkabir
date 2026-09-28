# Logo and symbol sources

## Four corrected brands: original upstream artwork

The one-time `tools/fetch_official_logos.py` setup uses these original files,
without tracing, recoloring, or substituting the artwork:

- JAX: https://raw.githubusercontent.com/jax-ml/jax/main/images/jax_logo_250px.png
- NumPyro: https://raw.githubusercontent.com/pyro-ppl/numpyro/master/docs/source/_static/img/pyro_logo.png
- MATLAB: https://raw.githubusercontent.com/mathworks/MATLAB-extension-for-vscode/main/public/L-Membrane_RGB_128x128.png
- vLLM light theme: https://raw.githubusercontent.com/vllm-project/vllm/main/docs/assets/logos/vllm-logo-text-light.png
- vLLM dark theme: https://raw.githubusercontent.com/vllm-project/vllm/main/docs/assets/logos/vllm-logo-text-dark.png

These five PNGs are not present in the initial archive because the working
container could not download the original bytes. The initial README therefore
uses the source URLs. The setup script (or included GitHub workflow) downloads the
files, validates them, records their hashes, and switches the README to local paths.
See SETUP.md. There is no need to run the previous browser repair page.

## Retained bundled artwork

Python, PyTorch, Hugging Face, TensorFlow, scikit-learn, NumPy, Pandas, Linux,
GNU Bash, Docker, Google Cloud, Git, C++, C, R, PostgreSQL, and MySQL retain the
Simple Icons-derived outlines from the preceding version. Some are recolored.

- https://github.com/simple-icons/simple-icons
- https://github.com/simple-icons/simple-icons/blob/develop/LICENSE.md

Matplotlib retains the SVG from the Matplotlib distribution:
https://github.com/matplotlib/matplotlib

The verl mark retains geometry derived from the public organization avatar:
https://github.com/verl-project.png

Seaborn retains the earlier simplified mark. Slurm/HPC and SQL retain representative
cluster and database symbols; the combined Bash/Zsh entry uses the Bash mark.
These symbols are not claimed to be newly verified official brand artwork.

The prior Lobe Icons notice is retained in LICENSE-LOBE-ICONS.txt.

## Presentation and ownership

Five category headings and 26 visible captions are retained. FSDP and LaTeX are
excluded. Logos are linked; captions are separate unlinked text. All project and
product names and marks belong to their respective owners; no endorsement is
implied. No font files are included.

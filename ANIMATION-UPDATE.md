# Research console: three-scene loop restored

The current animation replaces the accidental single-command loop. It cycles through:

1. `whoami`: name, Computer Science Ph.D. student, Indiana University Bloomington.
2. `cat research.txt`: LLM post-training & interpretability; Reinforcement learning;
   Bayesian modeling & inference.
3. `ls selected-work/`: the three research project identifiers.

`research.focus` remains the separate, static right-hand panel. The visible header
panels remain 312 × 250 CSS pixels each. Animation pixels remain 936 × 750.
No README, navigation, research-section, focus, or toolchain edits are required.

## Existing installation

For the visible change, replace only:

```
assets/profile-v4/console-light.gif
assets/profile-v4/console-dark.gif
```

To retain reproducible sources, also replace `design/profile.json` and
`tools/build_profile.py`. The update ZIP includes those files at their repository
paths. The complete ZIP contains the entire latest repo including the fixed MATLAB logo.

Keep your existing `README.md` and other assets. Do not delete or replace the entire
assets folder when applying the animation-only update. No scripts need to run to
publish the supplied, pre-rendered GIFs.

See `design/animation-checks.json` for timing, frame checks and preservation checks.
Local previews are not live GitHub screenshots.

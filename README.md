# Source code concerning the paper Hinaut &amp; Dominey, PLoS ONE 2013

Reference of the paper [freely available here](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0052946):

*Hinaut X, Dominey PF (2013) Real-Time Parallel Processing of Grammatical Structure in the Fronto-Striatal System: A Recurrent Network Simulation Study Using Reservoir Computing. PLoS ONE 8(2): e52946. https://doi.org/10.1371/journal.pone.0052946*

The original code is still [available at PLoS ONE web site as a supplementary material](https://doi.org/10.1371/journal.pone.0052946.s008) of the [paper](https://doi.org/10.1371/journal.pone.0052946). The README with instructions is available comes as [another supplementary material](https://doi.org/10.1371/journal.pone.0052946.s006).

## Python version & dependencies
This code is Python 2 based. It uses Scientific Python librairies (numpy, matplotib), MDP (Modular Processing Toolkit, needed for Oger) and some PDF printing librairies.

You will also need [Oger](https://github.com/neuronalX/Oger) toolbox which is no longer maintained but I provide the version I use for this code [here](https://github.com/neuronalX/Oger).

## Installation
Please refer to the [original README of the paper]()

## Quick try
Open a terminal and clone the repository:

  '''bash
  git clone https://github.com/neuronalX/HinautDominey2013_PLoS_ONE
  cd HinautDominey2013_PLoS_ONE/
  '''

Then try the default experiment with the *small corpus*:

  '''bash
  cd scripts_plos/
  python simple_xp.py
  '''

It will generate PDF files containing the outputs (readouts) of the network in the RES_TEMP/ folder.

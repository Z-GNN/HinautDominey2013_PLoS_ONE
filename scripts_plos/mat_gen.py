# -*- coding: utf-8 -*-
"""
Created on 11 juil. 2012

@author: Xavier HINAUT
xavier.hinaut #/at\# inserm.fr
"""

import mdp
import Oger

def generate_internal_weights(N, spectral_radius=None, proba=0.1, seed=None, randomize_seed_afterwards=False, verbose=False):
    """
    Method that generate the weight matrix that will be used for the internal connections of the Reservoir.
    
    Inputs :

        - verbose: print in the console detailed information.
        - seed: if not None, set the seed of the numpy.random generator to the given value.
        - randomize_seed_afterwards: as the module mdp.numx.random may not be used only by this method,
            the user may want to run several experiments with the same seed only for this method
            (generating the internal weights of the Reservoir), but have random seed for all other
            methods that will use mdp.numx.random.
    """
    if seed is not None:
        mdp.numx.random.seed(seed)
    mask = 1*(mdp.numx_rand.random((N,N))<proba)
    mat = mdp.numx.random.normal(0, 1, (N,N)) #equivalent to mdp.numx.random.randn(n, m) * sd + mu
    w = mdp.numx.multiply(mat, mask)
    if verbose:
        print "Spectra radius of generated matrix before applying another spectral radius: "+str(Oger.utils.get_spectral_radius(w))
    if spectral_radius is not None:
        w *= spectral_radius / Oger.utils.get_spectral_radius(w)
        if verbose:
            print "Spectra radius matrix after applying another spectral radius: "+str(Oger.utils.get_spectral_radius(w))
    if randomize_seed_afterwards:
        """ redifine randomly the seed in order to not fix the seed also for other methods that are using numpy.random methods.
        """
        import time
        mdp.numx.random.seed(int(time.time()*10**6))
    return w

def generate_input_weights(nbr_neuron, dim_input, input_scaling=None, proba=0.1, seed=None, randomize_seed_afterwards=False, verbose=False):
    """
    Method that generate the weight matrix that will be used for the input connections of the Reservoir.
    """
    if seed is not None:
        mdp.numx.random.seed(seed)
    mask = 1*(mdp.numx_rand.random((nbr_neuron, dim_input))<proba)
    mat = mdp.numx.random.randint(0, 2, (nbr_neuron, dim_input)) * 2 - 1
    w = mdp.numx.multiply(mat, mask)
    if input_scaling is not None:
        w = input_scaling * w
    if randomize_seed_afterwards:
        """ redifine randomly the seed in order to not fix the seed also for other methods that are using numpy.random methods.
        """
        import time
        mdp.numx.random.seed(int(time.time()*10**6))
    return w

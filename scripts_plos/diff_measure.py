# -*- coding: utf-8 -*-
"""
Created on 11 juil. 2012

@author: Xavier HINAUT
xavier.hinaut #/at\# inserm.fr
"""

import mdp

def amount_of_change(states_out, verbose=False):
    ## initialization of all the list containing the vectors containing the differences (comparing one step before)
    diff = [mdp.numx.zeros_like(states_out[0])]*len(states_out)
    for idx_so in range(len(states_out)):
        so = states_out[idx_so]
        if verbose:
            print "so.shape", so.shape
        so_diff_tmp = mdp.numx.zeros_like(so) ## so_diff_tmp = mdp.numx.zeros(so.shape[0],so.shape[1])
        for current_time_step in range(1,so.shape[0]): # there is nothing to compute at step 0, so we skip it
            so_diff_tmp[current_time_step,:] = so[current_time_step,:] - so[current_time_step-1,:]
            if verbose:
                print "previous", so[current_time_step-1,:]
                print "actual", so[current_time_step,:]
                print "time step "+ str(current_time_step)
                print "diff", so_diff_tmp[current_time_step,:]
        diff[idx_so] = mdp.numx.copy(so_diff_tmp) #so_diff_tmp[:] #
    return diff

def sum_amount_of_change(diff, return_as_tuple=True, verbose=False):
    """
    Input:
        - diff: list of vector containing the difference (at n time step backward) for the states_out
            this is the output of method amount_of_change()
    """
    if return_as_tuple:
        sum_diff = [mdp.numx.zeros_like(diff[0][:,0])]*len(diff)
        abs_sum_diff = [mdp.numx.zeros_like(diff[0][:,0])]*len(diff)
        abs_max_diff = [mdp.numx.zeros_like(diff[0][:,0])]*len(diff)
    else:
        s_diff = [mdp.numx.zeros_like(diff[0][:,0:2])]*len(diff)
    for idx_diff in range(len(diff)):
        # summing the diff vector on the lines: each line has a single column afterwards
        if return_as_tuple:
            sum_diff[idx_diff] = diff[idx_diff].sum(axis=1)
            abs_sum_diff[idx_diff] = abs(diff[idx_diff]).sum(axis=1)
            abs_max_diff[idx_diff] = mdp.numx.amax(abs(diff[idx_diff]), axis=1)
        else:
            s_diff[idx_diff] = mdp.numx.concatenate((mdp.numx.atleast_2d(diff[idx_diff].sum(axis=1)),
                mdp.numx.atleast_2d(abs(diff[idx_diff]).sum(axis=1)),
                mdp.numx.atleast_2d(mdp.numx.amax(diff[idx_diff], axis=1))), axis=0).transpose()
        if verbose:
            print "diff", diff
            print "sum_diff", sum_diff
            print "abs_sum_diff", abs_sum_diff
            print "abs_max_diff", abs_max_diff
    if return_as_tuple:
        return (sum_diff, abs_sum_diff, abs_max_diff)
    else:
        return s_diff
    

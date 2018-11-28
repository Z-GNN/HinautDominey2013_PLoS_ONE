# -*- coding: utf-8 -*-
"""
Created on 11 juil. 2012

@author: Xavier HINAUT
xavier.hinaut #/at\# inserm.fr
"""

import pylab as pl
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot

def get_labels(l_data, subset, l_offset, initial_pause=True, verbose=False):
    """
    Data is organised in this way:
        - l_data is a list of sentences
        - each sentence is a list of words
        
    The label ticks are generated. Keep in mind that when plotting the ticks are plot like if there is an initial pause (because the tick doesn't begin at x=0).
        
    - offset: represents the difference between the maximum number of words in the data and the number of word of a given sentence.
    - l_offset: is the list of offset for each sentence of l_data
    """
    if subset is None:
        labels = l_data
        offsets = l_offset
    else:
        labels = [l_data[x] for x in subset]
        offsets = [l_offset[x] for x in subset]
    lab_tick = len(labels)*[None]
    for i1 in range(len(labels)):
        lab_tick[i1] = [' ']*offsets[i1]
        for i2 in range(len(labels[i1])): 
            lab_tick[i1].append(labels[i1][i2])
        if initial_pause==False:
            # delete first tick if there is no initial pause (simple way to avoid ticks issues)
            lab_tick[i1] = lab_tick[i1][1:]
        if verbose:
            print "ticks :", lab_tick[i1]
    return (labels, lab_tick)

def plot_output(_outputs, d_io, save_pdf=True, nr_nouns=4, nr_verbs=2, root_file_name="",
                subtitle="", window=0, verbose=False, y_lim=[-1.5,1.5], no_ext_fct=True,
                forced_subset=None):
    print " *** Plotting outputs *** "
    print " * root_file_name="+root_file_name+" - subtitle="+subtitle+" * "
    
    if forced_subset is None:
        subset = d_io['subset']
    else:
        subset = forced_subset
    l_data = d_io['l_data']
    (labels, lab_tick) = get_labels(l_data=l_data, subset=subset,
                                    initial_pause=d_io['initial_pause'], l_offset=d_io['l_offset'])
    if verbose:
        print "d_io['l_output']", d_io['l_output']
    #Windows are separated by sentences and nouns
    TOSpN = 3*nr_verbs  #number of Total Output Signal per Noun (for AOR, it's 3 times the number of verbs)
    
    ## Plotting procedure
    if save_pdf:
        ## Initiate object PdfPages for saving figures
        pp = PdfPages(str(root_file_name)+'_'+str(subtitle)+'.pdf')
    for i in range(len(_outputs)):
        if verbose:
            idx_sentence = subset[i]
            label_sentence = labels[i]
            words_tick = lab_tick[i]
            print "idx_sentence", idx_sentence
            print "i="+str(i)
            print "output[i]", _outputs[i]
            print "label_sentence", label_sentence
            print "len(label_sentence)", len(label_sentence)
            print "words_tick", words_tick
        ## For each sentence, plot as many graphs  as the number of nouns
        for j in range(nr_nouns):
            pl.figure()
            pl.plot(_outputs[i][:,TOSpN*j:TOSpN*(j+1)])
            pl.legend(d_io['l_output'][TOSpN*j:TOSpN*(j+1)], loc='upper left')
            pl.suptitle("Testing sentence "+str(subset[i])+ ": '"+" ".join(labels[i])+"'"+"\n"+subtitle)
            pl.xticks(range(d_io['act_time'],_outputs[i].shape[0],d_io['act_time']))
            a = matplotlib.pyplot.gca()
            if y_lim!=None:
                a.set_ylim(y_lim)
            a.set_xticklabels(lab_tick[i], fontdict=None, minor=False)
            
            if save_pdf:
                # Save figure for each plot
                pp.savefig()
            pl.close()
    if save_pdf:
        ## Close object PdfPages
        pp.close()
    print " * Plot finished * "
    print " *** "
    

def plot_with_output_fashion(l_array, subset, d_io, root_file_name, subtitle="_output_fashion", legend=None, y_lim=None, verbose=False):
    print " *** Plotting with output fashion *** "
    print " * root_file_name="+root_file_name+" - "+subtitle+" * "
    
    (labels, lab_tick) = get_labels(l_data=d_io['l_data'], subset=subset,
                                    initial_pause=d_io['initial_pause'], l_offset=d_io['l_offset'])

    pp = PdfPages(str(root_file_name)+'_'+str(subtitle)+'.pdf')
    
    for i in range(len(l_array)):
        if verbose:
            print "idx_sentence", subset[i]
            print "i="+str(i)
            print "output[i]", l_array[i]
            print "label_sentence", labels[i]
            print "len(label_sentence)", len(labels[i])
            print "words_tick", lab_tick[i]
        pl.figure()
        pl.plot(l_array[i])
        if legend is not None:
            pl.legend(legend)
        
        pl.suptitle("Testing sentence "+str(subset[i])+ ": '"+" ".join(labels[i])+"'"+"\n"+subtitle)
        pl.xticks(range(d_io['act_time'],l_array[i].shape[0],d_io['act_time']))
        a = matplotlib.pyplot.gca()
        if y_lim!=None:
            a.set_ylim(y_lim)
        a.set_xticklabels(lab_tick[i], fontdict=None, minor=False)
        
        pp.savefig()
        pl.close()
    pp.close()
    print " * Plot finished * "
    print " *** "

def plot_array_in_file(root_file_name, array_, data_subset=None, titles_subset=None, plot_slice=None, title="", subtitle="", legend_=None):
    """
    
    inputs:
        array_: is the array or matrix to plot
        data_subset: correspond to the subset of the whole data that is treated. array_ is corresponds to this subset. /
            array_ and subset have to have the same length
        titles_subset: list of subtitles
        plot_slice: slice determining the element of array_ that will be plotted.
    """
    import mdp
    if data_subset is None:
        data_subset = range(len(array_))
    if titles_subset is None:
        titles_subset = ['' for _ in range(len(data_subset))]
        nl_titles_sub = ''
    else:
        nl_titles_sub = '\n'
    if array_==[] or array_==mdp.numx.array([]):
        import warnings
        warnings.warn("Warning: array empty. Could not be plotted. Title:"+str(title))
        return
    if plot_slice is None:
        plot_slice = slice(0,len(data_subset))
    else:
        if (plot_slice.stop-1) > len(data_subset):
            raise Exception, "The last element of the slice is out of the subset."
        subtitle = subtitle+"_slice-"+str(plot_slice.start)+"-"+str(plot_slice.stop)+"-"+str(plot_slice.step)
    ppIS = PdfPages(str(root_file_name)+str(title)+'.pdf')
    
    for i in range(plot_slice.stop)[plot_slice]:
        pl.figure()
        pl.suptitle(title+" "+str(titles_subset[i])+nl_titles_sub+" - seq "+str(data_subset[i])+"\n"+subtitle)
        pl.plot(array_[i])
        if legend_ is not None:
            pl.legend(legend_)
        ppIS.savefig()
        pl.close()
    ppIS.close()
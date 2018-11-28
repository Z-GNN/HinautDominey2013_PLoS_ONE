# -*- coding: utf-8 -*-
"""
Created on 11 juil. 2012

@author: Xavier HINAUT
xavier.hinaut #/at\# inserm.fr
"""

import mdp
import numpy as np
import Oger
    
def check_signal_dimensions(input_signal, target_signal):
    if input_signal.shape != target_signal.shape:
        raise RuntimeError("Input shape (%s) and target_signal shape (%s) should be the same."% (input_signal.shape, target_signal.shape))
    
def keep_max_for_each_time_step_with_default(input_signal, default_min_value=-1.0):
    # get the maximum for each line (= each time step)
    m_arr = np.max(input_signal, axis=1)
    m_arr = np.atleast_2d(m_arr).T
    m_mat = np.concatenate([m_arr for _ in range(input_signal.shape[1])],axis=1)
    # keep only the maximum in each line / for each time step, rest is 0
    return (input_signal >= m_mat)*input_signal + (input_signal < m_mat)*default_min_value    
    
def threshold_and_take_max_before_error(input_signal, target_signal, error_measure, thresh, default_min_value=-1.0):
    """
    First keep only the maximum for each line (i.e. keep the maximum for each time step)
    then applies a threshold to input_signal and target_signal,
    finally determines the error using the error_measure function.
    The threshold is estimated as the mean of the target_signal maximum and minimum unless a threshold 'thresh' is specified
    """
    check_signal_dimensions(input_signal, target_signal)
    
    # check if default_min_value is coherent with the threshold
    if default_min_value >= thresh:
        raise Exception, 'the default value applied after the max is taken is equal or superior to the threshold.'
    
    if thresh == None:
        thresh = (max(target_signal) + min(target_signal)) / 2.
    
    input_signal_max = keep_max_for_each_time_step_with_default(input_signal, default_min_value=default_min_value)
    return error_measure(input_signal_max > thresh, target_signal > thresh)

    

    
class thematic_role_error():
    """
    Specific language error: measure defined for a special language task on thematic role assignment.
    """
    def __init__(self, d_io, error_measure=Oger.utils.loss_01, threshold=0,
                 verbose=False):
        """
        Inputs:
            - d_io: dictionary that gathers parameters and informations on the inputs and outputs
            - error_measure: method used to compute the error on the given interval defined by self.time_step_slice
            - threshold: threshold used by the error_measure to discriminate for binary response.
        """
        self.error_measure = error_measure
        self.threshold = threshold
        self.lt_NVassoc = [('N1','V1'), ('N1','V2'), ('N2','V1'), ('N2','V2'),
                           ('N3','V1'), ('N3','V2'), ('N4','V1'), ('N4','V2')]
        self.d_io_current = d_io
        self.d_io = d_io.copy()
        self.verbose = verbose
        self._check_output_version()
        self.__initialize_error_algorithm()

    def __initialize_error_algorithm(self):
        """
        Definning:
            time_step_slice: start and stop slice for evaluate output signal
            max_answers: maximum number of active outputs
        """
        
        self.time_step_slice = slice(-1+self.d_io_current['full_time'],self.d_io_current['full_time'])
        self.max_answers = self._get_max_answers()
    
    def _check_change_in_d_io(self, just_warning=False):
        if self.d_io_current != self.d_io:
            if just_warning:
                raise Warning, "d_io (dictionary of input/output) has changed since the initialization of object 'thematic_role_error'."
                self.__check_full_time()
                self.__check_output_version()
            else:
                raise Exception, "d_io (dictionary of input/output) has changed since the initialization of object 'thematic_role_error'."

    def _check_output_version(self):
        if not(self.d_io.has_key('l_output')):
            print "!!! WARNING: io dictionary has no 'l_output' entry, version of output could not be checked. !!!"
        elif self.d_io['l_output'] != ['N1-A1','N1-O1','N1-R1','N1-A2','N1-O2','N1-R2','N2-A1','N2-O1','N2-R1','N2-A2','N2-O2','N2-R2','N3-A1','N3-O1','N3-R1','N3-A2','N3-O2','N3-R2','N4-A1','N4-O1','N4-R1','N4-A2','N4-O2','N4-R2']:
            raise Exception, "Output coding is not the same as expected"

    def _get_max_answers(self):
        """
        Return the maximal number of answer for one sentence.
            It corresponds to the maximal length of elements in 'l_teacher'.
        !!! Warning: to be accurate, 'l_teacher' needs to corresponds to the subset selected, and not the full set of data.
        """
        return max([len(x) for x in self.d_io['l_teacher']])

    def _get_NVassoc_sliced(self, input_signal, target_signal, verbose=False):
        """
        Output:
            (NVassoc_admiting_anwser, NVassoc_not_present_in_sent)
            Each element of this tuple is a list. Each element of a list is a 3-tuple:
                - 1st: index of the Noun-Verb association in the 'self.lt_NVassoc' list of tuples
                - 2nd: sub-matrix (sub-numpyarray) of the input_signal that will be used by error_measure
                - 3rd: sub-matrix (sub-numpyarray) of the teacher_signal that will be used by error_measure
                
        !Warning: this method rely on a specific way of coding the output signal.
            If this coding is changed, you may have to recode most of this method.
                
        Notation:
            Nva: Noun-Verb association
        
        NB: some precisions on what is the problem that have to deal the algorithm:
            It should infer which NVa-s (Noun-Verb association) are present in the sentence
            -- this means inferring how many Open Class Words (~Nouns) and how many meanings
             there is by looking to the teacher output signals --,
            In this method we do it by inferring from the target_signal (because the input corpus is not available).
        """
        ## The Noun-Verb associations (i.e. full AOR for a given noun respect to a given verb)
        ##    that admit answer are the NVassoc that have at the same time
        ##    Noun and Verb with one teacher at 1 (one of the AOR for the NVassoc).
        ##    The different NVassoc possible are given by self.lt_NVassoc.
        if verbose:
            print "<<< Beginning method _get_NVassoc_sliced():"
            print "self.time_step_slice", self.time_step_slice
        
        ## check if this version of error computation is ok with the way output is coded
        self._check_output_version()
        
        ## creating NVassoc
        NVassoc_admiting_anwser = []
        NVassoc_not_admiting_answer = []
        l_N_V_present_in_sentence = []
        ## Finding which Nouns, Verbs and association of Noun-Verb are present in the sentence
        for idx in range(0,21+1,3):
            NVindex = int(idx/3)
            current_NVassoc = (NVindex, input_signal[self.time_step_slice, idx:idx+3], target_signal[self.time_step_slice, idx:idx+3])
#            if mdp.numx.any(target_signal[self.time_step_slice, idx:idx+3]):
            if mdp.numx.any(target_signal[self.time_step_slice, idx:idx+3] > self.threshold): # the non-1 signal could be 0 or -1 (so np.any() is not sufficient)
                ## add the current NVassoc to the list
                NVassoc_admiting_anwser.append(current_NVassoc)
                ## add the noun and the verb to the list of Noun and Verb present in the sentence (will be used later)
                    # there will be duplicate, but this is not an issue
                l_N_V_present_in_sentence.extend(self.lt_NVassoc[NVindex])
            else:
                NVassoc_not_admiting_answer.append(current_NVassoc)
        if verbose:
            print "target_signal.shape", target_signal.shape
            print "self.time_step_slice", self.time_step_slice
            print "target_signal[self.time_step_slice, idx:idx+3].shape", target_signal[self.time_step_slice, idx:idx+3].shape
            print " NVassociations admiting anwser: "
            for NVi in NVassoc_admiting_anwser:
                print "  - "+str(self.lt_NVassoc[NVi[0]])+" _ "+str(NVi)
            print " NVassociations not admiting anwser: "   
            for NVi in NVassoc_not_admiting_answer:
                print "  - "+str(self.lt_NVassoc[NVi[0]])+" _ "+str(NVi)
        
        ## create list of NVassoc_not_admiting_answer but present in the sentence
        NVassoc_not_admiting_answer_but_present = []
        NVassoc_not_present_in_sent = []
        # for each NVa in NVassoc_not_admiting_answer,
        for NVi in NVassoc_not_admiting_answer:
            # if its Noun (i.e. self.lt_NVassoc[NVi[0]][0]) or its Verb (i.e. self.lt_NVassoc[NVi[0]][1]) is not present in the sentence
            if l_N_V_present_in_sentence.count(self.lt_NVassoc[NVi[0]][0])==0 \
                or l_N_V_present_in_sentence.count(self.lt_NVassoc[NVi[0]][1])==0: 
                # put it in a new list containing the NVa not present in setence
                NVassoc_not_present_in_sent.append(NVi)
            #if N and V are present in the NVa
            else: 
                #add it to the new list
                NVassoc_not_admiting_answer_but_present.append(NVi)
        if verbose:
            print " NVassociations not admiting anwser, but present: "
            for NVi in NVassoc_not_admiting_answer_but_present:
                print " - "+str(self.lt_NVassoc[NVi[0]])+" _ "+str(NVi)
            print " NVassociations not admiting anwser and not present: "   
            for NVi in NVassoc_not_present_in_sent:
                print "  - "+str(self.lt_NVassoc[NVi[0]])+" _ "+str(NVi)

        if (len(NVassoc_admiting_anwser)+len(NVassoc_not_admiting_answer_but_present)+len(NVassoc_not_present_in_sent)) != len(self.lt_NVassoc):
            raise Exception, "The number of Noun-Verb association is not correct. Should be "+str(len(self.lt_NVassoc))
        
        if verbose:
            print ">>> End of method _get_NVassoc_sliced():"
        
        return (NVassoc_admiting_anwser, NVassoc_not_admiting_answer_but_present, NVassoc_not_present_in_sent)

    def compute_error(self, input_signal, target_signal, verbose=False):
        """
        Inputs:
            input_signal: output readout activity
            target_signal: teacher output used for the supervised learning
        Outputs:
            (mean of meaning errors, mean of sentence errors,
                number of erroneous Noun/action, number of pertinent Noun/action, list of NVa that are correct, list of NVa that are incorrect)
        The 2nd line gathers results not used in default mode. Use this information to know more on errors.
        """
        check_signal_dimensions(input_signal, target_signal)
        self._check_change_in_d_io()
        
        ## initialization
        perf_asso_adm_answ = [] #performance of NVa admiting answer
        (NVassoc_admiting_anwser, NVassoc_not_admiting_answer_but_present, NVassoc_not_present_in_sent) = \
            self._get_NVassoc_sliced(input_signal, target_signal, verbose=False)
        NVa_correct = []
        NVa_erroneous = []
        
        ## Computing errors and impossible states for NVa admiting answer
        for NVi in NVassoc_admiting_anwser:
            ## Evaluate fraction of time when the good answer if given for the 3 signal AOR at the same time
            err_answer = threshold_and_take_max_before_error(input_signal=NVi[1],
                                                           target_signal=NVi[2],
                                                           error_measure=self.error_measure,
                                                           thresh=self.threshold)
            perf_asso_adm_answ.append(1 - err_answer)
            if err_answer > 0:
                NVa_erroneous.append(NVi[0])
            else:
                NVa_correct.append(NVi[0])
                
            if verbose:
                print "NVassoc_admiting_anwser: "+str(self.lt_NVassoc[NVi[0]])+" _ "+str(NVi)
                print "only max of NVa", keep_max_for_each_time_step_with_default(NVi[1])
                print "err_answer="+str(err_answer)
        
        ## Computing errors and impossible states for NVa not admiting answer, but present in the sentence
        perf_asso_not_adm_answ_p = [] #performance of NVa not admiting answer, but present
        for NVi in NVassoc_not_admiting_answer_but_present:
            err_answer = threshold_and_take_max_before_error(input_signal=NVi[1],
                                                       target_signal=NVi[2],
                                                       error_measure=self.error_measure,
                                                       thresh=self.threshold)
            perf_asso_not_adm_answ_p.append(1 - err_answer)
            if err_answer > 0:
                NVa_erroneous.append(NVi[0])
            else:
                NVa_correct.append(NVi[0])
            if verbose:
                print "NVassoc_not_admiting_answer_but_present: "+str(self.lt_NVassoc[NVi[0]])+" _ "+str(NVi)
                print "only max of NVa", keep_max_for_each_time_step_with_default(NVi[1])                
                print "print err_answer="+str(err_answer)
        
        ## Compute means
        if perf_asso_adm_answ != []:
            if perf_asso_not_adm_answ_p != []:
                aa = perf_asso_adm_answ
                naap = perf_asso_not_adm_answ_p
                perf_asso_present = (len(aa)*mdp.numx.mean(aa) + len(naap)*mdp.numx.mean(naap)) / float((len(aa) + len(naap)))
            else:
                perf_asso_present = mdp.numx.mean(perf_asso_adm_answ)
        else:
            raise Exception, "There is no answer for this sentence."

        # compute the fraction of time when all the pertinent NVa are correct (for NVa present in the sentence)
        all_output_signal = []
        all_target_signal = []
        for NVi in NVassoc_admiting_anwser:
            all_output_signal.append(keep_max_for_each_time_step_with_default(NVi[1]))
            all_target_signal.append(NVi[2])
        for NVi in NVassoc_not_admiting_answer_but_present:
            all_output_signal.append(keep_max_for_each_time_step_with_default(NVi[1]))
            all_target_signal.append(NVi[2])
        global_out_arr = mdp.numx.concatenate(all_output_signal, axis=1)
        global_target_arr = mdp.numx.concatenate(all_target_signal, axis=1)
        global_err_answer = Oger.utils.threshold_before_error(input_signal=global_out_arr,
                                                   target_signal=global_target_arr,
                                                   error_measure=self.error_measure,
                                                   thresh=self.threshold)
        
        ## Supplementary computations (not used in default program)
        ## Compute the number of pertinent SW (semantic word) outputs for each verb that is erroneous
        # i.e. number of erroneous NV-assoc
        total_nr_of_pertinent_SW = len(NVassoc_admiting_anwser) + len(NVassoc_not_admiting_answer_but_present)
        nr_of_erroneous_SW = int(round(total_nr_of_pertinent_SW * (1-perf_asso_present)))
        if total_nr_of_pertinent_SW != (len(NVa_erroneous)+len(NVa_correct)):
            raise Exception, "Incoherent total_nr_of_pertinent_SW. total_nr_of_pertinent_SW"+str(total_nr_of_pertinent_SW)+ \
                "\n NVa_correct="+str(NVa_correct)+ \
                "\n NVa_erroneous="+str(NVa_erroneous)
        if nr_of_erroneous_SW != len(NVa_erroneous):
            raise Exception, "Incoherent nr_of_erroneous_SW." \
                +"\nnr_of_erroneous_SW="+str(nr_of_erroneous_SW)+ \
                "\n NVa_correct="+str(NVa_correct)+ \
                "\n len(NVa_erroneous)="+str(len(NVa_erroneous))
        if verbose:
            print "all_output_signal", all_output_signal
            print "global activity (only max was kept)", global_out_arr
            print "global_out_arr.shape", global_out_arr.shape
            print "global_err_answer", global_err_answer
            print "total_nr_of_pertinent_SW", total_nr_of_pertinent_SW
            print "nr_of_erroneous_SW", nr_of_erroneous_SW
            print "SW level error: ", (1-perf_asso_present)
            
        
        return (1 - perf_asso_present, global_err_answer,
                nr_of_erroneous_SW, total_nr_of_pertinent_SW, NVa_correct, NVa_erroneous)


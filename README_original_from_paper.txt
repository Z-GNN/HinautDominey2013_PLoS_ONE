Instructions for running simulations corresponding to Experiment 1 - 4, and the tests on effects of reservoir size and simulation time step.
The simulations are run in python, using the Oger toolbox.  Thus we require installation of python and Oger.
Installation instructions for both python and Oger, and download for Oger can be found at:
http://www.reservoir-computing.org/installing_oger
Here, links for python are presented, along with the Oger download.  Note that when installing python, the following should be included:
The required dependencies for Oger are:
Python 2.6 or higher
Numpy 1.1 or higher  
Scipy 0.7 or higher
Matplotlib 0.99 or higher
MDP 3.0 or higher
This is clearly explained on the oger page.   In general, when choosing parameters for the python installation, check all dependencies.

Instructions:
1. Install python and Oger

2.  Download the python scripts and unzip.  go into the scripts_plos directory

3. open a python shell
OR
3 bis. open a terminal

4. go to (cd) HinautSM3Zipped\scripts_plos

5. type:  run simple_xp
OR
5 bis. type: python simple_xp.py 
The parameters are pre-set to correspond to Experiment 1.  

6.  look in the ..\RES_TEMP directory and there will be two output files created corresponding to the readout activity, and the temporal derivative signals (corresponding to the ERP signals).  The readout activity corresponds to that seen in Figure 2
The readout neuron activity should be comparable to that in the Supplementary material part 2.

7.  change parameters for different tests
Parameters that can be modified are:
activation_time (act_time):  corresponds to the number of time steps activation time for each input. The current value is 20.
number of neurons (N): in the reservoir.  Current value is 300
training data (subset):  These are the sentences that are used to train the reservoir.  Current value is: subset = range(15,41) 

Try changing the number of neurons to 30 to see some performance degradation.  Try 100.


8.  Experiment 2 part 1:  This will produce the results in Figure 3.
uncomment this line
#   subset= range(15,45) # Exp 2 part 1
and comment the line: subset= range(15,41) # Exp1

9.  Experiment 2 part 2:  This will produce the results seen in Figures 4 and 5 (for the readout and temporal derivitive files, respectively)
uncomment the following lines
#   subset= range(15,42) #  Exp 2 part 2
#    subset.remove(24)   #  Exp 2 part 2
#    subset.remove(25)   #  Exp 2 part 2
#    subset.remove(26)   #  Exp 2 part 2
#    subset.remove(27)   #  Exp 2 part 2
#    subset.remove(32)   #  Exp 2 part 2
#    subset.remove(33)   #  Exp 2 part 2
#    subset.remove(38)   #  Exp 2 part 2
#    subset.remove(39)   #  Exp 2 part 2
and comment any other subset lines

Examine the run_multi_simple_xp_test_data 15_abs_sum_diff.pdf to see the "ERP" responses.  compare in Part 1 and Part 2.
Try with subset= range(15,42)

10.  Experiment 3 Generalization:
set N = 100, act_time = 1, n_folds = -1 (this does the cross validation leaving one out),  nr_instance=10 (ten repetitions),  plot_output=False (this saves much time in generating the plots - can turn it on, but then better to set nr_instances to 1).

to see the graphic outputs, set nr_instance=1, and plot_output=True
try with act_time =  20, compare plots for construction 16, 17, 23 and 27 with figure 6.

try with activation times = 1, 5, 10, 20

try changing seed (the random number generator seed value used to initialize connections).

11.  Experiment 4 Discourse processing:  this produces results illustrated in Figure 7.
set parameters back to those for Experiment 1
uncomment
   subset= range(0,45)  # Exp 4
and comment any other subset lines

look at sentence 0, 1, 10 and 11 compared with Fig 7

If you want to save a history of different output files (without overwriting), set root_file_name='../RES_TEMP/run_multi_simple_xp' with a different prefix than run_multi_simple_xp

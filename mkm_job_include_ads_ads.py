#!/usr/bin/env python
#LSF -q suncat
#LSF -n 1
#LSF -W 40:10
#LSF -e err.log

from catmap import ReactionModel
from catmap import analyze
import numpy as np
import cPickle as pickle
import os
import sys
import commands

loc = os.getcwd()

name = ['0.00', '0.5','0.6', '0.7','0.8','0.9', '1.0']
num = len(name)

n = 0
os.mkdir(name[n])
os.chdir(name[n])
os.system('cp '+ loc +'/energies.txt .')
os.system('cp '+ loc +'/EtOH.mkm .')
mkm_file = 'EtOH.mkm'
model = ReactionModel(setup_file=mkm_file)

model.output_variables += ['consumption_rate','production_rate','selectivity','zero_point_energy','enthalpy','entropy','free_energy','carbon_selectivity']
model.output_variables += ['interaction_matrix','interacting_energy','equilibrium_constant','gas_pressure']

model.products =['CH3CH2OH_g','CH3CHO_g','CH3OH_g','CH4_g','H2O_g']
model.reactants =['H2_g','CO_g']

model.run()

vm = analyze.VectorMap(model)
vm.log_scale = True #rates should be plotted on a log-scale
vm.min = 1e-10 #minimum rate to plot
vm.max = 1e0 #maximum rate to plot
vm.threshold = 1e-25 #do not plot rates below this
vm.plot_variable = 'production_rate'
vm.subplots_adjust_kwargs['wspace'] = 0.55
vm.plot(save='production_rate.pdf')

sa = analyze.ScalingAnalysis(model)
sa.plot(save='scaling.pdf')

f = open('converged','w')
f.write('converged')
f.close()

os.chdir('..')

for n in range(1,num):
    if not os.path.exists(name[n]):
	os.mkdir(name[n])
	os.chdir(name[n])
	os.system('cp '+ loc +'/' + name[n-1] +'/*.* .')
	os.system('sed -i \'/interaction_strength/d\' EtOH.mkm')
	cmd2 = 'echo \"interaction_strength = \"' + name[n] + ' >> EtOH.mkm'
	os.system(cmd2)

	include_rate_control = False
	mkm_file = 'EtOH.mkm'
	model = ReactionModel(setup_file=mkm_file)
#model.create_standalone = True

	model.output_variables += ['consumption_rate','production_rate','selectivity','zero_point_energy','enthalpy','entropy','free_energy','carbon_selectivity']
	model.output_variables += ['interaction_matrix','interacting_energy','equilibrium_constant','gas_pressure']
	if include_rate_control:
    		model.output_variables += ['rate_control']

	model.products =['CH3CH2OH_g','CH3CHO_g','CH3OH_g','CH4_g','H2O_g']
	model.reactants =['H2_g','CO_g']
	
	model.run()

	vm = analyze.VectorMap(model)
	vm.log_scale = True #rates should be plotted on a log-scale
	vm.min = 1e-10 #minimum rate to plot
	vm.max = 1e0 #maximum rate to plot
	vm.threshold = 1e-25 #do not plot rates below this
	vm.plot_variable = 'production_rate'
	#vm.include_labels = ['CH3CH2OH_g', 'CH3CHO_g', 'CH4_g','CH3OH_g']
	vm.subplots_adjust_kwargs['wspace'] = 0.55
	vm.plot(save='production_rate.pdf')

	vm = analyze.VectorMap(model)
        vm.log_scale = True #rates should be plotted on a log-scale
        vm.min = 1e-10 #minimum rate to plot
        vm.max = 1e0 #maximum rate to plot
        vm.threshold = 1e-25 #do not plot rates below this
        vm.plot_variable = 'consumption_rate'
        #vm.include_labels = ['CH3CH2OH_g', 'CH3CHO_g', 'CH4_g','CH3OH_g']
        vm.subplots_adjust_kwargs['wspace'] = 0.55
        vm.plot(save='consumption_rate.pdf')

        vm.plot_variable = 'rate'
        vm.subplots_adjust_kwargs['wspace'] = 0.55
        vm.plot(save='rates.pdf')

	vm2 = analyze.VectorMap(model)
	vm2.plot_variable = 'coverage'
	vm2.log_scale = False
	vm2.min = 0
	vm2.max = 1
	vm2.plot(save='coverage.pdf')

	vm2.plot_variable = 'selectivity'
	vm2.subplots_adjust_kwargs['wspace'] = 0.55
	vm2.plot(save='selectivity.pdf')
	
#	sa = analyze.ScalingAnalysis(model)
#	sa.plot(save='scaling.pdf')

#model.model_summary(summary_file='model_info.tex')

	f = open('converged','w')
	f.write('converged')
	f.close()

	os.chdir('..')



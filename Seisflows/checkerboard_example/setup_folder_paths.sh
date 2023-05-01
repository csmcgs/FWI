#!/bin/sh

workdir=$(dirname $(realpath $0))
echo "Setting workdir to ${workdir}"

seisflows par path_workdir $workdir
seisflows par path_scratch $workdir/scratch
seisflows par path_eval_grad $workdir/scratch/eval_grad
seisflows par path_output $workdir/output
seisflows par path_model_init $workdir/model_init
seisflows par path_model_true $workdir/model_true

seisflows par path_output_log $workdir/sflog.txt
seisflows par path_state_file $workdir/sfstate.txt
seisflows par path_log_files $workdir/logs
seisflows par path_eval_func $workdir/scratch/eval_func
seisflows par path_specfem_bin $workdir/bin
seisflows par path_specfem_data $workdir/DATA
seisflows par path_solver $workdir/scratch/solver

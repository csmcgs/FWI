# Seisflows

This repository contains the following folders:

### RunwithContainer
In this folder you'll find 3 Jupyter notebooks to run seisflows with the container created for the 2022 specfem user's workshop (intruction to pull and run the container: https://github.com/adjtomo/adjdocs/blob/main/readmes/docker_image_install.md). 

Paste the jupyter notebooks to the empty directory where you will run the container. This folder will be binded to the home/scoped/work directory in the container. Now in the container locate to the home/scoped/work directory and run the jupyter notebooks. Before runing any of the B_ you'll need to run the A_ notebook, as described below:

1) run A_CreateInitialandTrueModels.ipynb to create the initial and true models. This script will create the folder "specfem2d_workdir"
2) run B1_RunSeisflows_Complete.ipynb if you wanna run the complete workflow for the paremeters defined in the parameters.yaml.
3) run B2_RunSeisflows_Complete.ipynb if you want to see how to stop in different phases of the workflow.

To run B1_RunSeisflows_Complete.ipynb or B2_RunSeisflows_Complete.ipynb the directory must be clean unless you wanna continue from a certain iteration. If you want to re-start the inversion use the command seisflows restart. 

some of the commands can be found in the following link:
https://seisflows.readthedocs.io/en/latest/command_line_tool.html#seisflows-restart 

### Runwithworkstation
If you installed seisflows in your computer you can use the files in the folder specfem2d_workdir to run the same example available in the jupyter notebooks for the container. To run this example in the terminal, relocate to the folder where you saved specfem2d_workdir and use the following commands.

```
# activate the environment where seisflows was installed 
conda activate seisflows

# seisflows help
seisflows -h

# create  parfile 
seisflows setup -f
cat parameters.yaml

# Change to inversion workflow
seisflows par workflow inversion
seisflows par preprocess pyaflowa
seisflows par optimize LBFGS

# Fill parameters file with default values 
seisflows configure

# Modify parfile
seisflows par ntask 3  # set the number of sources/events to use
seisflows par nproc 1  # set the number of sources/events to use
seisflows par materials elastic  # update Vp and Vs during inversion
seisflows par end 5    # final iteration -- we will only run 1
seisflows par data_case synthetic  # synthetic-synthetic means we need both INIT and TRUE models
seisflows par components Y  # this default example creates Y-component seismograms
seisflows par step_count_max 10  # limit the number of steps in the line search
seisflows par smooth_h 5000  # smoothing distance 
seisflows par smooth_v 5000  # smoothing distance
seisflows par min_period 10  # tmin
seisflows par max_period 200 # tmax
seisflows par filter_corners 4 # limit the number of steps in the line search


# define paths (in the parfile)
seisflows par path_workdir /Users/andreacamilarianoescandon/Work/specfem2d_users_workshopv3
seisflows par path_specfem_bin /Users/andreacamilarianoescandon/packages/specfem2d/bin
seisflows par path_specfem_data /Users/andreacamilarianoescandon/Work/specfem2d_users_workshopv3/specfem2d_workdir/DATA
seisflows par path_model_init /Users/andreacamilarianoescandon/Work/specfem2d_users_workshopv3/specfem2d_workdir/OUTPUT_FILES_INIT
seisflows par path_model_true /Users/andreacamilarianoescandon/Work/specfem2d_users_workshopv3/specfem2d_workdir/OUTPUT_FILES_TRUE

% use binary models as input
cd specfem2d_workdir/DATA
seisflows sempar model gll
seisflows sempar use_existing_STATIONS .true.

% workflow list 
seisflows print tasks

# run workflow
seisflows submit

# plotting results (e.g., model_init, model_true, gradient and final model after iteration 5)
seisflows plot2d MODEL_INIT vs --savefig m_init_vs.pn 
seisflows plot2d MODEL_TRUE vs --savefig m_true_vs.png
seisflows plot2d GRADIENT_05 vs_kernel --savefig g_05_vs.png
seisflows plot2d MODEL_05 vs --savefig m_05_vs.png

```

You can also use the notebooks I created for the container in your pc, but for that you need to create a kernel in jupyter notebook to be able to use the conda environment "seisflows"
https://medium.com/@nrk25693/how-to-add-your-conda-environment-to-your-jupyter-notebook-in-just-4-steps-abeab8b8d084 





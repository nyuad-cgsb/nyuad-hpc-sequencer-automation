This is the beginning of a pipeline to use airflow https://airflow.apache.org/start.html to automate sequence protocols.

* Rsync from sequence server to /work/gencore/ (only in this example though as future runs will be written directly to $WORK).
* BCL2FASTQ (with no demux since it's only phix, other runs will need to be demuxed using the corresponding SampleSheet).
* Rsync the resulting fastqs to /scratch/gencore/novaseq/180710_A00534_0022_AHFY3KDMXX/
* Tar the whole run folder (with the fastqs) on $WORK.
* ssh into archive3 and rsync the tarball from $WORK to /archive/gencore/ (and verify the transfer with md5 checksums).
* Delete the run (and it's tarball) from $WORK

## Installation

Bootstrap an environment with the environment.yml of the repo.

```
conda env create -f environment.yml -p $HOME/software/airflow
```

This only installs the default packages, which are not suitable for a production environment. More information on starting a production environment coming soon.

At the time of writing airflow does not work with python 3.7 because of a namespace issue.

## Getting Starting

Once the packages are installed, you must first initialize the airflow database.


```
source activate $HOME/software/airflow
airflow initdb
## The scheduler and the webserver run continuously and will have to be run in different windows / tmux panes
## Ensure the environment is sourced with source activate $HOME/software/airflow
airflow scheduler
airflow webserver
```

If you haven't unset the load_examples from airflow.cfg, you might get some errors about kubernetes. Don't worry about these, or just set load_examples as False in the config.

~/airflow/airflow.cfg (or $AIRFLOW_HOME/airflow.cfg)

```
#load_examples = True
load_examples = False
```

## Dags and Plugins

In order to get airflow to see the dags and plugins here you need to modify the airflow.cfg, which is in ${AIRLFOW_HOME}/airflow.cfg. Default is ~/airflow/airflow.cfg

```
dags_folder = /home/airflow/airflow/dags
plugins_folder = /home/airflow/airflow/plugins
```

To $(pwd)/plugins and $(pwd)/dags

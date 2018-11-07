This is the beginning of a pipeline to use airflow https://airflow.apache.org/start.html to automate sequence protocols.

```
Rsync from sequence server to /work/gencore/ (only in this example though as future runs will be written directly to $WORK).
BCL2FASTQ (with no demux since it's only phix, other runs will need to be demuxed using the corresponding SampleSheet).
Rsync the resulting fastqs to /scratch/gencore/novaseq/180710_A00534_0022_AHFY3KDMXX/
Tar the whole run folder (with the fastqs) on $WORK.
ssh into archive3 and rsync the tarball from $WORK to /archive/gencore/ (and verify the transfer with md5 checksums).
Delete the run (and it's tarball) from $WORK
```

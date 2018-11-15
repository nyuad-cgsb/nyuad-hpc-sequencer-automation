import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

@NgModule({
  imports: [
    CommonModule
  ],
  declarations: []
})
export class BiosailsWorkflowsModule {
  public selectedWorkflow: string;
  public selectedQCWorkflow: string;
  public availableWorkflows: string[] = [
    '/scratch/gencore/workflows/stable/QC-QT-PE-nextseq.yml',
    '/scratch/gencore/workflows/stable/QC-QT-PE-nextseq-noTrimming-NEW.yml',
    '/scratch/gencore/workflows/stable/QC-QT-PE-nextseq-noTrimming.yml',
    '/scratch/gencore/workflows/stable/rnaseq_without_DGE-HISAT2-Mouse_ensembl-82.yml',
    '/scratch/gencore/workflows/stable/chipseq-noPeaks-deeptools2-mouse10.yml',
    '/scratch/gencore/workflows/stable/rnaseq_kallisto.yml',
    '/scratch/gencore/workflows/stable/atac-seq-zf.yml',
    '/scratch/gencore/workflows/stable/alignment_only-diatom-BWA-MEM.yml',
    '/scratch/gencore/workflows/stable/rnaseq_without_DGE-HISAT2-Human_ensembl-81.yml',
    '/scratch/gencore/workflows/stable/rnaseq_without_DGE-Mouse10-Nextseq.yml',
    '/scratch/gencore/workflows/stable/QC-QT-MP.yml',
    '/scratch/gencore/workflows/stable/QC-QT-PE.yml',
    '/scratch/gencore/workflows/stable/rnaseq_without_DGE-DM.yml',
    '/scratch/gencore/workflows/stable/de_novo_sequencing.yml',
    '/scratch/gencore/workflows/stable/rnaseq_ercc.yml',
    '/scratch/gencore/workflows/stable/QC-QT-SE.yml',
    '/scratch/gencore/workflows/stable/rnaseq_without_DGE-HISAT2-Diatom.yml',
    '/scratch/gencore/workflows/stable/rnaseq_without_DGE-Mouse10.yml',
    '/scratch/gencore/workflows/stable/non-model-resequencing-dpDario-BWA-MEM.yml',
    '/scratch/gencore/workflows/stable/rnaseq_without_DGE-ZF.yml',
    '/scratch/gencore/workflows/stable/rnaseq_without_DGE-Human38p2.yml',
    '/scratch/gencore/workflows/stable/non-model-resequencing-diatom-BWA-MEM.yml',
    '/scratch/gencore/workflows/stable/rip-seq-mouse10.yml',
    '/scratch/gencore/workflows/stable/trimmomatic_qc.yml',
    '/scratch/gencore/workflows/stable/contamination_checking_human-mouse-zf.yml',
    '/scratch/gencore/workflows/stable/chipseq-noPeaks-deeptools2-human38.yml',
    '/scratch/gencore/workflows/stable/trimmomatic_qc-split-reads.yml',
    '/scratch/gencore/workflows/stable/resequencing-human-complete.yml',
    '/scratch/gencore/workflows/stable/non-model-resequencing.yml',
    '/scratch/gencore/workflows/stable/non-model-resequencing-dpPilion.yml',
    '/scratch/gencore/workflows/stable/non-model-resequencing-BWA-MEM.yml',
    '/scratch/gencore/workflows/stable/non-model-resequencing-anolis-BWA-MEM.yml'];

  public availableQCWorkflows: string[] = [
    '/scratch/gencore/workflows/stable/QC-QT-PE-nextseq.yml',
    '/scratch/gencore/workflows/stable/QC-QT-PE-nextseq-noTrimming-NEW.yml',
    '/scratch/gencore/workflows/stable/QC-QT-PE-nextseq-noTrimming.yml',
    '/scratch/gencore/workflows/stable/QC-QT-MP.yml',
    '/scratch/gencore/workflows/stable/QC-QT-PE.yml',
    '/scratch/gencore/workflows/stable/QC-QT-SE.yml',
    '/scratch/gencore/workflows/stable/trimmomatic_qc.yml',
    '/scratch/gencore/workflows/stable/trimmomatic_qc-split-reads.yml',
  ];

}

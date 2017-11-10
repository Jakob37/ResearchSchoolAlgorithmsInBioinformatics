# Introduction

The purpose of this demonstration is to explore how batch effects influences
the behaviour of a label-free quantification proteomics dataset.

It is generated using the OpenMS tool `MSSimulator`. Intensities are generated on protein level
using a custom script which uses two separate FASTA files to generate background and spike-in
data with different intensities. Spike-in levels are then determined as a fold compared
to a base-line intensity.

The batch effect is applied as a fixed shift to a subselection of samples which is picked across
the different biological conditions.



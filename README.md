# Univeristy of Luxembourg - Master Thesis Replication Package
By Vinicius Amaro Cechin

## Abstract

Continuous delivery is well-established method known for enabling software development teams to enhance their performance on software delivery. Applying continuous delivery, implies (technically speaking) to implement a deployment pipeline. It is of utmost importance for development teams practising continuous delivery to know what are the fundamental elements required to be included in a deployment pipeline to meet continuous delivery. The goal of this thesis was to identify and classify the common constitutive elements of a deployment pipeline, how they are grouped and in which order they appear. 

A systematic literature review (SLR) and a Data Mining methodology were used to select and extract relevant information, followed by a triangulation of the results. This thesis provides a strong, rigorous, replicable and up-to-date description of the state-of-the-art on deployment pipeline's activities, which was validate by the triangulation with the results from mining real pipeline implementations and annotating their activities with the described activities.

Over 22 activities that were extracted from the papers during the SLR, only 2 were not found during the repositories mining, which were `NFR` and `Regression testing` activities. Also, over the 5 activities that appeared the most in both research methodologies, only one diverged between them, which consisted of the `Communication` activities for the SLR and `Pre-processing` activities for the Data Mining. These results can benefit both researchers and practitioners interested in the design and analysis of deployment pipelines.

## RQs

The research questions aimed at being answered based on the collected evidence are:

*RQ1:* What are the type of activities and how are they grouped into a deployment pipeline?

*RQ2:* What is the order in which these activities are performed by the deployment pipeline?

## Folder Structure

```bash
Master Thesis Replication Package
├───MSR
|   ├───data
|   └───src
└───SLR
    └───data
```
Where:

1. MSR folder contains the data necessary to replicate the mining procedures executed to achieve the thesis results. As well as the annotated pipeline configuration files after the manual annotation process described in the thesis.
2. SLR folder contains the reports, charts, lists and links generated during the systematic literature review executed in this thesis. No paper is directly made available, but links where they are available can be found in the available materials of this replication package.
## Explainable Classification of Brain Networks via Contrast Subgraphs

[Tommaso Lanciano](https://phd.uniroma1.it/web/LANCIANO-TOMMASO_nP1661409_EN.aspx) (Sapienza University, Rome), [Francesco Bonchi](http://www.francescobonchi.com/) (ISI Foundation, Turin & Eurecat, Barcelona), and [Aristides Gionis](https://www.kth.se/profile/argioni) (KTH, Stockholm).

_Mining human-brain networks to discover patterns that can be used to discriminate between healthy individuals and patients affected by some neurological disorder, is a fundamental task in neuroscience. Learning simple and interpretable models is as important as mere classification accuracy. In this paper we introduce a novel approach for classifying brain networks based on extracting contrast subgraphs, i.e., a set of vertices whose induced subgraphs are dense in one class of graphs and sparse in the other. We formally define the problem and present an algorithmic solution for extracting contrast subgraphs. We then apply our method to a brain-network dataset consisting of children affected by Autism Spectrum Disorder and children Typically Developed. Our analysis confirms the interestingness of the discovered patterns, which match background knowledge in the neuroscience literature. Further analysis on other classification tasks confirm the simplicity, soundness, and high explainability of our proposal, which also exhibits superior classification accuracy, to more complex state-of-the-art methods._

---

This repository contains the code necessary to implement algorithms described in the paper "Explainable classification of brain networks via contrast subgraphs", KDD 2020.

This package is free for research, academic and non-profit making purposes only. If you use this piece of software for your work and got something published please include the citation reported below. The software may not be sold or redistributed without prior approval. One may make copies of the software for their use provided that the copies, are not sold or distributed, are used under the same terms and conditions. As unestablished research software, this code is provided on an "as is" basis without warranty of any kind, either expressed or implied. The downloading, or executing any part of this software constitutes an implicit agreement to these terms. These terms and conditions are subject to change at any time without prior notice.


<strong>TERMS OF USAGE:</strong>
The following paper should be cited in any research product whose findings are based on the code here distributed:

- Tommaso Lanciano, Francesco Bonchi, and Aristides Gionis. 2020. Explainable Classification of Brain Networks via Contrast Subgraphs. In Proceedings of the 26th ACM SIGKDD Conference on Knowledge Discovery and Data Mining (KDD ’20), August 23–27, 2020, Virtual Event, CA, USA. ACM, New York, NY, USA, 11 pages. https://doi.org/10.1145/3394486.3403383
<p>

### Requirements

The code has been tested with:

* Python 2.7
* Matlab R2019a
* CVX
* Networkx==1.9

### Folders
* datasets: datasets listed in Table 1.
* icdm16-egoscan: code of the work by [Cadena et al.](https://ieeexplore.ieee.org/document/7837829), released by the authors.

### Execution

In order to run our code, download [CVX](http://cvxr.com/cvx/download/), unzip the folder and place it in "icdm16-egoscan".

Then, run the following command: 'python cs.py [-h] [-p {1,2}] d a b alpha'

#### Positional arguments:
  * d           &nbsp;&nbsp;&nbsp;&nbsp;dataset
  * a          &nbsp;&nbsp;&nbsp;&nbsp;Group A
  * b          &nbsp;&nbsp;&nbsp;&nbsp;Group B
  * alpha      &nbsp;&nbsp;&nbsp;&nbsp;alpha


#### Optional arguments:
  * -h, --help  
    show the help message and exit	
  * -p       &nbsp;&nbsp;&nbsp;&nbsp;Problem  
  	Problem Forumlation (default: 1)
  	
#### Examples:
'python cs.py children td asd 0.05'  
'python cs.py adolescents asd td 0.08 -p 2'  
  
### Contacts
Mail to [tommaso.lanciano@uniroma1.it](mailto:tommaso.lanciano@uniroma1.it) for any question.

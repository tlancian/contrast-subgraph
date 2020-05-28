## Explainable classification of brain networks via contrast subgraphs

[Tommaso Lanciano](https://phd.uniroma1.it/web/LANCIANO-TOMMASO_nP1661409_EN.aspx) (Sapienza University, Rome), [Francesco Bonchi](http://www.francescobonchi.com/) (ISI Foundation, Turin & Eurecat, Barcelona), and [Aristides Gionis](https://www.kth.se/profile/argioni) (KTH, Stockholm).

This repository contains the code necessary to implement algorithms described in the paper "Explainable classification of brain networks via contrast subgraphs", KDD 2020.

This package is free for research, academic and non-profit making purposes only. If you use this piece of software for your work and got something published please include the citation reported below. The software may not be sold or redistributed without prior approval. One may make copies of the software for their use provided that the copies, are not sold or distributed, are used under the same terms and conditions. As unestablished research software, this code is provided on an "as is" basis without warranty of any kind, either expressed or implied. The downloading, or executing any part of this software constitutes an implicit agreement to these terms. These terms and conditions are subject to change at any time without prior notice.


<strong>TERMS OF USAGE:</strong>
The following paper should be cited in any research product whose findings are based on the code here distributed:

- T. Lanciano, F. Bonchi, A. Gionis.<br>
Explainable classification of brain networks via contrast subgraphs.<br>
Proceedings of the 26th ACM SIGKDD International Conference on Knowledge Discovery and Data Mining (KDD 2020). San Diego, CA, USA - August 23-27, 2020.
<p>

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

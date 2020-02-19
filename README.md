## Explainable classification of brain networks via contrast subgraphs

[Tommaso Lanciano](https://phd.uniroma1.it/web/LANCIANO-TOMMASO_nP1661409_EN.aspx) (Sapienza University, Rome), [Francesco Bonchi](http://www.francescobonchi.com/) (Eurecat, Barcelona & ISI Foundation, Turin), and [Aristides Gionis](https://www.kth.se/profile/argioni) (KTH, Stockholm).

### Folders
* datasets: datasets listed in Table 1.
* icdm16-egoscan: code of the work by [Cadena et al.](https://ieeexplore.ieee.org/document/7837829), released by the authors.

### Execution

In order to run our code, download [CVX](http://cvxr.com/cvx/download/), unzip the folder and place it in "icdm16-egoscan".

Then, run the following command: 'python cs.py [-h] [-p P] d c1 c2 a'

#### Positional arguments:
  * d           &nbsp;&nbsp;&nbsp;&nbsp;dataset
  * c1          &nbsp;&nbsp;&nbsp;&nbsp;First Group of Networks
  * c2          &nbsp;&nbsp;&nbsp;&nbsp;Second Group of Networks
  * a          &nbsp;&nbsp;&nbsp;&nbsp;alpha


#### Optional arguments:
  * -h, --help  
    show the help message and exit	
  * -p       &nbsp;&nbsp;&nbsp;&nbsp;Problem  
  	Problem formulation. "1" for Problem 1, "2" for Problem 2. (default: 1)
  	
#### Examples:
'python cs.py children td asd 0.05'  
'python cs.py adolescents td asd 0.08 -p 2'  
  
### Contacts
Mail to [tommaso.lanciano@uniroma1.it](mailto:tommaso.lanciano@uniroma1.it) for any question.

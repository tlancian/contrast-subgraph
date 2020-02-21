## Explainable classification of brain networks via contrast subgraphs

[Tommaso Lanciano](https://phd.uniroma1.it/web/LANCIANO-TOMMASO_nP1661409_EN.aspx) (Sapienza University, Rome), [Francesco Bonchi](http://www.francescobonchi.com/) (ISI Foundation, Turin & Eurecat, Barcelona), and [Aristides Gionis](https://www.kth.se/profile/argioni) (KTH, Stockholm).

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

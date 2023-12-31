# Doctor Residency Assignment Program
## Authors
* Sijun Wang
* Haochen Wang
## Description
This program assigns doctors to residencies based on the rating from each doctor on the positions. It takes an array of 
ratings as input, in which each row represents entries from a single doctor and each column corresponds to the ratings 
for a residence position. The program uses Hungarian algorithm to complete the assignment and greedy algorithm to
evaluate the effectiveness of the implementation.
## Usage
Type in the rating entries (each row corresponds to ratings from the same doctor, and each column represents the rating 
given to each hospital), then run the program and receive an assignment array, in which an entry of "1" assigns the 
doctor of the row to the residency in the column.
## Assumptions
   * Candidates provide their rating for all hospitals.
   * Ties in ranking from each candidate are allowed.
   * There are more or equal number of positions compared to the number of doctors, and to match the real-world 
scenario, some doctors may not get an assignment.
   * Ignore the preference and selection process from the hospitals.
   * When discovering conflicts in assignment (such as when all doctors give the same rating for each hospital), doctors
who showed equal preference to the residency are randomly assigned to the position
## Reference
[1] “How it works,” NRMP, https://www.nrmp.org/intro-to-the-match/how-matching-algorithm-works/ 
(accessed Sep. 6, 2023). 

[2] Cmglee, “File:Hungarian algorithm unbalanced assignment problem example.svg,” Wikimedia Commons, 
https://commons.wikimedia.org/wiki/File:Hungarian_algorithm_unbalanced_assignment_problem_example.svg#/media/File:Hungarian_algorithm_unbalanced_assignment_problem_example.svg 
(accessed Sep. 6, 2023). 

[3] Munkres - munkres implementation for python, https://software.clapper.org/munkres/ (accessed Sep. 6, 2023). 

[4] Bmc, “BMC/Munkres: Munkres algorithm for python,” GitHub, https://github.com/bmc/munkres 
(accessed Sep. 6, 2023). 
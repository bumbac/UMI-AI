# Automated planning using Lilotane

\['li·lo·tein], **Li**fted **Lo**gic for **Ta**sk **Ne**tworks:  
SAT-driven Totally-ordered Hierarchical Task Network (HTN) Planning [0]

### Assignment #4 for NI-UMI 2021

Problem of planning is in finding an ordered set of actions that lead from initial state to goal.


#### Problem assignment 

Navrhněte  plánovací  doménu  pro  úlohu  s opicí  a  vysoko  visícími  banány.  Opice  se  může 
pohybovat mezi místy A, B, a C, které jsou rozmístěny v lince. Banány jsou na místě B. Dále 
v úloze vystupuje krabice, která je umístěná na místě A. Opice ze země na banány nedosáhne, 
ale  může  vylézt  na  krabici,  ze  které  už  na  banány  dosáhne.  Krabicí  opice  může  posouvat, 
přitom ale musí být na stejném místě jako krabice. Následující ilustrace ukazuje v jaké situaci 
se opice na začátku nachází.  
 
  
Nabízí  se  použít  následující  operátory,  jejichž  význam  v doméně  je  očekávatelný  a  proto 
uvedeme jen názvy: Go, Push, ClimbUp, ClimbDown, Grasp, Ungrasp. 
 
**a)** V navržené doméně sestavte [plán](https://gitlab.fit.cvut.cz/sutymate/ni-umi/blob/master/4/src/Manual_monkey_plan.txt), kterým se opice zmocní banánů. 

**b)** Upravte  [cíl](https://gitlab.fit.cvut.cz/sutymate/ni-umi/blob/master/4/src)  tak,  aby  opice  zmátla  vědce,  kteří  ji  pozorují,  tj.  zmocnila  se  banánů,  ale 
zároveň uvedla prostředí do původního stavu (krabice zpět na své místo). 

**c)** Úlohu řešte automaticky pomocí nějakého plánovače účastnícího se soutěže IPC.

  [Riešenie 1](https://gitlab.fit.cvut.cz/sutymate/ni-umi/blob/master/4/src/solution1.txt)
  
  [Riešenie 2](https://gitlab.fit.cvut.cz/sutymate/ni-umi/blob/master/4/src/confuse_scientist_solution.txt)

  I have chosen **Lilotane** [0] from IPC 2021 competition. This planner uses SAT solver (glucose4 in this task)
  to find totally ordered hierarchical plan.

**d)** V prostředí se bude vyskytovat více krabic dvou typů, a  sice lehké a těžké. S těžkými 
opice  nedokáže  pohnout  s lehkými  ano.  Modifikujte  doménu,  aby  tyto  vlastnosti 
operátory zohledňovaly. 


[0] Schreiber, D. (2021). [**Lilotane: A Lifted SAT-based Approach to Hierarchical Planning.**](https://doi.org/10.1613/jair.1.12520) In Journal of Artificial Intelligence Research (JAIR) 2021 (70), pp. 1117-1181.

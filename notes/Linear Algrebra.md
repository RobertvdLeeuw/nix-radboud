
| Operations             |                           |
| ---------------------- | ------------------------- |
| Exchange rows          | $E_i \leftrightarrow E_j$ |
| Multiply by $c \neq 0$ | $E_i \coloneq cE_i$       |
| Add $c \neq 0$         | $E_i \coloneq E_i + cE_j$ |

Echelon form: every pivot (first non-zero element) in row has more leading zeroes than the last row
System is inconsistent **iff** it contains a row with only zeroes before | and non-zero after (0x  = 7)
System has 1 unique solution **iff** its echelon form contains as many pivots as variables
Reduced echelon form: every pivot = 1 and is only non-zero in column
## Gauss-elimination
1. **Rows with trailing zeroes**: row exchange to reduce those
2. Pick any row, make first element 1 by multiplying by constant
3. Pick another row, add/subtract and/or multiply to make first element 0
4. Make first non-zero element of that row 1
5. Repeat until (reduced) echelon form

## Homogenous
Trivial solution: all = 0, basic: non-trivial
If pivots (k) < vars (n): (k-n) different basic solutions
$$H = c_1H_1 + ... + c_{n-k}H_{n-k}$$
### To find $H(_i)$
1. Convert system to echelon form
2. For each non-pivot col:
	1. Keep it and all pivot cols
	2. Find non-zero solution for this system
	3. Augment with 0's on removed columns
	4. That's $H_i$
3. That's $H$

$$S=P+H \text{ , where }P = \text{a particular solution for the nonhomo}$$


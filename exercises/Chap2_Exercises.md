# GIN400 / GIN540 – Advanced Database Systems
## Chapter 2: Query Optimization – Exercise Sheet

> Use the formulas from the course slides (Prof. J. Zalaket). Round **up** (⌈ ⌉) for numbers of blocks, runs and passes.
> Worked solutions are in [Chap2_Solutions.md](Chap2_Solutions.md). Try every question yourself before you look at them.

---

## Part A – Concepts

### Exercise 1 – Short answers
1. Define **query processing** and **query optimization**. How does the optimizer estimate the cost of a plan?
2. What is a **query block**? How are nested queries and aggregate operators handled?
3. List the catalog information used in cost functions, (a) about the file and (b) about its indexes.
4. Define **selectivity (sl)** and **selection cardinality (s)**. Give the estimate of `sl` for an equality condition on (a) a key attribute and (b) a non-key attribute.
5. Compare **materialization** and **pipelining**. Give two operations where pipelining is not always possible.
6. What is the difference between a **query tree** and a **query graph**?
7. Name and briefly explain the **four steps of query decomposition**.
8. What is the difference between a **linear** join tree and a **bushy** join tree? Why do optimizers often restrict themselves to linear trees?
9. Explain how `SELECT MAX(SALARY) FROM EMPLOYEE` can be evaluated (a) with an ascending B+-tree index on SALARY and (b) without one. What changes for `SUM`/`COUNT` with a dense index compared with a non-dense index?
10. State the three main rules of heuristic optimization.

### Exercise 2 – True or False (justify each answer in one line)
1. Linear search (S1) can only be used if the file is ordered on the selection attribute.
2. Binary search on a unique (key) attribute costs `log2 b` block accesses.
3. A query graph tells the system which operation to perform first.
4. Pipelined evaluation can always be applied, unlike materialization.
5. When more than about 5% of the tuples are retrieved, a full table scan is usually cheaper than using an unclustered index.
6. In block nested-loop join, the smaller relation should normally be the outer relation.
7. CNF is generally preferred over DNF for representing the WHERE clause.
8. The cost of a partition hash join is `3(bR + bS) + bRES`.
9. If the buffer size `nB < √b`, external sort-merge needs more than one merge pass.
10. A projection whose attribute list contains a key of R needs duplicate elimination.
11. Restricting the search to linear join trees makes the search space larger than with bushy trees.
12. For a join `R.A = S.B` where A is a key of R, the join selectivity satisfies `js ≤ 1/|R|`.

---

## Part B – Cost Estimation for SELECTION

### Exercise 3
Consider the relation

`STUDENT (SID, NAME, EMAIL, MAJOR, YEAR, GPA, DEPTID, CITY)`

Catalog information:
- `r = 40,960` records, `bfr = 10` records/block
- The file is **physically ordered on SID** (primary key)

Access paths:
| # | Access path | Statistics |
|---|---|---|
| 1 | Primary index on SID | `x = 3` |
| 2 | Static hash on EMAIL (key) | – |
| 3 | Secondary B+-tree index on DEPTID | `x = 2`, `bI1 = 20`, `d = 64` |
| 4 | Secondary B+-tree index on YEAR | `x = 1`, `d = 4` |
| 5 | Secondary B+-tree index on GPA | `x = 3`, `bI1 = 200` |

**Questions**
- (a) Compute the number of blocks `b`.
- (b) `σ SID = 12345 (STUDENT)`: give the cost using S1, S2 and S3. Which method is best?
- (c) `σ EMAIL = 'ali@uni.edu' (STUDENT)`: give the cost with static hashing. What would it be with extendible hashing?
- (d) `σ DEPTID = 7 (STUDENT)`: compute `sl` and `s`, then compare S1 with S7-a. What percentage of the tuples is retrieved?
- (e) `σ YEAR = 2 (STUDENT)`: compute `s` and compare S1 with S7-a. Explain the result using the 5% rule.
- (f) `σ GPA > 3.5 (STUDENT)`: compare S1 with S7-b.
- (g) `σ SID > 30000 (STUDENT)`: which method applies (other than S1)? Give its cost.
- (h) `σ DEPTID = 7 AND YEAR = 2 (STUDENT)`: which method (S8) should be used and how is it executed? Estimate the number of resulting records, assuming the attributes are independent and uniformly distributed.
- (i) *What-if:* suppose the file were instead **physically ordered on DEPTID** and had a **clustering index** on DEPTID with `x = 2`. Compute the cost of `σ DEPTID = 7` using S2 and S6.

---

## Part C – External Sort-Merge

### Exercise 4
A file has `b = 2000` blocks.

- (a) With `nB = 6` buffer blocks: compute the number of initial runs `nR` (and the size of the last run), the degree of merging `dM`, the number of passes `nP` and the number of runs left after each pass. Then compute the total cost.
- (b) Repeat (a) with `nB = 11`.
- (c) What happens if `nB = 2001`? Give the cost.
- (d) What is the **minimum** `nB` for which a **single merge pass** is enough? Give the cost in that case and relate your answer to the `√b` rule.
- (e) **Trace:** a file contains the keys
  `44, 12, 87, 3, 56, 21, 9, 70, 35, 18`
  with **one record per block** and `nB = 3`. Show the runs produced in Phase I, the content of each merge pass in Phase II, and the total cost given by the formula.

---

## Part D – Join Cost Estimation

### Exercise 5
`STUDENT ⋈ DEPTID = DNUM DEPARTMENT`

- **STUDENT:** `rS = 40,960`, `bS = 4096`; secondary index on DEPTID: `xDEPTID = 2`, `dDEPTID = 64` (so `sDEPTID = 640`). STUDENT is physically ordered on SID.
- **DEPARTMENT:** `rD = 64`, `bD = 8`; **primary index** on DNUM: `xDNUM = 1`.
- Buffer: `nB = 6` blocks. Blocking factor of the result file: `bfrRES = 5`.

**Questions**
- (a) Compute the join selectivity `js`, the size of the result `|STUDENT ⋈ DEPARTMENT|` and `bRES`.
- (b) **J1 (basic nested-loop, worst case):** compute the cost with STUDENT as the outer loop and then with DEPARTMENT as the outer loop.
- (c) **J1 improved (block nested-loop with nB − 2 blocks for the outer relation):** compute both costs again.
- (d) What is the smallest `nB` that brings the improved J1 with DEPARTMENT as outer down to its **best case**? Give that cost.
- (e) **J2 (single-loop with index):** compute the cost (i) with STUDENT as outer, using the primary index on DNUM, and (ii) with DEPARTMENT as outer, using the secondary index on DEPTID.
- (f) **J3 (sort-merge join):** which of the two files actually needs sorting? *(Hint: look at the indexes.)* Compute the full cost using the external sort-merge cost formula with `nB = 6`.
- (g) **J4 (hash join):** compute the cost.
- (h) Rank all strategies from cheapest to most expensive and say which plan the optimizer should choose.

---

## Part E – Query Decomposition

Use the running schema:

```
EMPLOYEE   (SSN, FNAME, MINIT, LNAME, TITLE, BDATE, ADDRESS, SEX, SALARY, SUPERSSN, DNO)
DEPARTMENT (DNUMBER, DNAME, MGRSSN, MGRSTARTDATE)
PROJECT    (PNUMBER, PNAME, PLOCATION, DNUM)
WORKS_ON   (ESSN, PNO, HOURS)
```

### Exercise 6
- (a) **Normalization.** Write the following qualification in CNF and in DNF, and say which form is better and why:
  ```sql
  WHERE EMPLOYEE.SSN = WORKS_ON.ESSN
    AND (WORKS_ON.PNO = 'P1' OR WORKS_ON.PNO = 'P2')
    AND WORKS_ON.HOURS > 10
  ```
- (b) **Analysis.** For each query, say whether it is correct, *type incorrect* or *semantically incorrect*. Justify, and correct it where you can.
  1. `SELECT PNAME FROM EMPLOYEE WHERE SALARY > 1000;`
  2. `SELECT * FROM PROJECT WHERE PNAME > 25;`
  3. ```sql
     SELECT E.FNAME
     FROM   EMPLOYEE E, DEPARTMENT D, WORKS_ON W
     WHERE  E.SSN = W.ESSN AND W.HOURS > 10 AND D.DNAME = 'HR';
     ```
     *(Draw the query graph.)*
- (c) **Simplification.** Simplify the following using the idempotency rules, naming the rule used at each step:
  ```sql
  SELECT LNAME
  FROM   EMPLOYEE
  WHERE  (SALARY > 3000 AND SALARY > 3000)
     OR  (DNO = 5 AND NOT (DNO = 5))
     OR  (SEX = 'F' AND (SEX = 'F' OR TITLE = 'Engineer'));
  ```

---

## Part F – Heuristic Optimization (Query Trees)

### Exercise 7
```sql
SELECT E.LNAME, P.PNAME
FROM   EMPLOYEE E, WORKS_ON W, PROJECT P, DEPARTMENT D
WHERE  E.SSN = W.ESSN
  AND  W.PNO = P.PNUMBER
  AND  P.DNUM = D.DNUMBER
  AND  D.DNAME = 'Research'
  AND  E.SALARY > 50000
  AND  W.HOURS > 20;
```
- (a) Draw the **initial (canonical) query tree**: Cartesian products of the relations, then one selection, then the projection.
- (b) Apply the reconstruction rules **step by step**. At each step name the rule used (cascade of σ, commuting σ with ×/⋈, turning σ + × into ⋈, commuting π with ⋈, ordering the joins).
- (c) Draw the **final optimized tree**, showing the attributes kept by each projection.
- (d) Explain the join order you chose (which join is the most restrictive and why?).
- (e) Is your final tree linear or bushy? How many join orders does the `O(N!)` estimate give for this query?

---

## Part G – Full Case Study (cost-based comparison of plans)

### Exercise 8
```
CUSTOMER (cid, cname, city, age)
ORDERS   (oid, cid, odate, amount, status)
```
- **ORDERS:** `bO = 2000` blocks, `bfrO = 50` → `rO = 100,000`; `status` has `d = 5` distinct values (uniform).
- **CUSTOMER:** `bC = 400` blocks, `bfrC = 25` → `rC = 10,000`; `city` has `d = 20` distinct values (uniform).
- `cid` is the key of CUSTOMER. Memory buffer: `nB = 5` blocks.

```sql
SELECT C.cname
FROM   ORDERS O, CUSTOMER C
WHERE  O.cid = C.cid AND O.status = 'SHIPPED' AND C.city = 'Beirut';
```
Ignore the cost of writing the final result unless asked.

- (a) **Plan 1 (naive):** basic nested-loop join with the selections and the projection done on the fly. Compute the cost with CUSTOMER as outer and with ORDERS as outer.
- (b) **Plan 2:** push the selections down. Linear search on each table and write the results to temporary files T1 = σ status(ORDERS) and T2 = σ city(CUSTOMER). Then sort T1 and T2 with external sort-merge and join them with a sort-merge join. Give every partial cost and the total.
- (c) **Plan 3:** same as Plan 2, but join T1 and T2 with a **hash join**.
- (d) **Plan 4:** same as Plan 2, but join T1 and T2 with an **improved (block) nested-loop join** using T2 as outer.
- (e) **Plan 5:** suppose a **primary index** on CUSTOMER.cid exists with `x = 2`. Build T1 as before, then use a **single-loop join (J2)** that probes CUSTOMER for every T1 record and checks `city` in memory. Compute the cost.
- (f) Rank the plans. Which one should be chosen? Which heuristic does this example confirm?
- (g) Estimate the number of tuples in the result. If `bfrRES = 100`, what is `bRES`?
- (h) **Challenge – pipelining:** in Plan 3, suppose the selections are *pipelined* straight into the partitioning phase of the hash join, so T1 and T2 are never materialized. Estimate the new total cost and the saving.

---
*End of exercise sheet.*

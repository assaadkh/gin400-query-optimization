# GIN400 / GIN540 – Chapter 2: Query Optimization
## Worked Solutions

> These are the solutions to [Chap2_Exercises.md](Chap2_Exercises.md). The formula sheet is at the end.

---

## Part A – Concepts

### Exercise 1 – Short answers
1. **Query processing** turns a high-level declarative query (SQL, a form of relational calculus) into an equivalent low-level procedural query (relational algebra) and executes it. **Query optimization** chooses, among all the equivalent evaluation plans, the one with the lowest estimated cost. The cost combines I/O and CPU and is estimated from statistics in the **system catalog** (number of tuples, tuple size, number of blocks, indexes, and so on).
2. A **query block** is the basic unit that is translated into algebra and optimized. It contains one `SELECT-FROM-WHERE` expression, plus `GROUP BY`/`HAVING` if present. Each **nested query** becomes a **separate query block**, and the optimizer picks a plan for every block. **Aggregate operators** must be expressed in the *extended* relational algebra.
3. (a) **File:** number of records `r`, record size `R`, number of blocks `b`, blocking factor `bfr`.
   (b) **Indexes:** number of levels `x` of each multilevel index, number of first-level index blocks `bI1`, number of distinct values `d` of an attribute, selectivity `sl`, selection cardinality `s`.
4. `sl = (# records satisfying the condition) / r`, with `0 ≤ sl ≤ 1`. `s = sl × r` is the number of records satisfying the condition.
   (a) Key attribute: `sl = 1/r`, so `s = 1`. (b) Non-key attribute: `sl = 1/d`, so `s = r/d`.
5. **Materialization** evaluates one operation at a time, from the bottom up, and stores each intermediate result on disk. It is *always applicable*, but writing and re-reading the temporary files is expensive. **Pipelining** evaluates several operations at once and passes tuples straight to the parent operation without storing them. It is much cheaper but *not always possible*, for example with **external sort** and **hash join**, which need their whole input before they can produce output.
6. A **query tree** corresponds to a **relational algebra** expression. The relations are the leaves and the operations are the internal nodes, so the tree implies an **order of execution**. A **query graph** corresponds to a **relational calculus** expression. It does **not** indicate an order of operations, and there is only **one** graph per query.
7. (1) **Normalization:** put the qualification into CNF/DNF. (2) **Analysis:** detect and reject type-incorrect or semantically incorrect queries. (3) **Simplification:** remove redundant predicates using the idempotency rules. (4) **Rewriting:** translate into relational algebra (transformation), then restructure the operator tree for performance (reconstruction).
8. In a **linear** join tree, every join has at least one **base relation** as an operand. In a **bushy** tree, some joins have no base relation as operand (both operands are intermediate results). With N relations there are `O(N!)` equivalent trees. Restricting to linear trees cuts the search space to about `O(2^N)`, which makes optimization tractable.
9. (a) With an ascending index, follow the **rightmost** pointer of each node from the root down to the rightmost leaf to get MAX. For MIN, follow the leftmost path.
   (b) Without an index, do a **full table scan**.
   With a **dense** index (one entry per record), SUM/COUNT/AVG can be computed from the index entries alone. With a **non-dense** index, you must also account for the actual number of records behind each index entry.
10. (1) First apply the operations that **reduce the size of intermediate results**. (2) Perform **selections and projections as early as possible**, which means pushing them down the tree. (3) Execute the **most restrictive** selections and joins before the others, which means reordering the leaves.

### Exercise 2 – True / False
| # | Answer | Justification |
|---|:---:|---|
| 1 | **F** | S1 works whatever the condition, file ordering or indexes. |
| 2 | **T** | S2 on a key: `C = log2 b`. |
| 3 | **F** | A query graph imposes no order. The query tree does. |
| 4 | **F** | It is the other way round: materialization is always applicable, pipelining is not (sort, hash join). |
| 5 | **T** | This is the rule stated on slide 12. |
| 6 | **T** | The outer relation is read once and the inner one is read `⌈bouter/(nB−2)⌉` times, so a smaller outer means fewer passes over the inner. |
| 7 | **T** | Queries contain more ANDs than ORs, and DNF repeats the conjunctions, which causes redundant work. |
| 8 | **T** | Partition phase (read + write) = `2(bR+bS)`, probe phase = `bR+bS`, plus `bRES`. |
| 9 | **T** | Fewer than `√b` buffers gives more runs than can be merged at once. |
| 10 | **F** | A key makes every projected tuple unique, so there are no duplicates. |
| 11 | **F** | Linear trees **reduce** the search space, to about `O(2^N)`. |
| 12 | **T** | Each S tuple matches at most one R tuple, so `|R⋈S| ≤ |S|` and `js ≤ |S|/(|R||S|) = 1/|R|`. |

---

## Part B – Selection Costs (Exercise 3)

**(a)** `b = r / bfr = 40,960 / 10 = 4096 blocks`.

**(b)** `σ SID = 12345` (SID is the key, and the file is ordered on SID):
| Method | Formula | Cost |
|---|---|---|
| S1 linear (key, stop when found) | `b/2` | 4096/2 = **2048** |
| S2 binary (key) | `log2 b` | log2 4096 = **12** |
| S3 primary index | `x + 1` | 3 + 1 = **4** |

✅ The best method is **S3, with 4 block accesses**.

**(c)** Static hashing (S4): **C = 1**. Extendible hashing: **C = 2** (one access for the directory and one for the bucket).

**(d)** `σ DEPTID = 7`, a non-key attribute:
- `sl = 1/d = 1/64`, so `s = 40,960 / 64 = 640` records.
- S1: `C = b = 4096` (non-key, so the whole file must be scanned).
- S7-a: `C = x + s = 2 + 640 = 642`.
- Percentage retrieved: 640 / 40,960 = **1.56 %**, which is below 5%.

✅ **Use the secondary index (642)**.

**(e)** `σ YEAR = 2`: `s = 40,960 / 4 = 10,240` records (25% of the table).
- S1: `4096`
- S7-a: `1 + 10,240 = 10,241`

✅ **Linear scan (4096)** is better. We retrieve 25% of the tuples, far above 5%. An unclustered index costs roughly one block access per record, while a scan reads each block once.

**(f)** `σ GPA > 3.5`:
- S7-b: `x + bI1/2 + r/2 = 3 + 200/2 + 40,960/2 = 3 + 100 + 20,480 = 20,583`
- S1: `4096`

✅ **Linear scan**.

**(g)** `σ SID > 30000`: this is a range condition on the key with an **ordering (primary) index**, so **S5** applies:
`C = x + b/2 = 3 + 2048 = 2051` (compared with S1 = 4096). ✅ **S5**.

**(h)** Conjunctive selection (S8). Compute the cost of each individual condition:
| Condition | Method | Cost |
|---|---|---|
| DEPTID = 7 | S7-a | 642 |
| YEAR = 2 | S7-a | 10,241 |
| (whole condition) | S1 | 4096 |

✅ Use the **DEPTID index** to retrieve the 640 records, then test `YEAR = 2` on each record **in the memory buffer**. Total cost: **642**.

Estimated result size: `s = r × (1/64) × (1/4) = 40,960 / 256 = 160` records.

**(i)** The file is ordered on DEPTID and has a clustering index (`s = 640`, `bfr = 10`, so the matching records fill `⌈640/10⌉ = 64` blocks):
- S6: `x + ⌈s/bfr⌉ = 2 + 64 = 66`
- S2: `log2 b + ⌈s/bfr⌉ − 1 = 12 + 64 − 1 = 75`

✅ **S6, with 66 block accesses**. Compare this with the 642 of the unclustered index in (d): physically clustering the matching records makes a big difference.

---

## Part C – External Sort-Merge (Exercise 4)

The formulas used are:
`nR = ⌈b/nB⌉`, `dM = min(nB−1, nR)`, `nP = ⌈log_dM(nR)⌉`, `Cost = 2b(1 + nP)`.

**(a)** `b = 2000`, `nB = 6`
- `nR = ⌈2000/6⌉ = 334` runs: 333 runs of 6 blocks and a last run of **2** blocks (333 × 6 = 1998).
- `dM = min(5, 334) = 5`
- `nP = ⌈log5 334⌉ = 4`, because 5³ = 125 < 334 ≤ 625 = 5⁴.
- Runs after each pass: 334 → **67** → **14** → **3** → **1**.
- `Cost = 2 × 2000 × (1 + 4) = ` **20,000** block I/Os.

**(b)** `nB = 11`
- `nR = ⌈2000/11⌉ = 182` runs: 181 runs of 11 blocks and a last run of **9** blocks.
- `dM = min(10, 182) = 10`
- `nP = ⌈log10 182⌉ = 3`
- Runs after each pass: 182 → **19** → **2** → **1**.
- `Cost = 2 × 2000 × 4 = ` **16,000**.

**(c)** `nB = 2001 ≥ b`: the whole file fits in memory, giving a single run and **no merge phase** (`nP = 0`).
`Cost = 2b = ` **4000** (read once, write once).

**(d)** For a single merge pass we need `nB − 1 ≥ ⌈b/nB⌉`.
- `nB = 45`: `nR = ⌈2000/45⌉ = 45` but `dM = 44 < 45`, so 2 passes are needed. ✗
- `nB = 46`: `nR = ⌈2000/46⌉ = 44` and `dM = min(45, 44) = 44`, so `nP = 1`. ✓

✅ **The minimum is nB = 46**, with `Cost = 2 × 2000 × 2 = 8000`. This matches the slide rule: `√2000 ≈ 44.7`, and with fewer than about `√b` buffers several merge passes are needed.

**(e)** Trace with `nB = 3` and one record per block (`b = 10`):

*Phase I – create runs (load 3 blocks, sort, write):*
```
Run 1: [12, 44, 87]
Run 2: [ 3, 21, 56]
Run 3: [ 9, 35, 70]
Run 4: [18]
```
`nR = ⌈10/3⌉ = 4`, `dM = min(3−1, 4) = 2` (two input buffers and one output buffer).

*Phase II – merge (2-way):*
```
Pass 1: Run1 + Run2 → [3, 12, 21, 44, 56, 87]
        Run3 + Run4 → [9, 18, 35, 70]
Pass 2: → [3, 9, 12, 18, 21, 35, 44, 56, 70, 87]
```
`nP = ⌈log2 4⌉ = 2`, so `Cost = 2 × 10 × (1 + 2) = ` **60**.

---

## Part D – Join Costs (Exercise 5)

**(a)** DNUM is the key of DEPARTMENT, so `js = 1/|DEPARTMENT| = 1/64`.
`|STUDENT ⋈ DEPARTMENT| = js × rS × rD = (1/64) × 40,960 × 64 = 40,960` tuples. Every student matches exactly one department.
`bRES = 40,960 / 5 = ` **8192** blocks.

**(b)** J1, basic nested loop: `Cost = bouter × binner + bouter + bRES`
- STUDENT outer: `4096 × 8 + 4096 + 8192 = 32,768 + 4096 + 8192 = ` **45,056**
- DEPARTMENT outer: `8 × 4096 + 8 + 8192 = 32,768 + 8 + 8192 = ` **40,968**

**(c)** J1 improved: `Cost = ⌈bouter/(nB−2)⌉ × binner + bouter + bRES`, with `nB − 2 = 4`.
- STUDENT outer: `⌈4096/4⌉ × 8 + 4096 + 8192 = 1024 × 8 + 4096 + 8192 = ` **20,480**
- DEPARTMENT outer: `⌈8/4⌉ × 4096 + 8 + 8192 = 2 × 4096 + 8 + 8192 = ` **16,392**

**(d)** The best case is reached when the whole outer relation fits in the `nB − 2` buffers: `nB − 2 ≥ 8`, so **nB = 10**.
`Cost = bD + bS + bRES = 8 + 4096 + 8192 = ` **12,296**.

**(e)** J2, single-loop join:
- (i) STUDENT outer, primary index on DNUM:
  `bS + rS × (xDNUM + 1) + bRES = 4096 + 40,960 × 2 + 8192 = 4096 + 81,920 + 8192 = ` **94,208**
- (ii) DEPARTMENT outer, secondary index on DEPTID:
  `bD + rD × (xDEPTID + sDEPTID) + bRES = 8 + 64 × (2 + 640) + 8192 = 8 + 41,088 + 8192 = ` **49,288**

**(f)** J3, sort-merge join.
DEPARTMENT has a **primary index on DNUM**, so it is already **physically sorted** on the join attribute and needs no sorting. STUDENT is ordered on SID, not on DEPTID, so it **must be sorted**.

Sorting STUDENT (`b = 4096`, `nB = 6`):
- `nR = ⌈4096/6⌉ = 683`, `dM = min(5, 683) = 5`
- `nP = ⌈log5 683⌉ = 5`, because 5⁴ = 625 < 683 ≤ 3125. Runs after each pass: 683 → 137 → 28 → 6 → 2 → 1.
- `Sort cost = 2 × 4096 × (1 + 5) = 49,152`

`Cost J3 = bS + bD + sort(STUDENT) + bRES = 4096 + 8 + 49,152 + 8192 = ` **61,448**

**(g)** J4, hash join: `3 × (bS + bD) + bRES = 3 × (4096 + 8) + 8192 = 12,312 + 8192 = ` **20,504**

**(h)** Ranking, with `nB = 6`:
| Rank | Strategy | Cost |
|:---:|---|---:|
| 1 | **J1 improved, DEPARTMENT outer** | **16,392** |
| 2 | J1 improved, STUDENT outer | 20,480 |
| 3 | J4 hash join | 20,504 |
| 4 | J1 basic, DEPARTMENT outer | 40,968 |
| 5 | J1 basic, STUDENT outer | 45,056 |
| 6 | J2, DEPARTMENT outer (secondary index) | 49,288 |
| 7 | J3 sort-merge | 61,448 |
| 8 | J2, STUDENT outer (primary index) | 94,208 |

✅ Choose the **block nested-loop join with DEPARTMENT as the outer relation**. DEPARTMENT is tiny (8 blocks), so STUDENT is scanned only twice. The unclustered index in J2 loses because each of the 640 matching students per department costs one block access. Note that `bRES = 8192` is the same for every method, so it cannot change the ranking.

---

## Part E – Query Decomposition (Exercise 6)

**(a)** Let `j = (EMPLOYEE.SSN = WORKS_ON.ESSN)`, `p1 = (PNO='P1')`, `p2 = (PNO='P2')`, `h = (HOURS > 10)`.
- **CNF:** `j ∧ (p1 ∨ p2) ∧ h`
- **DNF:** `(j ∧ p1 ∧ h) ∨ (j ∧ p2 ∧ h)`

**CNF is better.** In DNF the conjunctions `j` and `h` are repeated, and evaluating the two disjuncts independently does redundant work (the join would be computed twice and then united). CNF also matches real queries, which contain more ANDs than ORs. Recall that ANDs map to joins or selections and ORs map to unions.

**(b)**
1. **Type incorrect.** `PNAME` is not an attribute of `EMPLOYEE` (it belongs to `PROJECT`).
2. **Type incorrect.** `PNAME` is a string and is compared with the number `25` (wrong type).
3. **Semantically incorrect.** Query graph:
   ```
   [EMPLOYEE] --(SSN = ESSN)-- [WORKS_ON]        [DEPARTMENT]
       |                         |                   |
     FNAME → RESULT          HOURS > 10        DNAME = 'HR'
   ```
   The graph is **not connected**. DEPARTMENT has no join condition and contributes nothing to the result, so it would cause a Cartesian product.
   **Correction:** add `AND E.DNO = D.DNUMBER`.

**(c)** Let `p = (SALARY > 3000)`, `q = (DNO = 5)`, `r = (SEX = 'F')`, `t = (TITLE = 'Engineer')`.
The WHERE clause is `(p ∧ p) ∨ (q ∧ ¬q) ∨ (r ∧ (r ∨ t))`.
1. `p ∧ p ≡ p` (idempotency)
2. `q ∧ ¬q ≡ false` (contradiction)
3. `r ∧ (r ∨ t) ≡ r` (absorption, `p1 ∧ (p1 ∨ p2) ≡ p1`)
4. `p ∨ false ∨ r ≡ p ∨ r` (`p ∨ false ≡ p`)

```sql
SELECT LNAME
FROM   EMPLOYEE
WHERE  SALARY > 3000 OR SEX = 'F';
```

---

## Part F – Heuristic Optimization (Exercise 7)

**(a) Initial canonical tree**
```
π E.LNAME, P.PNAME
        |
σ E.SSN=W.ESSN ∧ W.PNO=P.PNUMBER ∧ P.DNUM=D.DNUMBER
  ∧ D.DNAME='Research' ∧ E.SALARY>50000 ∧ W.HOURS>20
        |
        ×
      /   \
     ×     DEPARTMENT
    /  \
   ×    PROJECT
  /  \
EMPLOYEE  WORKS_ON
```

**(b) Step by step**
1. **Cascade of σ (rule 3, idempotency of unary operators):** split the conjunctive selection into six separate selections, `σc1(σc2(…(R)))`.
2. **Commute σ with × (rule 5):** push every single-relation selection down to its relation:
   `σ SALARY>50000 → EMPLOYEE`, `σ HOURS>20 → WORKS_ON`, `σ DNAME='Research' → DEPARTMENT`.
3. **σ followed by × becomes ⋈ (rule 7):** each join condition directly above a × turns that product into a join:
   `E ⋈ SSN=ESSN W`, `… ⋈ PNO=PNUMBER P`, `… ⋈ DNUM=DNUMBER D`. No Cartesian product remains.
4. **Order the joins by restrictiveness (commutativity and associativity, rules 1 and 2):** `σ DNAME='Research'(DEPARTMENT)` returns about **one** tuple, so join DEPARTMENT with PROJECT first, then with WORKS_ON, then with EMPLOYEE.
5. **Commute π with σ and ⋈ (rules 4 and 6):** push projections down, keeping only the attributes needed for later joins and for the final result.

**(c) Final optimized tree**
```
                          π LNAME, PNAME
                                |
                       ⋈  W.ESSN = E.SSN
                      /                  \
            π ESSN, PNAME               π SSN, LNAME
                  |                          |
         ⋈  P.PNUMBER = W.PNO          σ SALARY > 50000
          /                \                 |
   π PNUMBER, PNAME      π ESSN, PNO       EMPLOYEE
         |                    |
 ⋈ D.DNUMBER = P.DNUM     σ HOURS > 20
    /            \            |
π DNUMBER   π PNUMBER,     WORKS_ON
   |         PNAME, DNUM
σ DNAME =        |
'Research'    PROJECT
   |
DEPARTMENT
```

**(d)** `σ DNAME='Research'` selects essentially a single department (DNAME is practically unique), so the most restrictive join is `DEPARTMENT ⋈ PROJECT`. It produces only the projects of one department. Each later join therefore starts from a small intermediate result, which follows heuristic 3 (most restrictive operations first).

**(e)** The tree is **linear (left-deep)**: every join has a base relation, possibly after a selection or projection, as one of its operands. With `N = 4` relations, `O(N!) = 4! = 24` orderings.

---

## Part G – Full Case Study (Exercise 8)

Preliminary numbers:
- `T1 = σ status='SHIPPED'(ORDERS)`: 100,000 / 5 = 20,000 tuples, so `bT1 = 2000/5 = 400` blocks
- `T2 = σ city='Beirut'(CUSTOMER)`: 10,000 / 20 = 500 tuples, so `bT2 = 400/20 = 20` blocks

**(a) Plan 1, naive nested loop** (selections done on the fly):
- CUSTOMER outer: `bC + bC × bO = 400 + 400 × 2000 = ` **800,400**
- ORDERS outer: `bO + bO × bC = 2000 + 2000 × 400 = ` **802,000**

**(b) Plan 2, push selections, sort-merge join**
| Step | Computation | Cost |
|---|---|---:|
| c1: scan ORDERS + write T1 | 2000 + 400 | 2400 |
| c2: scan CUSTOMER + write T2 | 400 + 20 | 420 |
| c3: sort T1 (b=400, nB=5) | nR = 80, dM = 4, nP = ⌈log4 80⌉ = 4, so 2·400·(1+4) | 4000 |
| c4: sort T2 (b=20, nB=5) | nR = 4, dM = min(4,4) = 4, nP = 1, so 2·20·(1+1) | 80 |
| c5: merge-join T1, T2 | 400 + 20 | 420 |
| **Total** | | **7320** |

**(c) Plan 3, hash join on T1 and T2**
`c6 = 3 × (400 + 20) = 1260`, so `Total = 2400 + 420 + 1260 = ` **4080**.

**(d) Plan 4, block nested loop with T2 outer** (`nB − 2 = 3`)
`⌈20/3⌉ × 400 + 20 = 7 × 400 + 20 = 2820`, so `Total = 2400 + 420 + 2820 = ` **5640**.

**(e) Plan 5, index single-loop join** (primary index on CUSTOMER.cid, `x = 2`)
`c1 + bT1 + rT1 × (x + 1) = 2400 + 400 + 20,000 × 3 = ` **62,800**. T2 is not needed, because `city` is checked in memory.
This plan is bad because there are too many probes (20,000), and each probe costs 3 accesses.

**(f) Ranking**
| Rank | Plan | Cost |
|:---:|---|---:|
| 1 | **Plan 3: selections pushed + hash join** | **4080** |
| 2 | Plan 4: selections pushed + block NL | 5640 |
| 3 | Plan 2: selections pushed + sort-merge | 7320 |
| 4 | Plan 5: index single-loop | 62,800 |
| 5 | Plan 1: naive NL | 800,400 |

✅ **Choose Plan 3.** The example confirms the main heuristic: pushing selections below the join reduces the cost from about 800,000 to a few thousand block I/Os, roughly 200 times cheaper.

**(g)** cid is the key of CUSTOMER, so `js = 1/rC = 1/10,000`.
`|T1 ⋈ T2| = js × |T1| × |T2| = (1/10,000) × 20,000 × 500 = ` **1000** tuples.
As a check: 20,000 shipped orders, of which 1/20 belong to Beirut customers, gives 1000.
`bRES = 1000 / 100 = ` **10** blocks.

**(h) Challenge, pipelining into the hash join**
- Read ORDERS and CUSTOMER once and filter on the fly: `2000 + 400 = 2400`
- Partitioning phase, writing the partitions only (input is pipelined): `400 + 20 = 420`
- Probing phase, reading the partitions: `400 + 20 = 420`
- **Total ≈ 3240**, compared with 4080. The saving is **840** I/Os: T1 and T2 are no longer written and then re-read (`2 × 420`).

The hash join itself is still blocking. The probe phase cannot start before partitioning finishes, so its output cannot be fully pipelined upward.

---

## Formula Sheet (from the slides)

| Operation | Cost |
|---|---|
| S1 linear search | `b` (key equality: `b/2`) |
| S2 binary search | `log2 b + ⌈s/bfr⌉ − 1` (key: `log2 b`) |
| S3 primary index, one record | `x + 1` |
| S4 hash | `1` static, `2` extendible |
| S5 ordering index, range on key | `x + b/2` |
| S6 clustering index, equality | `x + ⌈s/bfr⌉` |
| S7-a secondary index, equality | `x + s` |
| S7-b secondary index, range | `x + bI1/2 + r/2` |
| Selectivity | key: `1/r`; non-key: `1/d`; `s = sl × r` |
| External sort | `nR = ⌈b/nB⌉`, `dM = min(nB−1, nR)`, `nP = ⌈log_dM nR⌉`, `Cost = 2b(1+nP)` |
| J1 nested loop | worst `bR·bS + bR + bRES`; best `bR + bS + bRES` |
| J1 improved | `⌈bR/(nB−2)⌉·bS + bR + bRES` |
| J2 single loop | `bR + rR·ci + bRES`; ci = `xB+sB` (secondary), `xB+⌈sB/bfrB⌉` (clustering), `xB+1` (primary), `h` (hash) |
| J3 sort-merge | `bR + bS + sort(R) + sort(S) + bRES` |
| J4 hash join | `3(bR + bS) + bRES` |
| Join result | `js = |R⋈S| / (|R|·|S|)`; `bRES = js·|R|·|S| / bfrRES` |

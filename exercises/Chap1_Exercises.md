# GIN400 / GIN540 – Advanced Database Systems
## Chapter 1: Physical Database Storage – Exercise Sheet

> Use the formulas from the course slides (Prof. J. Zalaket). Round **up** (⌈ ⌉) for numbers of blocks, levels, and accesses.
> Worked solutions are in [Chap1_Solutions.md](Chap1_Solutions.md). Try every question yourself before checking the solutions.

---

## Part A – Core Concepts

### Exercise 1 – Short Answers
1. Define a **disk block**, a **cylinder**, and a **sector**. How is a physical disk block addressed by the storage controller?
2. Name the three components of **disk access latency** for reading or writing a block. Which component typically takes the longest?
3. What is **double buffering**, and how does it reduce CPU-I/O bottleneck during file scans?
4. Define the **blocking factor ($bfr$)** for fixed-length records. What is the difference between **unspanned** and **spanned** record organization?
5. State the average number of disk block transfers to locate a record in:
   - (a) An unordered (heap) file of $b$ blocks.
   - (b) An ordered sequential file of $b$ blocks using binary search on the ordering key.
6. Distinguish between a **primary index**, a **clustering index**, and a **secondary index**. For each, indicate whether it is dense or sparse (non-dense).
7. Why does a **multi-level index** search require significantly fewer block accesses than a binary search on a single-level index?
8. Explain the fundamental structural differences between a **B-Tree** and a **B+-Tree**. Why do relational databases almost universally prefer B+-Trees?
9. In **extendable hashing**, what is the difference between **global depth ($d$)** and **local depth ($d'$)**? What condition causes the directory to double in size?
10. What types of attributes are suitable candidates for a **bitmap index**? Give two examples and describe how multi-condition queries are evaluated.

### Exercise 2 – True or False (Justify each answer in one line)
1. A primary index can be built on an unordered data file as long as the search key has unique values.
2. In an unspanned file organization, records can cross block boundaries, eliminating unused block space.
3. A clustering index requires the data file to be ordered on the indexing attribute, even though that attribute may have duplicate values.
4. In a B+-Tree with index fanout $fo = 100$, an index file with 10,000 first-level blocks can be searched in at most 3 block accesses.
5. In extendable hashing, every bucket split forces the directory to double in size.
6. A secondary index on a candidate key is always dense.
7. Bitmap indexes are efficient for high-cardinality attributes like Social Security Numbers (SSN).
8. Double buffering reduces the rotational latency of the magnetic disk.

---

## Part B – Numerical & Calculation Problems

### Exercise 3 – File Geometry & Blocking Factor
Consider a table `CUSTOMER` with the following physical parameters:
- Record size $R = 256$ bytes (fixed length).
- Total records $r = 120,000$.
- Disk block size $B = 4,096$ bytes.
- Block header size is negligible.

1. Calculate the **blocking factor** $bfr$ for unspanned organization.
2. Determine the total number of disk blocks $b$ required to store the table.
3. Calculate the unused (wasted) space per block due to internal fragmentation.
4. If spanned organization were used instead, calculate the minimum number of blocks $b_{spanned}$ needed.

---

### Exercise 4 – Single-Level Primary Index vs. Binary Search
Consider the `CUSTOMER` file from Exercise 3 physically ordered on the primary key `CustomerID`.
We construct a **Primary Index** on `CustomerID`:
- Search key field size $V = 16$ bytes.
- Block pointer size $P = 6$ bytes.
- Disk block size $B = 4,096$ bytes.

1. Calculate the index record size $R_I$ and the index blocking factor $bfr_I$.
2. Determine the total number of index entries $r_I$ and index blocks $b_I$.
3. Compute the number of block accesses required to find a customer record:
   - (a) Using linear search on the data file.
   - (b) Using binary search directly on the ordered data file.
   - (c) Using the primary index (binary search on index blocks + data block fetch).

---

### Exercise 5 – Secondary Index with Indirection
Consider an unordered data file with:
- $r = 50,000$ records, $b = 5,000$ disk blocks.
- We build a **Secondary Index** on a non-ordering, non-key attribute `CITY`:
  - Number of distinct city values $d = 200$.
  - Record pointer size $P_R = 6$ bytes, key size $V = 20$ bytes.
  - Block pointer size $P_B = 6$ bytes, block size $B = 4,096$ bytes.
  - Implemented using **one level of indirection** so index entries are fixed length $\langle \text{CITY}, P_B \rangle$, where $P_B$ points to a block of record pointers.

1. Calculate the number of first-level index blocks $b_I$.
2. Calculate the total number of indirection blocks required to hold all 50,000 record pointers ($bfr_{ind} = \lfloor B / P_R \rfloor$).
3. On average, how many records exist per city? How many indirection blocks must be read per city?
4. Calculate the total cost to retrieve all customers residing in a given city using this secondary index compared to a full file scan.

---

### Exercise 6 – Multi-Level B+-Tree Calculation
Suppose a database table has $r = 1,000,000$ records stored in $b = 50,000$ data blocks.
We construct a multi-level B+-Tree index on the primary key:
- Block size $B = 4,096$ bytes.
- Key field size $V = 12$ bytes, record pointer $P = 6$ bytes, block pointer $P_B = 6$ bytes.
- For internal nodes, each entry is $\langle P_B, K, P_B \rangle$. The fanout $fo = \lfloor B / (V + P_B) \rfloor$.
- For leaf nodes, each entry is $\langle K, P \rangle$, with one sibling pointer $P_B$.

1. Calculate the fanout $fo$ of the internal nodes.
2. Calculate the number of leaf blocks needed if leaf entries are filled at 100% capacity.
3. Calculate the number of tree levels (height $x$).
4. How many block accesses are required to retrieve an arbitrary record using this B+-Tree?
5. How many block accesses are required to retrieve all records with keys in the range $[K_1, K_2]$ that span 25 consecutive leaf blocks?

---

### Exercise 7 – Extendable Hashing Step-by-Step
Assume disk buckets have capacity $C = 2$ records.
A dynamic hash function produces 4-bit binary values for keys:
- $h(A) = 0100_2$
- $h(B) = 1000_2$
- $h(C) = 1100_2$
- $h(D) = 0010_2$
- $h(E) = 0100_2$
- $h(F) = 1101_2$

Extendable hashing uses the **last $d$ bits** (suffix) of the hash value.
Initially, global depth $d = 1$, and local depth $d' = 1$ for all buckets.

1. Show the initial directory state and bucket assignments after inserting $A$ and $B$.
2. Insert key $C$ ($h(C) = 1100_2$). Explain whether a bucket split or directory doubling occurs.
3. Insert key $D$ and then key $E$. Trace the directory doubling and local depth updates step by step.
4. Draw the final directory and bucket state, specifying the global depth and local depth of each bucket.

---

### Exercise 8 – Bitmap Index Query Evaluation
Consider a database of $r = 8$ employees (IDs 0 to 7):
- Attribute `GENDER`: `M` or `F`.
- Attribute `RATING`: `HIGH`, `MEDIUM`, or `LOW`.

The bitmap vectors are:
- `M`: `1 1 0 1 0 0 1 0`
- `F`: `0 0 1 0 1 1 0 1`
- `HIGH`: `0 1 0 0 0 1 1 0`
- `MEDIUM`: `1 0 1 0 1 0 0 0`
- `LOW`: `0 0 0 1 0 0 0 1`

1. Evaluate the query: `SELECT * FROM EMPLOYEE WHERE GENDER = 'M' AND RATING = 'HIGH'`. Show the bitwise boolean operation and identify the matching employee IDs.
2. Evaluate: `SELECT * FROM EMPLOYEE WHERE (GENDER = 'F' OR RATING = 'MEDIUM') AND NOT (RATING = 'LOW')`.
3. How does the database engine evaluate `SELECT COUNT(*) FROM EMPLOYEE WHERE GENDER = 'F' AND RATING = 'HIGH'` without retrieving employee data records?

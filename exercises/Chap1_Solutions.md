# GIN400 / GIN540 – Advanced Database Systems
## Chapter 1: Physical Database Storage – Worked Solutions

> Based on course notes by Prof. J. Zalaket.
> Standard notation: $r$ = number of records, $R$ = record size, $B$ = block size, $bfr = \lfloor B/R \rfloor$, $b = \lceil r/bfr \rceil$, $fo = bfr_I$.

---

## Part A – Core Concepts

### Exercise 1 – Short Answers
1. **Definitions & Physical Address:**
   - **Disk Block (Page):** The smallest unit of physical data transfer between disk storage and main memory (typically 512 B to 8 KB).
   - **Track & Sector:** A magnetic platter surface is divided into concentric rings called **tracks**. Each track is divided into fixed-size arcs called **sectors**.
   - **Cylinder:** The collection of all tracks at the exact same radial arm position across all recording surfaces of the disk pack.
   - **Address Format:** The storage controller addresses a physical block via the 3-tuple:  
     $$\text{Address} = \langle \text{Surface Number}, \text{Track/Cylinder Number}, \text{Sector Number} \rangle$$

2. **Components of Disk Access Latency:**
   - **Seek Time ($s$):** Mechanical movement of the read/write head assembly to position over the desired cylinder/track. (Typically takes the longest: 3–10 ms).
   - **Rotational Latency ($rd$):** Time waiting for the target sector to rotate underneath the head. On average, half a revolution: $rd = \frac{1}{2 \times \text{RPM}}$ (e.g. $\sim 2.8$ ms at 10,800 RPM).
   - **Transfer Time ($tr$):** Time required to physically read/write the bits of the block: $tr = \frac{\text{Block Size}}{\text{Transfer Rate}}$.
   - **Dominant Component:** **Seek time** is mechanically the slowest and dominates latency.

3. **Double Buffering:**
   - A technique that allocates **two memory buffer pages** (Buffer A and Buffer B).
   - While the CPU is executing operations on the tuples in Buffer A, the disk controller concurrently reads the next sequential disk block into Buffer B via Direct Memory Access (DMA).
   - Once Buffer A is processed, the roles flip without the CPU waiting idle for I/O, effectively overlapping CPU computation and disk transfer.

4. **Blocking Factor & Spanned vs. Unspanned:**
   - **Blocking Factor ($bfr$):** The maximum number of whole records that can fit into a single disk block: $bfr = \lfloor B / R \rfloor$.
   - **Unspanned Organization:** Each record is contained entirely within a single block. If a record cannot fit into the remaining block space, the space is left unused (**internal fragmentation**).
   - **Spanned Organization:** Records can cross block boundaries; the portion that cannot fit in block $i$ is stored at the start of block $i+1$, linked by a pointer. Eliminates wasted space at the cost of multiple block reads for spanned records.

5. **Average Search Costs:**
   - (a) Unordered (Heap) file: Linear scan average cost $= \lceil b / 2 \rceil$ block transfers (or $b$ if record not found).
   - (b) Ordered sequential file: Binary search cost $= \lceil \log_2 b \rceil$ block transfers.

6. **Index Types Comparison:**
   - **Primary Index:** Defined on an **ordered data file** on a **key attribute** (unique). It is **sparse (non-dense)**: exactly 1 index entry per data block containing the anchor key and block pointer.
   - **Clustering Index:** Defined on an **ordered data file** on a **non-key attribute** (duplicate values allowed). It is **sparse (non-dense)**: exactly 1 index entry per distinct search value pointing to the first block containing that value.
   - **Secondary Index:** Defined on a **non-ordering attribute**. It is **dense** when defined on a candidate key (1 entry per record). For non-key attributes, it uses an indirection pointer list.

7. **Multi-Level Index Efficiency:**
   - Binary search on a single-level index reduces the search range by a factor of **2** per block access ($\log_2 b_I$).
   - A multi-level index organizes index blocks hierarchically where each higher level has a fanout $fo = bfr_I$ (typically $fo = 100 \text{ to } 500$). Each step reduces the search range by a factor of **$fo$** instead of 2. Hence, tree height is $\lceil \log_{fo} b_{I1} \rceil + 1$, reducing search cost to just 3–4 block accesses even for billions of records.

8. **B-Tree vs. B+-Tree:**
   - **B-Tree:** Record pointers $\langle K, P_{\text{record}} \rangle$ exist in **all nodes** (both internal nodes and leaf nodes).
   - **B+-Tree:** All record pointers exist **exclusively in the leaf nodes**. Internal nodes store only router search keys and tree node pointers $\langle P_{\text{block}}, K, P_{\text{block}} \rangle$. Leaf nodes are connected as a doubly linked list.
   - **Why B+-Trees are preferred:**
     1. Internal nodes store no data pointers, resulting in **much higher fanout ($fo$)**, leading to a shallower tree with fewer disk accesses.
     2. Sequential range scans can be answered simply by traversing the linked leaf nodes without revisiting internal tree levels.

9. **Extendable Hashing:**
   - **Global Depth ($d$):** Number of hash bits used to index the directory ($2^d$ directory entries).
   - **Local Depth ($d'$):** Number of hash bits shared by records stored in a specific bucket.
   - **Directory Doubling Condition:** When a bucket overflows upon insertion and its local depth **equals** the global depth ($d' = d$), the directory must double ($d \leftarrow d + 1$). If $d' < d$, the bucket simply splits without doubling the directory.

10. **Bitmap Indexes:**
    - Well suited for attributes with **low cardinality** (few distinct values) across large relations, e.g. `Gender` (`M`, `F`), `State` (50 values), `MaritalStatus`.
    - Multi-attribute queries are answered via fast hardware bitwise operators:
      - `AND` for conjunctions
      - `OR` for disjunctions
      - `NOT` for negation
      - Population count (`POPCNT`) instructions for `COUNT(*)` aggregates without loading table rows from disk.

---

### Exercise 2 – True or False
1. **False.** A primary index strictly requires the data file to be **physically ordered** on the search key.
2. **False.** Spanned organization allows records to cross block boundaries; unspanned forbids it.
3. **True.** A clustering index requires the file to be ordered on the non-key indexing attribute.
4. **True.** Tree height is $\lceil \log_{100}(10000) \rceil + 1 = 2 + 1 = 3$ block accesses to reach the leaf.
5. **False.** If the overflowed bucket has local depth $d' < d$, the bucket splits without doubling the directory.
6. **True.** Because candidate keys are unique in every record, every record must have an entry in the secondary index (dense).
7. **False.** High cardinality attributes result in massive bitmaps that are mostly zeros (sparse) with high storage overhead.
8. **False.** Double buffering reduces CPU wait time, not the physical rotational speed of the disk platter.

---

## Part B – Numerical & Calculation Problems

### Exercise 3 – File Geometry & Blocking Factor
**Given:** $R = 256$ bytes, $r = 120,000$, $B = 4,096$ bytes.

1. **Blocking factor ($bfr$):**
   $$bfr = \left\lfloor \frac{B}{R} \right\rfloor = \left\lfloor \frac{4096}{256} \right\rfloor = 16 \text{ records/block}$$

2. **Total disk blocks ($b$):**
   $$b = \left\lceil \frac{r}{bfr} \right\rceil = \left\lceil \frac{120,000}{16} \right\rceil = 7,500 \text{ blocks}$$

3. **Unused space per block:**
   $$\text{Used space} = 16 \times 256 = 4,096 \text{ bytes}$$
   $$\text{Wasted space} = 4,096 - 4,096 = 0 \text{ bytes}$$
   *(Note: Since 256 divides 4096 exactly, there is zero internal fragmentation in this specific case).*

4. **Spanned organization:**
   $$\text{Total raw bytes} = 120,000 \times 256 = 30,720,000 \text{ bytes}$$
   $$b_{spanned} = \left\lceil \frac{30,720,000}{4096} \right\rceil = 7,500 \text{ blocks}$$

---

### Exercise 4 – Single-Level Primary Index vs. Binary Search
**Given:** $b = 7,500$ blocks, $V = 16$ bytes, $P = 6$ bytes, $B = 4,096$ bytes.

1. **Index entry size and blocking factor:**
   $$R_I = V + P = 16 + 6 = 22 \text{ bytes}$$
   $$bfr_I = \left\lfloor \frac{B}{R_I} \right\rfloor = \left\lfloor \frac{4096}{22} \right\rfloor = 186 \text{ index entries/block}$$

2. **Index entries and index blocks ($b_I$):**
   For a Primary Index, there is 1 index entry per data block:
   $$r_I = b = 7,500 \text{ entries}$$
   $$b_I = \left\lceil \frac{r_I}{bfr_I} \right\rceil = \left\lceil \frac{7500}{186} \right\rceil = 41 \text{ index blocks}$$

3. **Access Cost Comparison:**
   - (a) Linear search on data file:
     $$\text{Cost} = \left\lceil \frac{b}{2} \right\rceil = \left\lceil \frac{7500}{2} \right\rceil = 3,750 \text{ block accesses}$$
   - (b) Binary search directly on data file:
     $$\text{Cost} = \lceil \log_2 b \rceil = \lceil \log_2 7500 \rceil = \lceil 12.87 \rceil = 13 \text{ block accesses}$$
   - (c) Primary Index:
     $$\text{Cost} = \lceil \log_2 b_I \rceil + 1 = \lceil \log_2 41 \rceil + 1 = 6 + 1 = 7 \text{ block accesses}$$
   *(The primary index cuts binary search I/O nearly in half!)*

---

### Exercise 5 – Secondary Index with Indirection
**Given:** $r = 50,000$, $b = 5,000$, $d = 200$ distinct cities, $V = 20$ B, $P_B = 6$ B, $P_R = 6$ B, $B = 4,096$ B.

1. **First-level index blocks ($b_I$):**
   - Each entry in the first-level index is $\langle \text{CITY}, P_B \rangle \implies R_I = 20 + 6 = 26$ bytes.
   - $bfr_I = \lfloor 4096 / 26 \rfloor = 157$ entries/block.
   - Total index entries $= d = 200$.
   $$b_I = \left\lceil \frac{200}{157} \right\rceil = 2 \text{ blocks}$$

2. **Total indirection blocks:**
   - Number of record pointers stored $= r = 50,000$.
   - Indirection blocking factor $bfr_{ind} = \lfloor 4096 / 6 \rfloor = 682$ pointers/block.
   $$b_{ind} = \left\lceil \frac{50,000}{682} \right\rceil = 74 \text{ blocks}$$

3. **Records and indirection blocks per city:**
   - Average records per city:
     $$\bar{s} = \frac{r}{d} = \frac{50,000}{200} = 250 \text{ records/city}$$
   - Indirection blocks per city:
     $$\left\lceil \frac{250}{bfr_{ind}} \right\rceil = \left\lceil \frac{250}{682} \right\rceil = 1 \text{ indirection block}$$

4. **Total Retrieval Cost:**
   - Search first-level index: $\lceil \log_2 b_I \rceil = \lceil \log_2 2 \rceil = 1$ access.
   - Fetch indirection block: 1 access.
   - Fetch data records: each of the 250 records resides on an unclustered data block: 250 accesses.
   $$\text{Total Index Cost} = 1 + 1 + 250 = 252 \text{ block accesses}$$
   - Full table scan cost: $b = 5,000$ block accesses.
   *(Using the secondary index is $\sim 20\times$ faster than a full scan).*

---

### Exercise 6 – Multi-Level B+-Tree Calculation
**Given:** $r = 1,000,000$, $b = 50,000$, $B = 4,096$ B, $V = 12$ B, $P = 6$ B, $P_B = 6$ B.

1. **Fanout ($fo$):**
   Internal node entry: $\langle P_B, K, P_B \rangle \implies \text{Size} = V + P_B = 12 + 6 = 18$ B.
   $$fo = \left\lfloor \frac{B}{V + P_B} \right\rfloor = \left\lfloor \frac{4096}{18} \right\rfloor = 227$$

2. **Leaf blocks:**
   Leaf node entry: $\langle K, P \rangle \implies \text{Size} = 12 + 6 = 18$ B.
   $$bfr_{leaf} = \left\lfloor \frac{4096 - 6}{18} \right\rfloor = 227 \text{ entries/block}$$
   $$b_1 = \left\lceil \frac{r}{bfr_{leaf}} \right\rceil = \left\lceil \frac{1,000,000}{227} \right\rceil = 4,406 \text{ leaf blocks}$$

3. **Tree Height ($x$):**
   - Level 1 (Leaves): $4,406$ blocks.
   - Level 2: $\lceil 4,406 / 227 \rceil = 20$ blocks.
   - Level 3: $\lceil 20 / 227 \rceil = 1$ block (Root node).
   $$\text{Total Levels } x = 3$$

4. **Point Lookup Cost:**
   $$\text{Cost} = x + 1 = 3 \text{ (tree blocks)} + 1 \text{ (data block)} = 4 \text{ block accesses}$$

5. **Range Scan Cost (25 consecutive leaf blocks):**
   - Traverse from root to first leaf block: 3 block accesses.
   - Follow leaf sibling pointers across remaining 24 leaf blocks: 24 block accesses.
   - Total index accesses $= 3 + 24 = 27$ accesses.

---

### Exercise 7 – Extendable Hashing Step-by-Step
**Bucket Capacity $C = 2$. Suffix hashing with depth $d$.**

1. **Initial state ($d = 1, d' = 1$):**
   - Directory entries: `0` $\to$ Bucket 0, `1` $\to$ Bucket 1.
   - Insert $A$ ($010\mathbf{0}_2$): Suffix bit is `0` $\implies$ Bucket 0 contains $\{A\}$.
   - Insert $B$ ($100\mathbf{0}_2$): Suffix bit is `0` $\implies$ Bucket 0 contains $\{A, B\}$ (Full).

2. **Insert $C$ ($110\mathbf{0}_2$):**
   - Suffix is `0`, but Bucket 0 is full ($\{A, B\}$).
   - Check depths: $d' = 1$ and $d = 1 \implies d' = d$.
   - **Action:** **Directory Doubles!** Global depth becomes $d = 2$.
   - New directory size $= 2^2 = 4$ entries: `00`, `01`, `10`, `11`.
   - Overflowed bucket splits into:
     - Bucket 00 ($d'=2$): records with suffix `00` $\implies \{A(0100), B(1000), C(1100)\}$.
       *(Still overflows! Splits again to $d=3$ if needed, but here $A, B, C$ all share suffix $00$. Since $A=0100, B=1000, C=1100$, checking 3rd bit: $A$ is $100$, $B$ is $000$, $C$ is $100$. Split on 3 bits: Bucket 000 has $\{B\}$, Bucket 100 has $\{A, C\}$).*

3. **State after Inserting $D$ ($00\mathbf{10}_2$):**
   - Suffix bit is `10`. Points to Bucket 10. Contains $\{D\}$.
   - No overflow.

4. **Insert $E$ and $F$:**
   - Keys route directly to their binary suffix buckets. Directory doubles only when the target bucket's local depth equals global depth.

---

### Exercise 8 – Bitmap Index Query Evaluation
**Bitmaps:**
- `M`: `1 1 0 1 0 0 1 0`
- `F`: `0 0 1 0 1 1 0 1`
- `HIGH`: `0 1 0 0 0 1 1 0`
- `MEDIUM`: `1 0 1 0 1 0 0 0`
- `LOW`: `0 0 0 1 0 0 0 1`

1. **Query 1: `GENDER = 'M' AND RATING = 'HIGH'`:**
   $$\text{Bitwise AND: } (1 1 0 1 0 0 1 0) \text{ AND } (0 1 0 0 0 1 1 0) = 0 1 0 0 0 0 1 0$$
   - Result bit vector: `0 1 0 0 0 0 1 0`.
   - Matching employee IDs: **ID 1** and **ID 6**.

2. **Query 2: `(GENDER = 'F' OR RATING = 'MEDIUM') AND NOT (RATING = 'LOW')`:**
   - Step 1: `F OR MEDIUM`:
     $$(0 0 1 0 1 1 0 1) \text{ OR } (1 0 1 0 1 0 0 0) = 1 0 1 0 1 1 0 1$$
   - Step 2: `NOT LOW`:
     $$\text{NOT }(0 0 0 1 0 0 0 1) = 1 1 1 0 1 1 1 0$$
   - Step 3: Conjunction:
     $$(1 0 1 0 1 1 0 1) \text{ AND } (1 1 1 0 1 1 1 0) = 1 0 1 0 1 1 0 0$$
   - Matching employee IDs: **ID 0, ID 2, ID 4, ID 5**.

3. **Query 3: `SELECT COUNT(*) FROM EMPLOYEE WHERE GENDER = 'F' AND RATING = 'HIGH'`:**
   - Evaluate `F AND HIGH`:
     $$(0 0 1 0 1 1 0 1) \text{ AND } (0 1 0 0 0 1 1 0) = 0 0 0 0 0 1 0 0$$
   - The CPU executes hardware population count `POPCNT` on the bit vector, which returns **1**.
   - **Zero data blocks** are retrieved from disk!

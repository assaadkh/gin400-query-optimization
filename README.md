# ⚡ Advanced Database Systems Masterclass Portal (GIN400 / GIN540)

An interactive, high-definition animated masterclass portal for **Advanced Database Systems** (Prof. Joseph Zalaket), featuring neural AI studio narration, real-time $\KaTeX$ formulas, 60fps dynamic canvas visualizations, word-by-word draggable karaoke subtitles, interactive cost sandboxes, and exam problem sheets with step-by-step worked mathematical proofs.

---

## 🌐 Live Hosted Web Portal (GitHub Pages)
👉 **Launch the master course portal online for free:**  
### **[https://assaadkh.github.io/gin400-query-optimization/](https://assaadkh.github.io/gin400-query-optimization/)**

*Works on all modern desktop and mobile browsers with zero setup or backend installation required.*

---

## 🏛️ Course Structure & Chapters

### 💾 [Chapter 1: Physical Database Storage & Indexing](chapter1.html)
- **Live Player:** [`chapter1.html`](chapter1.html)
- **Slides PDF:** [`GIN-ADB-Chap1.pdf`](GIN-ADB-Chap1.pdf)
- **Problem Sheet:** [`exercises/Chap1_Exercises.md`](exercises/Chap1_Exercises.md)
- **Step-by-Step Worked Solutions:** [`exercises/Chap1_Solutions.md`](exercises/Chap1_Solutions.md)
- **Curriculum:**
  1. **Physical Storage Hierarchy & Disk Geometry**: Platters, cylinders, tracks, sectors, address $(\text{Surface}, \text{Track}, \text{Sector})$, seek/rotational/transfer latency $T = s + \frac{r}{2} + \frac{b}{t}$, double buffering, and RAID striping.
  2. **Record Organization, Blocking Factor & Spanning**: $bfr = \lfloor B/R \rfloor$, blocks $b = \lceil r/bfr \rceil$, unspanned internal fragmentation $B \pmod R$ vs spanned continuation pointers, heap ($b/2$) vs binary scan ($\lceil \log_2 b \rceil$).
  3. **Single-Level Indexes (Primary, Clustering, Secondary)**: Primary index (anchor key, sparse, $\lceil \log_2 b_I \rceil + 1$), Clustering index (ordering non-key, distinct values $d$), Secondary index (candidate key dense vs indirection pointer buckets).
  4. **Multi-Level Balanced Indexing & B+ Trees**: Fanout $fo = bfr_I$, height $x = \lceil \log_{fo}(b_{i1}) \rceil + 1$, B-Tree vs B+-Tree (pushing data pointers exclusively to leaves, doubly linked leaf chain for range scans).
  5. **Static vs Dynamic Extendable Hashing**: Static collision overflow chains vs Extendable Hashing (directory size $2^d$, global depth $d$, local depth $d'$, bucket splits vs directory doubling when $d'=d$).
  6. **Bitmap Indexing & Multi-Attribute Bitwise Engine**: Low-cardinality vectors, in-register bitwise `AND`, `OR`, `NOT`, and `POPCNT` counting without disk block reads.

---

### ⚡ [Chapter 2: Query Processing & Optimization](chapter2.html)
- **Live Player:** [`chapter2.html`](chapter2.html)
- **Slides PDF:** [`GIN-ADB-Chap2.pdf`](GIN-ADB-Chap2.pdf)
- **Problem Sheet:** [`exercises/Chap2_Exercises.md`](exercises/Chap2_Exercises.md)
- **Step-by-Step Worked Solutions:** [`exercises/Chap2_Solutions.md`](exercises/Chap2_Solutions.md)
- **Standalone Broadcast MP4:** [`query_optimization_masterclass.mp4`](query_optimization_masterclass.mp4) (H.264 / AAC 192k 720p HD, 5m 20s)
- **Curriculum:**
  1. **Query Processing Architecture**: Declarative SQL $\to$ Relational Algebra $\to$ Physical Operator Tree $\to$ Execution Engine.
  2. **Catalog Statistics & Selectivity**: $r, R, b, bfr, V(A, R)$, selectivity $sl$, linear scan vs binary search.
  3. **Index Selection Algorithms (A1–A6)**: Primary key equality ($HT+1$), clustering range scan, secondary index equality and range costs.
  4. **Join Algorithms (Nested-Loop & Hash)**: Simple nested-loop, block nested-loop with $B$ buffers, Grace/partition hash join.
  5. **Sort-Merge Join Deep Dive**: External sort-merge phases, buffer allocation, $3(b_R + b_S)$ cost.
  6. **Relational Algebra Equivalences**: Selection/projection pushdown, join commutativity and associativity.
  7. **Cost Estimation & Plan Search Space**: Left-deep trees, Dynamic Programming $\mathcal{O}(3^n)$, Catalan combinatorial explosion.
  8. **Mathematical Reference & Proofs**: Complete proofs for selection algorithms, blocking factors, and joins.
  9. **Exam Checklist & Mastery Matrix**: Algorithm decision flowchart and exam review checklist.

---

## ✨ Interactive Features
1. **Studio Copilot Narration**: Mastered neural audio (`en-US-AndrewMultilingualNeural`) embedded directly as base64 data URIs for 100% offline static CDN playback.
2. **Synchronized 60fps Visual Spotlights**: Elements on the diagrams glow and pulse in real time as the narration explains them.
3. **Word-by-Word Karaoke Subtitles**: Frame-accurate word highlighting with freely draggable on-screen CC box.
4. **Interactive Formula HUD & Sandboxes**:
   - Chapter 1: Disk Latency & Transfer Calculator, Blocking Factor & B+ Tree Height Calculator, Extendable Hashing Simulator.
   - Chapter 2: External Sort-Merge Simulator and Join Algorithms Showdown.
5. **1-Click Native MP4 Video Export**: Directly records and saves broadcast MP4/WebM videos from within the browser via MediaRecorder API.

---

## 📁 Repository Structure
```
gin400-query-optimization/
├── index.html                           # Master Course Portal (Landing Page)
├── chapter1.html                        # Chapter 1 Standalone Interactive Player (3.3 MB)
├── chapter2.html                        # Chapter 2 Standalone Interactive Player (7.3 MB)
├── query_optimization_video.html        # Original Chapter 2 Player
├── query_optimization_masterclass.mp4   # Broadcast 720p Standalone MP4
├── GIN-ADB-Chap1.pdf                    # Chapter 1 Course Slides
├── GIN-ADB-Chap2.pdf                    # Chapter 2 Course Slides
├── exercises/
│   ├── Chap1_Exercises.md               # Chapter 1 Exam Problems
│   ├── Chap1_Solutions.md               # Chapter 1 Mathematical Step-by-Step Proofs
│   ├── Chap2_Exercises.md               # Chapter 2 Exam Problems
│   └── Chap2_Solutions.md               # Chapter 2 Mathematical Step-by-Step Proofs
├── audio/                               # Generated Raw MP3 Audio Tracks
├── build_chapter1_data.py               # Edge-TTS Audio & Karaoke Alignment Generator
├── build_chapter1_html.py               # Chapter 1 Standalone Player Builder
└── README.md
```

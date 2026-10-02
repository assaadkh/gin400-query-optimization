# ⚡ Query Optimization Interactive Masterclass & Video (GIN400 / GIN540)

An interactive, animated masterclass on **Database Query Optimization** (Chapter 2: Query Processing & Optimization) with AI studio narration, real-time $\KaTeX$ formulas, synchronized voice spotlighting, draggable word-by-word karaoke subtitles, and standalone 1080p/720p broadcast MP4 export.

---

## 🌐 Live Hosted Web Player
👉 **Access the interactive masterclass online:**
**[https://assaadkh.github.io/gin400-query-optimization/](https://assaadkh.github.io/gin400-query-optimization/)**

*Works on all modern desktop and mobile browsers with zero installation required.*

---

## 🎬 Standalone MP4 Download
- **Full Video:** [`query_optimization_masterclass.mp4`](query_optimization_masterclass.mp4)
- **Duration:** 5 minutes 20 seconds
- **Format:** H.264 / AAC 192k (1280×720 HD)
- **Features:** Studio Copilot narration, baked-in karaoke subtitles, dynamic voice spotlighting, and active $\KaTeX$ cost formulas.

---

## 📚 Course Curriculum & Scenes

| Scene | Topic | Key Concepts | Cost Model / Formula |
|:---:|:---|:---|:---|
| **1** | **Query Processing Architecture** | Declarative SQL $\to$ Relational Algebra $\to$ Physical Plan $\to$ Engine | $\mathcal{O}(\text{Cost}) = \text{Est(Disk I/O)} + \text{Est(CPU)}$ |
| **2** | **Catalog Statistics & Selectivity** | $r$, $b$, $bfr$, $V(A, R)$, Selectivity $sl$, Linear vs Binary Search | $sl = \frac{1}{V(A,R)}$, $\text{Cost}(A_1) = \lceil b/2 \rceil$, $\text{Cost}(A_2) = b$ |
| **3** | **Index Selection Algorithms** | Primary Key ($A_3$), Primary Non-Key ($A_4$), Secondary ($A_5, A_6$) | $A_3 = HT + 1$, $A_4 = HT + b$, $A_5 = HT + 1$ |
| **4** | **Join Algorithms: Nested-Loop & Hash** | Simple Nested-Loop, Block Nested-Loop with $B$ buffers, Hash Join | $b_R + b_R \cdot b_S$ vs $b_R + \lceil \frac{b_R}{B-2} \rceil \cdot b_S$ |
| **5** | **Sort-Merge Join Deep Dive** | Sort Phase + Merge Scan Phase, Memory buffer constraints | $\text{Cost} = 3(b_R + b_S)$ |
| **6** | **Relational Algebra Equivalences** | Commutativity, Associativity, Heuristic Selection/Projection Pushdown | $\sigma_\theta(R \bowtie S) \equiv (\sigma_\theta(R)) \bowtie S$ |
| **7** | **Cost Estimation & Plan Search Space** | Left-deep trees, Dynamic Programming, Catalan combinatorial explosion | $N = \frac{(2n)!}{n!}$, DP complexity $\mathcal{O}(3^n)$ |
| **8** | **Mathematical Reference & Proofs** | Rigorous proofs for $A_1 \to A_6$, blocking factors, and joins | $b = \lceil r / bfr \rceil$, $V(A, R) = |\pi_A(R)|$ |
| **9** | **Exam Checklist & Mastery Matrix** | Core exam takeaway matrix and algorithm decision flowchart | Complete exam review checklist |

---

## ✨ Features
1. **Studio Copilot Narration**: Mastered neural voice (`en-US-AndrewMultilingualNeural`, 128 kbps 44.1 kHz).
2. **Synchronized Visual Spotlights**: Elements on the diagrams glow and pulse in real time as the narration explains them.
3. **Word-by-Word Karaoke Subtitles**: Frame-accurate word highlighting with freely draggable on-screen CC box.
4. **Interactive Formula HUD & Sandbox**: Live $\KaTeX$ typesetting with interactive Sort-Merge parameter sandbox.
5. **1-Click Native MP4 Video Export**: Directly records and saves broadcast MP4 video from within the browser.

---

## 🛠️ Offline Build Script
To re-render the standalone `.mp4` video from scratch:
```bash
python build_mp4_video.py
```
*Requires Google Chrome and FFmpeg.*

import asyncio
import edge_tts
import json
import base64
import os
import re

work_dir = r'c:\Users\user\Desktop\Uni\gin400'
audio_dir = os.path.join(work_dir, 'audio')
os.makedirs(audio_dir, exist_ok=True)

VOICE = 'en-US-AndrewMultilingualNeural'

SCENES = [
    {
        "id": 0,
        "title": "1. Physical Storage Hierarchy & Disk Geometry",
        "hudCost": "\\text{Address} = (\\text{Surface}, \\text{Track}, \\text{Sector})",
        "text": (
            "Welcome to Chapter 1 on Physical Database Storage. "
            "Relational database engines store massive volumes of data on non-volatile secondary storage, primarily magnetic disks and solid state drives. "
            "A magnetic disk pack consists of multiple rotating platters coated with magnetic material, organized into concentric circles called tracks, and subdivided into fixed-size arcs called sectors. "
            "All tracks at the same radius across all recording surfaces form a cylinder. "
            "To access any physical disk block, the storage engine specifies a three-part address: surface number, track number, and sector number. "
            "The total read or write latency is dominated by mechanical delay: seek time to position the read-write head onto the cylinder, rotational latency waiting for the target sector to rotate underneath the head, and transfer time to read the bits. "
            "To reduce I/O bottlenecks, modern database management systems employ double buffering, keeping two memory buffers active so the CPU processes one block while the disk controller concurrently fetches the next, alongside RAID disk striping across multiple arms."
        )
    },
    {
        "id": 1,
        "title": "2. Record Organization, Blocking Factor & Spanning",
        "hudCost": "bfr = \\lfloor B / R \\rfloor \\mid b = \\lceil r / bfr \\rceil",
        "text": (
            "A database table consists of records stored inside disk blocks of fixed size B. "
            "For fixed-length records of size R bytes, the blocking factor bfr is the floor of block size B divided by record size R. "
            "The total number of disk blocks b needed to store r records equals the ceiling of r divided by bfr. "
            "When records do not fit evenly into a block, systems face a design choice between unspanned and spanned organization. "
            "In unspanned organization, each record is contained entirely within a single block, leaving unused leftover bytes as internal fragmentation. "
            "In spanned organization, records that exceed remaining block capacity cross block boundaries into the next block using continuation pointers, eliminating wasted space at the cost of multiple block I/O operations. "
            "Searching an unordered heap file requires an average of b over 2 block transfers, while an ordered sequential file enables binary search in ceiling of log base 2 of b block accesses."
        )
    },
    {
        "id": 2,
        "title": "3. Single-Level Indexes: Primary, Clustering, & Secondary",
        "hudCost": "b_I = \\lceil b / bfr_I \\rceil \\mid \\text{Cost} = \\lceil \\log_2(b_I) \\rceil + 1",
        "text": (
            "To avoid scanning every disk block, database systems build index access paths. "
            "A primary index is created on an ordered file using a unique primary key field. "
            "It is a non-dense, sparse index containing one entry per data block, storing the block anchor key and a block pointer. "
            "Because there are only b index entries, searching costs ceiling of log base 2 of index blocks b sub I, plus one data block access. "
            "A clustering index is defined on an ordered file ordered by a non-key field. "
            "It is also non-dense, storing one entry for each of the d distinct values pointing to the first data block containing that value. "
            "In contrast, a secondary index provides an alternate access path on a non-ordering field. "
            "For candidate keys, it is dense, containing an entry for every single record r. "
            "For non-key attributes with duplicate values, secondary indexes employ a level of indirection, pointing to an intermediate bucket of record pointers, keeping index entries fixed-length."
        )
    },
    {
        "id": 3,
        "title": "4. Multi-Level Indexing & B+ Tree Architecture",
        "hudCost": "t = x = \\lceil \\log_{fo}(b_{i1}) \\rceil + 1 \\mid fo = bfr_I",
        "text": (
            "While binary search on a single-level index reduces the search space by a factor of 2 at each step, a multi-level index achieves dramatic acceleration by reducing the search space by the index fanout at every step. "
            "With fanout fo equal to the index blocking factor, each higher level indexes the blocks of the level beneath it, until all entries fit into a single root block. "
            "The total tree height x equals ceiling of log base fanout of b sub i 1, plus 1. "
            "Because balanced search trees prevent skew, production databases implement B-trees and B-plus trees where every node corresponds to a disk block. "
            "In a standard B-tree, record pointers reside at all levels of the tree. "
            "In a B-plus tree, all data record pointers are pushed exclusively to the leaf level, and leaf blocks are linked sequentially as a doubly linked list, enabling both lightning-fast point lookups in 3 to 4 block accesses and ultra-efficient range scans."
        )
    },
    {
        "id": 4,
        "title": "5. Static vs Extendable Hashing & Dynamic Directories",
        "hudCost": "\\text{Directory} = 2^d \\mid d' = d \\implies d \\leftarrow d + 1",
        "text": (
            "Hashing offers direct address calculation using a hash function h of k. "
            "In static hashing, a fixed number of primary bucket pages are allocated sequentially. "
            "As files grow, collision chains degrade search performance into linear scans, while over-allocating buckets initially wastes storage. "
            "Extendable hashing solves this through dynamic hashing. "
            "It maintains a directory of size 2 to the power d, where d is the global depth. "
            "The last d bits of the hash value index directly into the directory to find the bucket address. "
            "Each bucket maintains its own local depth d prime. "
            "When a bucket overflows, if its local depth equals the global depth, the directory doubles in size, global depth increments by 1, and the overflowed bucket splits into two new buckets with local depth incremented. "
            "However, if local depth is strictly less than global depth, the bucket splits without doubling the directory, simply updating existing directory pointers."
        )
    },
    {
        "id": 5,
        "title": "6. Bitmap Indexing & Multi-Attribute Bitwise Engine",
        "hudCost": "B_1 \\land B_2 \\mid B_1 \\lor B_2 \\mid \\neg B_1",
        "text": (
            "Bitmap indices provide high-speed filtering specifically engineered for attributes with low distinct cardinalities, such as gender, country, or income bracket. "
            "For each distinct attribute value, a bitmap vector contains one bit per record in the relation, where bit n is 1 if record n possesses that value, and 0 otherwise. "
            "Rather than reading data blocks from disk, complex multi-attribute queries are evaluated directly inside CPU registers using hardware bitwise instructions. "
            "An intersection query performs a bitwise AND between attribute bitmaps, a union executes a bitwise OR, and negation performs a bitwise NOT. "
            "Counting matching tuples is performed instantly via population count operations. "
            "Once the resulting bit vector is calculated, the query engine directly computes record addresses for the 1 bits, minimizing physical disk block I/O."
        )
    }
]

async def process_scene(sc):
    sc_id = sc["id"]
    mp3_path = os.path.join(audio_dir, f'chap1_scene_{sc_id}.mp3')
    tts = edge_tts.Communicate(sc["text"], VOICE)
    
    sentences = []
    audio_chunks = bytearray()
    
    async for chunk in tts.stream():
        if chunk["type"] == "audio":
            audio_chunks.extend(chunk["data"])
        elif chunk["type"] == "SentenceBoundary":
            s_time = chunk["offset"] / 1e7
            dur = chunk["duration"] / 1e7
            s_text = chunk["text"].strip()
            
            # Divide sentence into words proportionally
            raw_words = s_text.split()
            total_chars = sum(len(w) for w in raw_words)
            if total_chars == 0:
                total_chars = 1
            cur_w_start = s_time
            w_objs = []
            for w in raw_words:
                w_dur = (len(w) / total_chars) * dur
                w_objs.append({
                    "word": w,
                    "start": round(cur_w_start, 3),
                    "end": round(cur_w_start + w_dur, 3)
                })
                cur_w_start += w_dur
                
            sentences.append({
                "text": s_text,
                "start": round(s_time, 3),
                "end": round(s_time + dur, 3),
                "words": w_objs
            })
            
    with open(mp3_path, "wb") as f:
        f.write(audio_chunks)
        
    total_dur = sentences[-1]["end"] if sentences else 0
    b64_audio = base64.b64encode(audio_chunks).decode('utf-8')
    data_uri = f"data:audio/mp3;base64,{b64_audio}"
    
    print(f"✓ Scene {sc_id + 1} generated: {len(sentences)} sentences, {total_dur:.2f}s, {len(audio_chunks)} bytes")
    return {
        "id": sc_id,
        "title": sc["title"],
        "hudCost": sc["hudCost"],
        "duration": round(total_dur, 2),
        "audioUri": data_uri,
        "subtitles": sentences
    }

async def main():
    print("🎙️ Generating Chapter 1 Studio Audio & Timestamps...")
    results = []
    for sc in SCENES:
        res = await process_scene(sc)
        results.append(res)
        
    out_json = os.path.join(work_dir, 'chap1_data.json')
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    print(f"🎉 Chapter 1 assets saved to {out_json}")

if __name__ == "__main__":
    asyncio.run(main())

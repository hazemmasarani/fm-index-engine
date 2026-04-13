# fm-index-engine

An efficient implementation of the **DC3 (Skew) algorithm**, **Suffix Array construction**, **Burrows–Wheeler Transform (BWT)**, and **FM-index** for compressed full-text indexing and pattern searching.

---

## 📌 Overview

This project implements a complete pipeline for building a compressed text indexing structure:

1. **Suffix Array construction using DC3 (Skew Algorithm)**
2. **Burrows–Wheeler Transform (BWT) generation**
3. Construction of the **FM-index**
4. Efficient substring queries using backward search

The goal is to provide a clear, low-level implementation of modern string indexing techniques used in bioinformatics and search engines.

---

## 🧠 Algorithms Implemented

### 🔹 DC3 (Skew) Algorithm
A linear-time algorithm for constructing suffix arrays in **O(n)** time.

- Handles suffixes based on modulo 3 positions  
- Recursive sorting strategy  
- Efficient linear-time merging  

---

### 🔹 Suffix Array
A sorted array of all suffixes of a string.

Used as the foundation for:
- BWT construction  
- Pattern matching  
- FM-index building  

---

### 🔹 Burrows–Wheeler Transform (BWT)

Transforms a text into a permutation that is:
- More compressible  
- Efficient for pattern matching  

Key idea:
> Sort all cyclic rotations of the string and extract the last column.

---

### 🔹 FM-Index

A compressed full-text index built on top of BWT.

Supports:
- Fast substring search  
- Backward search algorithm  
- Reduced memory usage compared to suffix arrays  

Core components:
- BWT string  
- Occurrence table (rank queries)  
- C array (cumulative character counts)  

---

## ⚙️ Features

- ✔ DC3 suffix array construction (linear time)
- ✔ BWT generation from suffix array
- ✔ FM-index construction
- ✔ Backward search pattern matching
- ✔ Modular and clean implementation
- ✔ Educational and research-focused design

---

## 📂 Project Structure
```
fm-index-engine/
│
├── fm_index_engine/
│   ├── __init__.py
│   ├── dc3.py
│   ├── suffix_array.py
│   ├── bwt.py
│   ├── fm_index.py
│
├── tests/
│   ├── test_dc3.py
│   ├── test_bwt.py
│   ├── test_fm_index.py
│
├── examples/
│   └── demo_usage.py
│
├── requirements.txt
├── pyproject.toml   # (modern Python packaging)
└── README.md
```


---

## 🚀 Example Usage

### Build FM-index

```python
text = "banana$"
fm = FMIndex(text)
```
### 🔍 Search pattern
```python
results = fm.search("ana")
print(results)
```
output
```
Pattern found at positions: [1, 3]
```

## 📊 Complexity

| Step                | Complexity |
|---------------------|------------|
| DC3 Suffix Array    | O(n)       |
| BWT Construction    | O(n)       |
| FM-index Build      | O(n)       |
| Pattern Search      | O(m)       |

Where:

- `n` = text length  
- `m` = pattern length  

---

## 🎯 Applications

- Bioinformatics (DNA sequence search)
- Search engines
- Data compression
- Text indexing systems
- Information retrieval systems

## 📚 References

- Kärkkäinen & Sanders (2003) — Linear suffix array construction (DC3)
- Ferragina & Manzini — FM-index
- Burrows & Wheeler (1994) — Burrows–Wheeler Transform

---

## 🧑‍💻 Author

This project is an educational implementation of:

- Suffix arrays
- String algorithms
- Compressed text indexing structures


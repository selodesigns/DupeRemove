# 🧹 Duplicate File Remover

A Python script that scans a directory for duplicate files based on content (using SHA-256 hashes), deletes redundant copies, and reports how much disk space was freed.

## ⚠️ WARNING

> This script **permanently deletes** duplicate files.  
> There is **no undo**. Use it with caution and always back up your data first.

---

## 📦 Features

- Recursively scans a directory
- Uses SHA-256 hashes for accurate duplicate detection
- Deletes all but one copy of each duplicate
- Reports number of files removed and storage space saved
- Interactive confirmation before deletion

---

## 💻 Usage

### ✅ Requirements

No external dependencies — works with standard Python 3.

### ▶️ Run the Script

```bash
python dedupe.py /path/to/your/directory

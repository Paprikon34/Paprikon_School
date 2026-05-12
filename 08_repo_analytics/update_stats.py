import os
import json
from datetime import datetime

def get_repo_stats():
    stats = {
        "last_updated": datetime.now().isoformat(),
        "project_count": 0,
        "file_counts": {},
        "total_code_lines": 0,
        "total_doc_lines": 0
    }
    
    # Get the root directory relative to the script location
    script_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.abspath(os.path.join(script_dir, ".."))
    
    for root, dirs, files in os.walk(root_dir):
        # Skip .git and hidden folders
        if ".git" in root or ".vscode" in root or ".github" in root:
            continue
            
        # Count projects (top-level folders starting with numbers)
        if root == root_dir:
            for d in dirs:
                if d and d[0].isdigit():
                    stats["project_count"] += 1
        
        for file in files:
            ext = os.path.splitext(file)[1]
            if ext in [".py", ".cpp", ".h", ".md"]:
                stats["file_counts"][ext] = stats["file_counts"].get(ext, 0) + 1
                
                # Count lines
                try:
                    with open(os.path.join(root, file), 'r', encoding='utf-8') as f:
                        line_count = len(f.readlines())
                        if ext == ".md":
                            stats["total_doc_lines"] += line_count
                        else:
                            stats["total_code_lines"] += line_count
                except:
                    pass
                    
    return stats

def main():
    stats = get_repo_stats()
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(script_dir, "repo_stats.json")
    
    with open(output_path, "w", encoding='utf-8') as f:
        json.dump(stats, f, indent=4, ensure_ascii=False)
    print(f"Stats updated: {stats['last_updated']}")

if __name__ == "__main__":
    main()

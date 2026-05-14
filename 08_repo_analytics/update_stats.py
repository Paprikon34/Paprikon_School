import os
import json
from datetime import datetime

def get_repo_stats():
    stats = {
        "last_updated": datetime.now().isoformat(),
        "project_count": 0,
        "repo_size_kb": 0,
        "file_counts": {},
        "total_code_lines": 0,
        "total_doc_lines": 0,
        "average_lines_per_file": 0,
        "top_files_by_lines": [],
        "project_details": {}
    }
    
    # Get the root directory relative to the script location
    script_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.abspath(os.path.join(script_dir, ".."))
    
    all_files_info = []
    total_files = 0
    total_bytes = 0
    
    for root, dirs, files in os.walk(root_dir):
        # Skip .git and hidden folders
        if any(ignored in root for ignored in [".git", ".vscode", ".github", "__pycache__"]):
            continue
            
        # Get relative path to identify project
        rel_path = os.path.relpath(root, root_dir)
        path_parts = rel_path.split(os.sep)
        project_name = path_parts[0] if rel_path != "." else None
        
        # Initialize project details if it's a project folder (starts with digits)
        if project_name and project_name[0].isdigit():
            if project_name not in stats["project_details"]:
                stats["project_details"][project_name] = {
                    "file_count": 0,
                    "code_lines": 0,
                    "doc_lines": 0
                }
        
        for file in files:
            file_path = os.path.join(root, file)
            ext = os.path.splitext(file)[1]
            
            # Track file size for all files
            try:
                total_bytes += os.path.getsize(file_path)
            except:
                continue

            # Analyze specific file types
            if ext in [".py", ".cpp", ".h", ".md"]:
                total_files += 1
                stats["file_counts"][ext] = stats["file_counts"].get(ext, 0) + 1
                
                # Count lines
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        line_count = len(f.readlines())
                        
                        # Global line counts
                        if ext == ".md":
                            stats["total_doc_lines"] += line_count
                        else:
                            stats["total_code_lines"] += line_count
                        
                        # Project specific line counts
                        if project_name and project_name in stats["project_details"]:
                            stats["project_details"][project_name]["file_count"] += 1
                            if ext == ".md":
                                stats["project_details"][project_name]["doc_lines"] += line_count
                            else:
                                stats["project_details"][project_name]["code_lines"] += line_count
                        
                        all_files_info.append({
                            "file": os.path.basename(file_path),
                            "project": project_name or "root",
                            "lines": line_count
                        })
                except:
                    pass
    
    # Finalize stats
    stats["project_count"] = len(stats["project_details"])
    stats["repo_size_kb"] = round(total_bytes / 1024, 2)
    
    if total_files > 0:
        total_lines = stats["total_code_lines"] + stats["total_doc_lines"]
        stats["average_lines_per_file"] = round(total_lines / total_files, 1)
    
    # Get top 5 largest files by line count
    stats["top_files_by_lines"] = sorted(all_files_info, key=lambda x: x["lines"], reverse=True)[:5]
    
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

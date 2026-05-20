import os
import json
import sys
import subprocess
from datetime import datetime, timedelta, timezone

def check_12h_rule(dates):
    """
    Checks if there exists a subset of at least 3 commits that are separated by >= 12 hours.
    Dates must be a sorted list of datetime objects.
    
    Kontroluje, zda existuje podmnožina alespoň 3 commitů, které dělí alespoň 12 hodin.
    """
    n = len(dates)
    if n < 3:
        return False, []
    
    for i in range(n):
        for j in range(i + 1, n):
            if (dates[j] - dates[i]).total_seconds() >= 12 * 3600:
                for k in range(j + 1, n):
                    if (dates[k] - dates[j]).total_seconds() >= 12 * 3600:
                        return True, [dates[i], dates[j], dates[k]]
    return False, []

def get_git_stats(repo_root):
    """
    Queries git log to get total commits, active development days, last commit info,
    and weekly compliance statistics for the current student.
    
    Získává statistiky z gitu - celkový počet commitů, aktivní dny, informace o posledním commitu
    a splnění týdenních podmínek studenta.
    """
    git_stats = {
        "total_commits": 0,
        "active_days": 0,
        "last_commit_date": None,
        "last_commit_message": None,
        "last_commit_author": None,
        "weekly_compliance": {
            "commits_this_week_count": 0,
            "commits_target_met": False,
            "intervals_12h_met": False,
            "docs_rule_met": False,
            "estimated_discipline_points": 0
        }
    }
    try:
        result = subprocess.run(
            ["git", "log", "--pretty=format:%H|%cI|%an|%s"],
            capture_output=True,
            text=True,
            check=True,
            cwd=repo_root
        )
        lines = result.stdout.strip().split("\n")
        
        valid_commits = []
        for line in lines:
            if not line:
                continue
            parts = line.split("|", 3)
            if len(parts) < 4:
                continue
            h, dt, author, subject = parts
            try:
                commit_date = datetime.fromisoformat(dt)
                valid_commits.append({
                    "hash": h,
                    "date": commit_date,
                    "author": author,
                    "subject": subject
                })
            except:
                pass
        
        if valid_commits:
            git_stats["total_commits"] = len(valid_commits)
            active_days = set(c["date"].strftime("%Y-%m-%d") for c in valid_commits)
            git_stats["active_days"] = len(active_days)
            
            last_c = valid_commits[0]
            git_stats["last_commit_date"] = last_c["date"].isoformat()
            git_stats["last_commit_message"] = last_c["subject"]
            git_stats["last_commit_author"] = last_c["author"]
            
            # Monday is 0, Sunday is 6
            now = datetime.now().astimezone()
            monday_of_this_week = (now - timedelta(days=now.weekday())).replace(hour=0, minute=0, second=0, microsecond=0)
            
            user_commits_this_week = []
            for c in valid_commits:
                # Filter out automated report commits by Repo Bot to track real developer work
                if c["author"] != "Repo Bot" and c["date"] >= monday_of_this_week:
                    user_commits_this_week.append(c)
            
            git_stats["weekly_compliance"]["commits_this_week_count"] = len(user_commits_this_week)
            git_stats["weekly_compliance"]["commits_target_met"] = len(user_commits_this_week) >= 3
            
            user_dates = sorted([c["date"] for c in user_commits_this_week])
            has_12h, _ = check_12h_rule(user_dates)
            git_stats["weekly_compliance"]["intervals_12h_met"] = has_12h
            
    except Exception as e:
        print(f"⚠️ Nepodařilo se načíst Git statistiky: {e}")
        
    return git_stats

def get_repo_stats():
    """
    Scans the repository structure, counts files and lines, measures size,
    and merges the metrics with Git history analysis.
    """
    stats = {
        "last_updated": datetime.now().isoformat(),
        "project_count": 0,
        "total_directories": 0,
        "repo_size_kb": 0,
        "file_counts": {},
        "total_code_lines": 0,
        "total_doc_lines": 0,
        "total_data_lines": 0,
        "average_lines_per_file": 0,
        "top_files_by_lines": [],
        "project_details": {}
    }
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.abspath(os.path.join(script_dir, ".."))
    
    all_files_info = []
    total_files = 0
    total_bytes = 0
    
    for root, dirs, files in os.walk(root_dir):
        # Skip system and hidden folders
        if any(ignored in root for ignored in [".git", ".vscode", ".github", "__pycache__"]):
            continue
            
        stats["total_directories"] += 1
            
        # Get relative path to identify project folder
        rel_path = os.path.relpath(root, root_dir)
        path_parts = rel_path.split(os.sep)
        project_name = path_parts[0] if rel_path != "." else None
        
        # Initialize project details if it's a numeric project folder
        if project_name and project_name[0].isdigit():
            if project_name not in stats["project_details"]:
                stats["project_details"][project_name] = {
                    "file_count": 0,
                    "code_lines": 0,
                    "doc_lines": 0,
                    "data_lines": 0,
                    "has_doc": False
                }
        
        for file in files:
            file_path = os.path.join(root, file)
            ext = os.path.splitext(file)[1]
            
            try:
                total_bytes += os.path.getsize(file_path)
            except:
                continue

            # Track files by key extensions
            if ext in [".py", ".cpp", ".h", ".md", ".json", ".txt", ".yml", ".yaml", ".csv"]:
                total_files += 1
                stats["file_counts"][ext] = stats["file_counts"].get(ext, 0) + 1
                
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        line_count = len(f.readlines())
                        
                        if ext == ".md":
                            stats["total_doc_lines"] += line_count
                        elif ext in [".json", ".csv", ".txt", ".yml", ".yaml"]:
                            stats["total_data_lines"] += line_count
                        else:
                            stats["total_code_lines"] += line_count
                        
                        if project_name and project_name in stats["project_details"]:
                            stats["project_details"][project_name]["file_count"] += 1
                            if ext == ".md":
                                stats["project_details"][project_name]["doc_lines"] += line_count
                            elif ext in [".json", ".csv", ".txt", ".yml", ".yaml"]:
                                stats["project_details"][project_name]["data_lines"] += line_count
                            else:
                                stats["project_details"][project_name]["code_lines"] += line_count
                            
                            # Check for the existence of project documentation
                            if file.lower().endswith("_projekt.md"):
                                stats["project_details"][project_name]["has_doc"] = True
                        
                        all_files_info.append({
                            "file": os.path.basename(file_path),
                            "project": project_name or "root",
                            "lines": line_count
                        })
                except:
                    pass
    
    stats["project_count"] = len(stats["project_details"])
    stats["repo_size_kb"] = round(total_bytes / 1024, 2)
    
    if total_files > 0:
        total_lines = stats["total_code_lines"] + stats["total_doc_lines"] + stats["total_data_lines"]
        stats["average_lines_per_file"] = round(total_lines / total_files, 1)
    
    stats["top_files_by_lines"] = sorted(all_files_info, key=lambda x: x["lines"], reverse=True)[:5]
    
    # Query Git stats and merge them
    git_stats = get_git_stats(root_dir)
    stats.update(git_stats)
    
    # Check documentations compliance rule (README in root and _projekt.md in all numeric folders)
    readme_exists = os.path.exists(os.path.join(root_dir, "README.md"))
    all_projects_documented = all(p.get("has_doc", False) for p in stats["project_details"].values())
    stats["weekly_compliance"]["docs_rule_met"] = readme_exists and all_projects_documented
    
    # Calculate estimated weekly discipline points (+20 points per satisfied rule)
    points = 0
    if stats["weekly_compliance"]["commits_target_met"]:
        points += 20
    if stats["weekly_compliance"]["intervals_12h_met"]:
        points += 20
    if stats["weekly_compliance"]["docs_rule_met"]:
        points += 20
    stats["weekly_compliance"]["estimated_discipline_points"] = points
    
    return stats

def update_readme_stats(stats, readme_path):
    """
    Automatically modifies root README.md to keep the repository statistics section fully updated.
    
    Automaticky aktualizuje sekci statistik v souboru README.md.
    """
    if not os.path.exists(readme_path):
        return
        
    try:
        with open(readme_path, "r", encoding="utf-8") as f:
            content = f.read()
            
        start_tag = "## 📈 Statistiky repozitáře"
        end_tag = "\n---"
        
        start_idx = content.find(start_tag)
        if start_idx == -1:
            return
            
        # Find next divider after the statistics section header
        end_idx = content.find(end_tag, start_idx + len(start_tag))
        if end_idx == -1:
            return
            
        repo_size_mb = round(stats['repo_size_kb'] / 1024, 2)
        
        documented_count = sum(1 for p in stats.get("project_details", {}).values() if p.get("has_doc", False))
        total_projects = stats.get("project_count", 0)
        
        if stats.get("weekly_compliance", {}).get("docs_rule_met", False):
            doc_status = "100% (Up to code) ✅"
        else:
            doc_status = f"Rozpracováno ({documented_count}/{total_projects}) 🚧"
            
        new_table = f"""{start_tag}

| Metrika | Hodnota |
| :--- | :--- |
| **Počet projektů** | {stats['project_count']} |
| **Celkem řádků kódu** | {stats['total_code_lines']} |
| **Celkem dokumentace** | {stats['total_doc_lines']} řádků |
| **Velikost repozitáře** | ~{repo_size_mb} MB |
| **Hlavní jazyky** | Python, C++ |
| **Stav dokumentace** | {doc_status} |
| **Průměrná náročnost** | ⭐⭐⭐⭐ (Pokročilý) |
"""
        new_content = content[:start_idx] + new_table + content[end_idx:]
        
        with open(readme_path, "w", encoding="utf-8") as f:
            f.write(new_content)
        print("✅ Statistiky v souboru README.md byly úspěšně aktualizovány.")
    except Exception as e:
        print(f"⚠️ Nepodařilo se aktualizovat README.md: {e}")

def generate_markdown_report(stats, output_path):
    """
    Generates a beautifully formatted human-readable Markdown analytics report.
    
    Generuje přehledný report o stavu repozitáře ve formátu Markdown.
    """
    md_content = f"# 📊 Repository Analytics & Compliance Report\n\n"
    md_content += f"*Poslední aktualizace: **{datetime.fromisoformat(stats['last_updated']).strftime('%d.%m.%Y v %H:%M:%S')}***\n\n"
    
    # 🎓 Grading Dashboard
    compliance = stats.get("weekly_compliance", {})
    commits_count = compliance.get("commits_this_week_count", 0)
    commits_met = compliance.get("commits_target_met", False)
    intervals_met = compliance.get("intervals_12h_met", False)
    docs_met = compliance.get("docs_rule_met", False)
    points = compliance.get("estimated_discipline_points", 0)
    
    documented_count = sum(1 for p in stats.get("project_details", {}).values() if p.get("has_doc", False))
    total_projects = stats.get("project_count", 0)
    
    commits_icon = "✅" if commits_met else "❌"
    commits_text = "Splněno" if commits_met else f"Nesplněno (Cíl: min 3, aktuálně {commits_count})"
    
    intervals_icon = "✅" if intervals_met else "❌"
    intervals_text = "Splněno (Detekován rozestup >= 12h mezi 3 commity)" if intervals_met else "Nesplněno (Není nalezen 12hodinový rozestup mezi 3 commity)"
    
    docs_icon = "✅" if docs_met else "❌"
    docs_text = f"Splněno (Dokumentováno {documented_count} z {total_projects} projektů)" if docs_met else f"Nesplněno (Dokumentováno {documented_count} z {total_projects} projektů)"
    
    md_content += f"> [!IMPORTANT]\n"
    md_content += f"> ### 🎓 Týdenní Hodnocení & Disciplína (Grading Dashboard)\n"
    md_content += f"> Tato sekce vyhodnocuje plnění administrativních podmínek pro získání bonusu **60 bodů** do vašeho Týdenního Indexu.\n"
    md_content += f"> \n"
    md_content += f"> - **Podmínka 1: Min. 3 commity za týden**\n"
    md_content += f">   - *Stav:* {commits_icon} **{commits_count}/3** - {commits_text}\n"
    md_content += f"> - **Podmínka 2: Pravidlo 12 hodin rozestupu**\n"
    md_content += f">   - *Stav:* {intervals_icon} - {intervals_text}\n"
    md_content += f"> - **Podmínka 3: Dokumentace README.md a [nazev]_projekt.md**\n"
    md_content += f">   - *Stav:* {docs_icon} - {docs_text}\n"
    md_content += f"> \n"
    md_content += f"> **Odhadovaný týdenní bonus za disciplínu:** `🏆 {points} / 60 bodů`\n"
    md_content += f"> *Poznámka: Pro přičtení bonusu je nutné získat minimálně 6 bodů za kvalitu kódu od AI (pravidlo 30%).*\n\n"
    
    # 📈 Celkový přehled repozitáře
    md_content += f"## 📈 Celkový přehled repozitáře\n\n"
    md_content += f"| Metrika | Hodnota | Popis |\n"
    md_content += f"| :--- | :--- | :--- |\n"
    md_content += f"| **Počet projektů** | `{stats['project_count']}` | Celkový počet evidovaných projektů |\n"
    md_content += f"| **Počet adresářů** | `{stats.get('total_directories', 0)}` | Celkový počet složek (mimo skryté) |\n"
    md_content += f"| **Velikost repozitáře** | `{stats['repo_size_kb']:.2f} KB` (~`{stats['repo_size_kb']/1024:.2f} MB`) | Celková fyzická velikost souborů |\n"
    md_content += f"| **Celkem řádků kódu** | `{stats['total_code_lines']}` | Celkový počet řádků ve zdrojových kódech (.py, .cpp, .h) |\n"
    md_content += f"| **Celkem řádků dokumentace** | `{stats['total_doc_lines']}` | Celkový počet řádků v dokumentaci (.md) |\n"
    md_content += f"| **Celkem datových řádků** | `{stats['total_data_lines']}` | Řádky v konfiguracích a datových souborech (.json, .txt, etc) |\n"
    md_content += f"| **Průměrně řádků na soubor** | `{stats['average_lines_per_file']}` | Průměrná délka analyzovaného souboru |\n\n"
    
    # 🐙 Git Aktivita & Historie
    md_content += f"## 🐙 Git Aktivita & Historie\n\n"
    md_content += f"| Metrika | Hodnota | Popis |\n"
    md_content += f"| :--- | :--- | :--- |\n"
    md_content += f"| **Celkový počet commitů** | `{stats.get('total_commits', 0)}` | Celkový počet verzí v historii |\n"
    md_content += f"| **Počet aktivních dnů** | `{stats.get('active_days', 0)}` | Počet dní s alespoň jedním commitem |\n"
    md_content += f"| **Poslední commit (Autor)** | `{stats.get('last_commit_author', 'N/A')}` | Kdo provedl poslední změnu |\n"
    md_content += f"| **Poslední commit (Zpráva)** | `{stats.get('last_commit_message', 'N/A')}` | Popis poslední úpravy |\n"
    md_content += f"| **Poslední commit (Datum)** | `{stats.get('last_commit_date', 'N/A')}` | Čas poslední úpravy |\n\n"
    
    # 🗂️ File Extensions Table
    md_content += f"## 🗂️ Distribuce přípon souborů\n\n"
    md_content += f"| Přípona | Počet souborů | Podíl z celku |\n"
    md_content += f"| :--- | :---: | :---: |\n"
    total_tracked_files = sum(stats['file_counts'].values())
    for ext, count in sorted(stats['file_counts'].items(), key=lambda x: x[1], reverse=True):
        percentage = (count / total_tracked_files) * 100 if total_tracked_files > 0 else 0
        md_content += f"| **{ext}** | {count} | {percentage:.1f}% |\n"
    md_content += "\n"
    
    # 📊 Mermaid Pie Chart
    md_content += f"### 📊 Poměr řádků v repozitáři\n"
    md_content += f"```mermaid\n"
    md_content += f"pie title \"Distribuce řádků v repozitáři\"\n"
    md_content += f"    \"Zdrojový kód\" : {stats['total_code_lines']}\n"
    md_content += f"    \"Dokumentace\" : {stats['total_doc_lines']}\n"
    md_content += f"    \"Data & Konfigurace\" : {stats['total_data_lines']}\n"
    md_content += f"```\n\n"
    
    # 🏆 Top 5 Largest Files
    md_content += f"## 🏆 5 Největších souborů (podle řádků)\n\n"
    md_content += f"| # | Název souboru | Projekt | Počet řádků |\n"
    md_content += f"| :--- | :--- | :--- | :---: |\n"
    for idx, f in enumerate(stats['top_files_by_lines'], 1):
        md_content += f"| {idx} | `{f['file']}` | {f['project']} | {f['lines']} |\n"
    md_content += "\n"
    
    # 📁 Project Details Table
    md_content += f"## 📁 Detailní přehled jednotlivých projektů\n\n"
    md_content += f"| ID / Složka | Soubory | Kód (řádky) | Dokumentace | Data (řádky) | Stav Dokumentace |\n"
    md_content += f"| :--- | :---: | :---: | :---: | :---: | :---: |\n"
    for proj, details in sorted(stats['project_details'].items()):
        proj_doc_status = "✅ Odevzdána" if details.get('has_doc', False) else "❌ Chybí"
        md_content += f"| **{proj}** | {details.get('file_count', 0)} | {details.get('code_lines', 0)} | {details.get('doc_lines', 0)} | {details.get('data_lines', 0)} | {proj_doc_status} |\n"
    
    with open(output_path, "w", encoding='utf-8') as f:
        f.write(md_content)

def main():
    # Ensure UTF-8 output on Windows (avoids Mojibake)
    try:
        if hasattr(sys.stdout, 'reconfigure'):
            getattr(sys.stdout, 'reconfigure')(encoding='utf-8')
        elif hasattr(sys.stdout, 'buffer'):
            import io
            sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    except (AttributeError, TypeError):
        pass

    stats = get_repo_stats()
    script_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.abspath(os.path.join(script_dir, ".."))
    
    json_output_path = os.path.join(script_dir, "repo_stats.json")
    with open(json_output_path, "w", encoding='utf-8') as f:
        json.dump(stats, f, indent=4, ensure_ascii=False)
        
    md_output_path = os.path.join(script_dir, "repo_report.md")
    generate_markdown_report(stats, md_output_path)
    
    readme_path = os.path.join(root_dir, "README.md")
    update_readme_stats(stats, readme_path)
    
    print(f"Stats updated: {stats['last_updated']}")
    print(f"Report generated: repo_report.md")

if __name__ == "__main__":
    main()

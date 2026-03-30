import sys
import json
import requests
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QListWidget, QLabel, QLineEdit, 
                             QScrollArea, QFrame, QProgressBar, QGridLayout,
                             QPushButton, QTabWidget, QComboBox)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QSize
from PyQt6.QtGui import QPixmap, QFont, QIcon, QColor, QPalette

# Type Colors map
TYPE_COLORS = {
    "normal": "#A8A77A", "fire": "#EE8130", "water": "#6390F0", 
    "electric": "#F7D02C", "grass": "#7AC74C", "ice": "#96D9D6", 
    "fighting": "#C22E28", "poison": "#A33EA1", "ground": "#E2BF65", 
    "flying": "#A98FF3", "psychic": "#F95587", "bug": "#A6B91A", 
    "rock": "#B6A136", "ghost": "#735797", "dragon": "#6F35FC", 
    "steel": "#B7B7CE", "fairy": "#D685AD"
}

class ImageLoader(QThread):
    """
    Background thread for loading images from URLs without blocking the main GUI thread.
    Emits a signal with the loaded QImage when finished.
    """
    loaded = pyqtSignal(object) 

    def __init__(self, url):
        super().__init__()
        self.url = url

    def run(self):
        """Thread's main loop to fetch image bytes from the API."""
        try:
            if not self.url:
                return
            # User agent added to comply with PokeAPI guidelines if necessary
            headers = {"User-Agent": "PokedexBot/1.0"}
            response = requests.get(self.url, timeout=10, headers=headers)
            if response.status_code == 200:
                data = response.content
                # Use QImage for thread-safe loading
                from PyQt6.QtGui import QImage
                image = QImage()
                if image.loadFromData(data):
                    self.loaded.emit(image)
        except Exception as e:
            print(f"Image load error: {e}")

class RemoteImage(QLabel):
    """
    Custom QLabel sub-class that handles asynchronous loading of remote images.
    Shows a placeholder while loading.
    """
    def __init__(self, url, size=80):
        super().__init__()
        self.size = size
        self.setFixedSize(size, size)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setStyleSheet("background: transparent;")
        if url:
            self.setText("...")
            self.loader = ImageLoader(url)
            self.loader.loaded.connect(self.set_image_from_qimage)
            self.loader.start()
        else:
            self.setText("?")

    def set_image_from_qimage(self, qimage):
        pixmap = QPixmap.fromImage(qimage)
        scaled = pixmap.scaled(self.size, self.size, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        self.setPixmap(scaled)

class PokedexWindow(QMainWindow):
    """
    Main Application Window for the Pokedex GUI.
    Handles layout management, data filtering, and user interaction.
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pokedex Ultra")
        self.resize(1100, 800)
        
        # Internal application state
        self.pokemon_data = {}
        self.filtered_keys = []
        self.selected_types = set()
        
        # Initial data load from local JSON
        self.load_data()
        
        # UI Setup
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QHBoxLayout(main_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Left Panel (List)
        left_panel = QFrame()
        left_panel.setFixedWidth(300)
        left_panel.setStyleSheet("background-color: #2b2b2b; border-right: 1px solid #444;")
        left_layout = QVBoxLayout(left_panel)
        
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search Pokemon...")
        self.search_bar.setStyleSheet("""
            QLineEdit {
                padding: 10px;
                border: 1px solid #555;
                border-radius: 5px;
                background-color: #333;
                color: white;
                font-size: 14px;
            }
        """)
        self.search_bar.textChanged.connect(self.apply_filters)
        
        # Sorting & Region Panel
        control_grid = QGridLayout()
        
        self.sort_box = QComboBox()
        self.sort_box.addItems(["Sort: ID (Asc)", "Sort: ID (Desc)", "Sort: Name (A-Z)", "Sort: Name (Z-A)", "Sort: Total Stats"])
        self.sort_box.setStyleSheet("background: #333; color: white; padding: 5px; border: 1px solid #444;")
        self.sort_box.currentIndexChanged.connect(self.apply_filters)
        
        self.region_box = QComboBox()
        self.region_box.addItems(["All Regions", "Kanto", "Johto", "Hoenn", "Sinnoh", "Unova", "Kalos", "Alola", "Galar", "Paldea"])
        self.region_box.setStyleSheet("background: #333; color: white; padding: 5px; border: 1px solid #444;")
        self.region_box.currentIndexChanged.connect(self.apply_filters)
        
        control_grid.addWidget(QLabel("Sort:"), 0, 0)
        control_grid.addWidget(self.sort_box, 0, 1)
        control_grid.addWidget(QLabel("Region:"), 1, 0)
        control_grid.addWidget(self.region_box, 1, 1)

        # Type Filter Panel
        type_filter_label = QLabel("Filter by Type:")
        type_filter_label.setStyleSheet("color: #888; margin-top: 10px; font-weight: bold;")
        
        self.type_button_layout = QGridLayout()
        self.type_button_layout.setSpacing(2)
        
        types_list = list(TYPE_COLORS.keys())
        for i, t in enumerate(types_list):
            btn = QPushButton(t[:3].upper())
            btn.setCheckable(True)
            btn.setFixedSize(35, 25)
            color = TYPE_COLORS[t]
            btn.setStyleSheet(f"""
                QPushButton {{ background-color: #222; color: {color}; border: 1px solid {color}; font-size: 9px; font-weight: bold; border-radius: 3px;}}
                QPushButton:checked {{ background-color: {color}; color: white; }}
            """)
            btn.toggled.connect(lambda checked, type_name=t: self.toggle_type_filter(type_name, checked))
            self.type_button_layout.addWidget(btn, i // 6, i % 6)

        self.refresh_btn = QPushButton("🔄 Refresh Data")
        self.refresh_btn.setStyleSheet("""
            QPushButton {
                background-color: #333; color: #aaa; border: 1px solid #444; padding: 8px; border-radius: 3px; font-size: 11px; margin-top: 5px;
            }
            QPushButton:hover { background-color: #444; color: white; }
        """)
        self.refresh_btn.clicked.connect(self.on_refresh)

        self.list_widget = QListWidget()
        self.list_widget.setStyleSheet("""
            QListWidget {
                background-color: #2b2b2b;
                border: none;
                color: #ddd;
                font-size: 16px;
            }
            QListWidget::item {
                padding: 10px;
                border-bottom: 1px solid #333;
            }
            QListWidget::item:selected {
                background-color: #d32f2f;
                color: white;
            }
        """)
        self.list_widget.currentRowChanged.connect(self.on_selection_change)
        
        left_layout.addWidget(self.search_bar)
        left_layout.addLayout(control_grid)
        left_layout.addWidget(type_filter_label)
        left_layout.addLayout(self.type_button_layout)
        left_layout.addWidget(self.refresh_btn)
        left_layout.addWidget(self.list_widget)
        
        # Right Panel (Details)
        self.right_panel = QScrollArea()
        self.right_panel.setWidgetResizable(True)
        self.right_panel.setStyleSheet("background-color: #1e1e1e; border: none;")
        
        self.detail_container = QWidget()
        self.detail_layout = QVBoxLayout(self.detail_container)
        self.detail_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        # Header (Name + ID)
        self.name_label = QLabel("Select a Pokemon")
        self.name_label.setStyleSheet("font-size: 32px; font-weight: bold; color: white; margin-top: 20px;")
        self.name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.id_label = QLabel("#000")
        self.id_label.setStyleSheet("font-size: 18px; color: #888;")
        self.id_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Image
        self.image_label = QLabel()
        self.image_label.setFixedSize(300, 300)
        self.image_label.setStyleSheet("background-color: #252525; border-radius: 15px; border: 2px solid #333;")
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        image_container = QWidget()
        img_layout = QHBoxLayout(image_container)
        img_layout.addStretch()
        img_layout.addWidget(self.image_label)
        img_layout.addStretch()

        button_layout = QHBoxLayout()
        self.shiny_btn = QPushButton("✨ Shiny Mode")
        self.shiny_btn.setCheckable(True)
        self.shiny_btn.setStyleSheet("""
            QPushButton {
                background-color: #444; color: white; border: 1px solid #555; padding: 5px; border-radius: 5px;
            }
            QPushButton:checked {
                background-color: #ffd700; color: black; border: 1px solid #cca300;
            }
        """)
        self.shiny_btn.toggled.connect(self.toggle_shiny)
        button_layout.addStretch()
        button_layout.addWidget(self.shiny_btn)
        button_layout.addStretch()

        # Types
        self.types_container = QWidget()
        self.types_layout = QHBoxLayout(self.types_container)
        self.types_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Info Grid (Basic Info)
        self.info_grid = QWidget()
        self.grid_layout = QGridLayout(self.info_grid)
        self.grid_layout.setSpacing(10)

        # Tabs for Detailed Info
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("""
            QTabWidget::pane { border: 1px solid #444; background: #252525;} 
            QTabBar::tab { background: #333; color: #aaa; padding: 10px; }
            QTabBar::tab:selected { background: #555; color: white; }
        """)
        
        self.stats_tab = QWidget()
        self.stats_layout = QVBoxLayout(self.stats_tab)
        
        self.moves_tab = QListWidget()
        self.moves_tab.setStyleSheet("background: #252525; color: #ddd; border: none;")
        
        self.loc_tab = QListWidget()
        self.loc_tab.setStyleSheet("background: #252525; color: #ddd; border: none;")
        
        self.evo_scroll = QScrollArea()
        self.evo_scroll.setWidgetResizable(True)
        self.evo_scroll.setStyleSheet("background: transparent; border: none;")
        self.evo_tab = QWidget()
        self.evo_layout = QHBoxLayout(self.evo_tab)
        self.evo_scroll.setWidget(self.evo_tab)
        
        self.forms_scroll = QScrollArea()
        self.forms_scroll.setWidgetResizable(True)
        self.forms_scroll.setStyleSheet("background: transparent; border: none;")
        self.forms_tab = QWidget()
        self.forms_layout = QHBoxLayout(self.forms_tab)
        self.forms_scroll.setWidget(self.forms_tab)

        self.tabs.addTab(self.stats_tab, "Stats")
        self.tabs.addTab(self.moves_tab, "Moves")
        self.tabs.addTab(self.evo_scroll, "Evolutions")
        self.tabs.addTab(self.forms_scroll, "Forms")
        self.tabs.addTab(self.loc_tab, "Locations")
        
        self.entries_scroll = QScrollArea()
        self.entries_scroll.setWidgetResizable(True)
        self.entries_scroll.setStyleSheet("background: transparent; border: none;")
        self.entries_tab = QWidget()
        self.entries_layout = QVBoxLayout(self.entries_tab)
        self.entries_scroll.setWidget(self.entries_tab)
        self.tabs.addTab(self.entries_scroll, "Entries")

        # Labels for dynamic content
        self.desc_label = QLabel()
        self.desc_label.setWordWrap(True)
        self.desc_label.setStyleSheet("font-size: 16px; font-style: italic; color: #bbb; padding: 20px;")
        self.desc_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Assemble Right Panel
        self.detail_layout.addWidget(self.name_label)
        self.detail_layout.addWidget(self.id_label)
        self.detail_layout.addWidget(image_container)
        self.detail_layout.addLayout(button_layout)
        self.detail_layout.addWidget(self.types_container)
        self.detail_layout.addWidget(self.desc_label)
        
        # Divider
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        line.setStyleSheet("background-color: #444;")
        self.detail_layout.addWidget(line)
        
        self.detail_layout.addWidget(self.info_grid)
        self.detail_layout.addWidget(self.tabs)
        
        self.right_panel.setWidget(self.detail_container)
        
        layout.addWidget(left_panel)
        layout.addWidget(self.right_panel)
        
        # Apply initial filters/sorting
        self.apply_filters()

    def on_refresh(self):
        """Reload data from disk and preserve current selection if possible."""
        current_name = getattr(self, 'current_name', None)
        self.load_data()
        self.apply_filters()
        if current_name:
            items = self.list_widget.findItems(current_name.capitalize(), Qt.MatchFlag.MatchExactly)
            if items:
                self.list_widget.setCurrentItem(items[0])
        
    def load_data(self):
        """Parses the local pokemon.json file."""
        try:
            import os
            script_dir = os.path.dirname(os.path.abspath(__file__))
            data_path = os.path.join(script_dir, "pokemon.json")
            with open(data_path, "r") as f:
                self.pokemon_data = json.load(f)
            self.filtered_keys = list(self.pokemon_data.keys())
        except Exception as e:
            print(f"Error loading data: {e}")
            self.pokemon_data = {}

    def populate_list(self):
        self.list_widget.clear()
        for name in self.filtered_keys:
            display_name = name.replace("-", " ").title()
            self.list_widget.addItem(f"#{self.pokemon_data[name].get('id', '000')} {display_name}")

    def toggle_type_filter(self, type_name, checked):
        if checked:
            self.selected_types.add(type_name)
        else:
            self.selected_types.discard(type_name)
        self.apply_filters()

    def apply_filters(self):
        """
        Processes search text, region filters, and type filters to update 
        the list of visible Pokemon.
        """
        search_text = self.search_bar.text().lower().strip()
        search_words = search_text.split()
        region_filter = self.region_box.currentText()
        
        results = []
        for name, data in self.pokemon_data.items():
            # Search filter (Check key, name, and ID)
            display_name = name.replace("-", " ").lower()
            if search_words:
                match = True
                full_text = f"{name.lower()} {display_name} {data.get('id', '')}"
                for word in search_words:
                    if word not in full_text:
                        match = False
                        break
                if not match:
                    continue
            
            # Type filter
            if self.selected_types:
                pokemon_types = set(data.get('types', []))
                if not self.selected_types.issubset(pokemon_types):
                    continue
            
            # Region filter
            if region_filter != "All Regions" and data.get('region') != region_filter:
                continue
            
            results.append(name)
        
        # Sorting
        sort_mode = self.sort_box.currentText()
        if "ID (Asc)" in sort_mode:
            results.sort(key=lambda x: (self.pokemon_data[x].get('id', 9999), x))
        elif "ID (Desc)" in sort_mode:
            results.sort(key=lambda x: (self.pokemon_data[x].get('id', 0), x), reverse=True)
        elif "Name (A-Z)" in sort_mode:
            results.sort()
        elif "Name (Z-A)" in sort_mode:
            results.sort(reverse=True)
        elif "Total Stats" in sort_mode:
            results.sort(key=lambda x: (sum(self.pokemon_data[x].get('stats', {}).values()), x), reverse=True)
            
        self.filtered_keys = results
        self.populate_list()

    def on_selection_change(self, row):
        if row < 0 or row >= len(self.filtered_keys):
            return
        
        self.current_name = self.filtered_keys[row]
        self.current_data = self.pokemon_data[self.current_name]
        self.update_details()

    def toggle_shiny(self, checked):
        if hasattr(self, 'current_data'):
            self.update_image(checked)

    def update_details(self):
        """Rebuilds the entire right panel detail view when selection changes."""
        data = self.current_data
        name = self.current_name
        
        self.name_label.setText(name.replace("-", " ").title())
        self.id_label.setText(f"#{data.get('id', '???')}")
        
        # Types
        for i in reversed(range(self.types_layout.count())): 
            item = self.types_layout.itemAt(i)
            if item.widget():
                item.widget().setParent(None)
            else:
                self.types_layout.removeItem(item)
            
        for t in data.get('types', []):
            lbl = QLabel(t.upper())
            color = TYPE_COLORS.get(t, "#777")
            lbl.setStyleSheet(f"background-color: {color}; color: white; padding: 5px 15px; border-radius: 12px; font-weight: bold;")
            self.types_layout.addWidget(lbl)
            
        # Description
        self.desc_label.setText(data.get('description', 'No description.'))
        
        # Image
        self.update_image(self.shiny_btn.isChecked())

        # Clear Grid
        for i in reversed(range(self.grid_layout.count())): 
            item = self.grid_layout.itemAt(i)
            if item.widget():
                item.widget().setParent(None)
            else:
                self.grid_layout.removeItem(item)

        # Physical Properties & New Data
        self.add_grid_item("Height", f"{data.get('height', '?')} m", 0, 0)
        self.add_grid_item("Weight", f"{data.get('weight', '?')} kg", 0, 1)
        self.add_grid_item("Catch Rate", f"{data.get('capture_rate', '?')}", 0, 2)
        
        # Hatch steps calculation
        h_counter = data.get('hatch_counter') 
        hatch_steps = f"{h_counter * 255} steps" if h_counter is not None else "???"
        
        self.add_grid_item("Hatch Steps", hatch_steps, 1, 0)
        self.add_grid_item("Base Happiness", f"{data.get('base_happiness', '?')}", 1, 1)
        self.add_grid_item("Base Exp", f"{data.get('base_experience', '?')}", 1, 2)

        self.add_grid_item("Egg Groups", ", ".join(data.get('egg_groups', [])).title(), 2, 0, 1, 3)
        self.add_grid_item("Gender", data.get('gender', 'Unknown'), 3, 0, 1, 3)
        self.add_grid_item("Abilities", ", ".join([a['name'].title() for a in data.get('abilities', [])]), 4, 0, 1, 3)
        
        # Stats Tab
        for i in reversed(range(self.stats_layout.count())): 
            item = self.stats_layout.itemAt(i)
            if item.widget():
                item.widget().setParent(None)
            else:
                self.stats_layout.removeItem(item)

        stats = data.get('stats', {})
        for stat_name, value in stats.items():
            container = QWidget()
            h = QHBoxLayout(container)
            h.setContentsMargins(0,0,0,0)
            
            lbl = QLabel(stat_name.upper().replace("-", " "))
            lbl.setFixedWidth(120)
            lbl.setStyleSheet("color: #aaa; font-weight: bold;")
            
            pbar = QProgressBar()
            # Pokemon stats typically range from 1 to 255
            pbar.setRange(0, 255)
            pbar.setValue(value)
            pbar.setTextVisible(True)
            pbar.setFormat(f"{value}")
            pbar.setStyleSheet(f"""
                QProgressBar {{
                    background-color: #333; border-radius: 5px; color: white; text-align: center; font-weight: bold;
                }}
                QProgressBar::chunk {{
                    background-color: {self.get_stat_color(value)}; border-radius: 5px;
                }}
            """)
            
            h.addWidget(lbl)
            h.addWidget(pbar)
            self.stats_layout.addWidget(container)
        self.stats_layout.addStretch()
        
        # Moves Tab
        self.moves_tab.clear()
        moves = data.get('moves', [])
        for m in moves:
            if isinstance(m, dict):
                method = f" (Lvl {m['level']})" if m['level'] > 0 else ""
                self.moves_tab.addItem(f"{m['name'].replace('-', ' ').title()}{method}")
            else:
                self.moves_tab.addItem(str(m))
                
        # Locations Tab
        self.loc_tab.clear()
        locs = data.get('locations', [])
        
        if not locs:
            evos = data.get('evolution', [])
            if evos and name in evos:
                idx = evos.index(name)
                if idx > 0:
                    # It's an evolved form
                    self.loc_tab.addItem(f"Obtained by Evolving {evos[0].title()}")
                    self.loc_tab.addItem("(Check Evolutions tab for details)")
                else:
                    self.loc_tab.addItem("No wild locations found")
                    self.loc_tab.addItem("(May be a Gift, Event, or Starter)")
            else:
                self.loc_tab.addItem("Unknown / No Data")
        
        for l in locs:
            self.loc_tab.addItem(l.title())

        # Evolution Tab
        for i in reversed(range(self.evo_layout.count())): 
            item = self.evo_layout.itemAt(i)
            if item.widget():
                item.widget().setParent(None)
            else:
                self.evo_layout.removeItem(item)
        
        evos = data.get('evolution', [])
        for e in evos:
            evo_container = QWidget()
            v = QVBoxLayout(evo_container)
            v.setContentsMargins(5, 5, 5, 5)
            
            # Get Sprite
            sprite_url = None
            if e in self.pokemon_data:
                sprite_url = self.pokemon_data[e].get('sprite')
                if not sprite_url:
                    # Fallback to species base
                    eid = self.pokemon_data[e].get('id')
                    for k, v in self.pokemon_data.items():
                        if v.get('id') == eid and '-' not in k:
                            sprite_url = v.get('sprite')
                            break
            
            img = RemoteImage(sprite_url, 100)
            
            btn = QPushButton(e.title())
            btn.setFixedWidth(120)
            btn.setStyleSheet("""
                QPushButton { background: #333; color: white; border: 1px solid #555; padding: 5px; border-radius: 4px; font-size: 11px;}
                QPushButton:hover { background: #444; }
            """)
            btn.clicked.connect(lambda checked, name=e: self.jump_to_pokemon(name))
            
            v.addWidget(img)
            v.addWidget(btn)
            v.setAlignment(Qt.AlignmentFlag.AlignCenter)
            
            self.evo_layout.addWidget(evo_container)
            
            # Add Arrow if not last
            if e != evos[-1]:
                arrow = QLabel("➔")
                arrow.setStyleSheet("font-size: 24px; color: #555; margin-bottom: 20px;")
                self.evo_layout.addWidget(arrow)
                
        self.evo_layout.addStretch()

        # Forms Tab
        for i in reversed(range(self.forms_layout.count())): 
            item = self.forms_layout.itemAt(i)
            if item.widget():
                item.widget().setParent(None)
            else:
                self.forms_layout.removeItem(item)

        forms = data.get('forms', [])
        for f in forms:
            f_container = QWidget()
            fv = QVBoxLayout(f_container)
            fv.setContentsMargins(5,5,5,5)
            
            f_sprite = None
            if f in self.pokemon_data:
                f_sprite = self.pokemon_data[f].get('sprite')
                if not f_sprite:
                    # Fallback to species base
                    fid = self.pokemon_data[f].get('id')
                    for k, v in self.pokemon_data.items():
                        if v.get('id') == fid and '-' not in k:
                            f_sprite = v.get('sprite')
                            break
            
            f_img = RemoteImage(f_sprite, 80)
            f_btn = QPushButton(f.replace("-", " ").title())
            f_btn.setFixedWidth(120)
            f_btn.setStyleSheet("""
                QPushButton { background: #333; color: white; border: 1px solid #555; padding: 5px; border-radius: 4px; font-size: 10px;}
                QPushButton:hover { background: #444; }
            """)
            f_btn.clicked.connect(lambda checked, name=f: self.jump_to_pokemon(name))
            
            fv.addWidget(f_img)
            fv.addWidget(f_btn)
            fv.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.forms_layout.addWidget(f_container)
        self.forms_layout.addStretch()

        # Entries Tab
        for i in reversed(range(self.entries_layout.count())): 
            item = self.entries_layout.itemAt(i)
            if item.widget():
                item.widget().setParent(None)
            else:
                self.entries_layout.removeItem(item)

        entries = data.get('pokedex_entries', [])
        for entry in entries:
            entry_container = QFrame()
            entry_container.setStyleSheet("background-color: #2b2b2b; border-radius: 8px; margin-bottom: 5px; border: 1px solid #333;")
            ev = QVBoxLayout(entry_container)
            
            v_lbl = QLabel(entry['version'])
            v_lbl.setStyleSheet("color: #d32f2f; font-weight: bold; font-size: 14px; border: none;")
            
            t_lbl = QLabel(entry['text'])
            t_lbl.setWordWrap(True)
            t_lbl.setStyleSheet("color: #ddd; font-size: 14px; border: none;")
            
            ev.addWidget(v_lbl)
            ev.addWidget(t_lbl)
            self.entries_layout.addWidget(entry_container)
        self.entries_layout.addStretch()

    def update_image(self, shiny):
        url = self.current_data.get('shiny_sprite' if shiny else 'sprite')
        
        # Fallback to base species sprite if variety lacks its own
        if not url:
            base_name = self.current_data.get('evolution', [self.current_name])[0]
            # Try to find a 'default' form of the same ID (species base)
            for k, v in self.pokemon_data.items():
                if v.get('id') == self.current_data.get('id') and '-' not in k:
                    url = v.get('shiny_sprite' if shiny else 'sprite')
                    break

        self.image_label.clear()
        self.image_label.setText("Loading...")
        if url:
            self.loader = ImageLoader(url)
            self.loader.loaded.connect(self.set_image)
            self.loader.start()
        else:
            self.image_label.setText("No Image")

    def jump_to_pokemon(self, name):
        # Format must match populate_list: f"#{id} {Title Case Name}"
        pid = self.pokemon_data.get(name, {}).get('id', '000')
        display_name = name.replace("-", " ").title()
        search_str = f"#{pid} {display_name}"
        
        items = self.list_widget.findItems(search_str, Qt.MatchFlag.MatchExactly)
        if items:
            self.list_widget.setCurrentItem(items[0])
        else:
            # Fallback for name only if ID is missing
            items = self.list_widget.findItems(display_name, Qt.MatchFlag.MatchContains)
            if items:
                self.list_widget.setCurrentItem(items[0])

    def get_stat_color(self, value):
        if value < 60: return "#de4e3e" # Red
        if value < 90: return "#f7d02c" # Yellow
        return "#7ac74c" # Green

    def add_grid_item(self, title, unique_val, row, col, rowspan=1, colspan=1):
        container = QWidget()
        v = QVBoxLayout(container)
        v.setContentsMargins(0,0,0,0)
        
        t = QLabel(title)
        t.setStyleSheet("color: #777; font-size: 12px; font-weight: bold; text-transform: uppercase;")
        
        val = QLabel(str(unique_val))
        val.setStyleSheet("color: white; font-size: 16px;")
        val.setWordWrap(True)
        
        v.addWidget(t)
        v.addWidget(val)
        
        self.grid_layout.addWidget(container, row, col, rowspan, colspan)

    def set_image(self, qimage):
        pixmap = QPixmap.fromImage(qimage)
        scaled = pixmap.scaled(250, 250, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        self.image_label.setPixmap(scaled)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Global Style
    app.setStyle("Fusion")
    
    window = PokedexWindow()
    window.show()
    sys.exit(app.exec())

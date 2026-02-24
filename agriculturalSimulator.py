#articolul 1: The effect of crop rotation on the soil biological activity 2021 by S.A.Zamyain | R.B. Maksimova
#artcolul 2: Influence of climatic factors and fertilization systems on grain crop yields Y.N. Ankudovich 


#articol 2
#a avut ca scop principal evaluarea modului în care condițiile meteorologice și tipurile de îngrășăminte influențează producția de cereale, respectiv orz, secară de toamnă, grâu și ovăz.
#3 scenarii de fertilizare:
#Fond natural (martor), unde nu s-au aplicat îngrășăminte;
#Fond organic, unde s-a utilizat gunoi de grajd;
#Fond mineral, unde s-au aplicat îngrășăminte chimice de tip NPK

import pygame
import sys
import matplotlib.pyplot as plt
import random

# ==========================================
# 1. DATE STIINTIFICE SI CONSTANTE (CITATE)
# ==========================================

WIDTH, HEIGHT = 1200, 850
FPS = 60

# --- PALETA DE CULORI EXTINSA ---
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (220, 220, 220)
DARK_GRAY = (100, 100, 100)

# Culori pentru Sol si Plante
COLOR_HEALTHY_MAX = (0, 100, 0)     # Verde Inchis (Fertilizat + Vreme Buna)
COLOR_HEALTHY_MID = (34, 139, 34)   # Verde Mediu (Standard)
COLOR_HEALTHY_PALE = (144, 238, 144)# Verde Pal (Nefertilizat / Slab)

COLOR_STRESSED = (218, 165, 32)     # Galben (Seceta)
COLOR_DEAD = (80, 50, 20)           # Maro Inchis (Sol Epuizat)
COLOR_FERTILE_SOIL = (139, 69, 19)  # Maro Roscat (Sol cu Organic activ)

HIGHLIGHT = (255, 215, 0)       
RED = (200, 50, 50)             
BLUE_PROGRESS = (50, 50, 200)

# --- DATE METEOROLOGICE (ARTICOL 2) ---
MONTHLY_MEANS = {
    0: {"name": "Mai",    "temp": 8.2,  "precip": 50},
    1: {"name": "Iunie",  "temp": 15.9, "precip": 58}, 
    2: {"name": "Iulie",  "temp": 18.3, "precip": 74},
    3: {"name": "August", "temp": 15.0, "precip": 74}
}

# --- CULTURI (ARTICOL 2 & 1) ---
CROP_DATA = {
    "Grau": {"base_yield": 16.2}, 
    "Orz":  {"base_yield": 14.4},
    "Ovaz": {"base_yield": 15.0},
    "Cartofi": {"base_yield": 150.0},
    "Parloagă": {"base_yield": 0.0}   
}

# --- FERTILIZARE (ARTICOL 1 & 2) ---
FERTILIZER_RULES = {
    "Niciunul (Martor)": {
        "bonus_yield": 0, 
        "bio_activity_bonus": 0,
        "cooldown": 0
    },
    "Mineral (NPK60)": {
        "bonus_yield": 8.0,        # [Art 2] Impact major randament
        "bio_activity_bonus": 10,  
        "cooldown": 0              
    },
    "Organic (Gunoi)": {
        "bonus_yield": 3.0,        
        "bio_activity_bonus": 35,  # [Art 1] Impact major biologie/sol
        "cooldown": 4              # [Art 2] 1 data pe rotatie
    }
}

# =======================
# 2. LOGICA SIMULARII
# =======================

class SimulationState:
    def __init__(self, total_years=10):
        self.current_year = 1
        self.total_years = total_years
        self.game_over = False
        self.phase = "PLANNING" 
        self.current_month_index = 0 
        
        # Date pentru grafic
        self.history_data = {0: [], 1: [], 2: [], 3: []} 
        self.history_details = {0: [], 1: [], 2: [], 3: []} 

        # Generare Climat
        self.weather_profiles = []
        for _ in range(total_years + 2):
            rnd = random.random()
            if rnd < 0.25: profile = "Secetos" 
            elif rnd < 0.60: profile = "Umed"    
            else: profile = "Normal"
            self.weather_profiles.append(profile)

    def get_current_weather_profile(self):
        return self.weather_profiles[self.current_year - 1]

    def get_month_weather(self, month_idx):
        base = MONTHLY_MEANS[month_idx]
        profile = self.get_current_weather_profile()
        temp = base["temp"]
        precip = base["precip"]
        
        if profile == "Secetos":
            temp += 2.0; precip *= 0.6
        elif profile == "Umed":
            temp -= 1.0; precip *= 1.4
            
        return {"temp": temp, "precip": precip, "profile": profile}

    def advance_month(self, parcels):
        if self.current_month_index < 3:
            self.current_month_index += 1
            current_weather = self.get_month_weather(self.current_month_index)
            for p in parcels:
                p.update_visuals(self.current_month_index, current_weather)
        else:
            self.finalize_year(parcels)

    def start_simulation_year(self, parcels):
        self.phase = "SIMULATING"
        self.current_month_index = 0
        current_weather = self.get_month_weather(0) 
        for p in parcels:
            p.update_visuals(0, current_weather)

    def finalize_year(self, parcels):
        weather_profile = self.get_current_weather_profile()
        
        for p in parcels:
            # 1. Calcul rezultate
            final_yield = p.calculate_final_yield(weather_profile)
            self.history_data[p.index].append(final_yield)
            
            details = {
                "year": self.current_year,
                "crop": p.planted_crop,
                "fertilizer": p.fertilizer,
                "weather": weather_profile,
                "yield": final_yield
            }
            self.history_details[p.index].append(details)
            
            # 2. Gestionare Cooldown
            if p.fertilizer == "Organic (Gunoi)":
                p.organic_cooldown = 4
            elif p.organic_cooldown > 0:
                p.organic_cooldown -= 1
            
            # 3. Pregatire an viitor
            p.fertilizer = "Niciunul (Martor)"
            
            # Resetare vizuala bazata pe starea solului
            if p.organic_cooldown > 0:
                p.color = COLOR_FERTILE_SOIL # Sol Fertil
                p.current_visual_health = 20 # Start cu avantaj
            else:
                p.color = COLOR_DEAD # Sol Epuizat
                p.current_visual_health = 0

        self.phase = "PLANNING"
        self.current_year += 1
        if self.current_year > self.total_years:
            self.game_over = True

class Parcel:
    def __init__(self, x, y, size, index):
        self.rect = pygame.Rect(x, y, size, size)
        self.index = index
        self.planted_crop = "Parloagă"
        self.fertilizer = "Niciunul (Martor)"
        self.organic_cooldown = 0
        self.color = COLOR_DEAD
        self.current_visual_health = 0 

    def update_visuals(self, month_idx, weather):
        if self.planted_crop == "Parloagă":
            self.color = COLOR_FERTILE_SOIL if self.organic_cooldown > 0 else COLOR_DEAD
            return

        # --- LOGICA NOUA PENTRU CULOARE (GRADIENT MAI DETALIAT) ---
        
        # 1. Crestere de baza: Max 75 puncte in August (fara fertilizare)
        # Astfel, fara fertilizare nu atingi niciodata 100 (Verde Inchis)
        growth_stage = (month_idx + 1) * 18.75 
        
        # 2. Factor Meteo
        gtk = weather["precip"] / (weather["temp"] * 3.0 + 0.1)
        weather_stress = 0
        if gtk < 0.8: weather_stress = 35 # Seceta vizibila
        elif gtk > 1.8: weather_stress = 10
            
        # 3. Fertilizare
        fert_bonus = FERTILIZER_RULES[self.fertilizer]["bio_activity_bonus"]
        
        # 4. Istoric Organic
        history_bonus = 0
        if self.organic_cooldown > 0 and self.fertilizer != "Organic (Gunoi)":
             history_bonus = 15 
        
        # Total Sanatate (0 - 100+)
        health = growth_stage + fert_bonus + history_bonus - weather_stress
        
        # Plafonare
        health = max(0, min(health, 100))
        self.current_visual_health = health
        
        # INTERPOLARE CULOARE
        # 0-30: Maro -> Galben (Rasarire sau Moarte)
        # 30-70: Galben -> Verde Pal (Creștere medie)
        # 70-100: Verde Pal -> Verde Inchis (Maturitate deplina)
        
        if health < 30:
            ratio = health / 30
            c1 = COLOR_FERTILE_SOIL if (self.organic_cooldown > 0 or "Organic" in self.fertilizer) else COLOR_DEAD
            c2 = COLOR_STRESSED
            self.color = self.interpolate(c1, c2, ratio)
            
        elif health < 70:
            ratio = (health - 30) / 40
            c1 = COLOR_STRESSED
            c2 = COLOR_HEALTHY_PALE # Verde deschis
            self.color = self.interpolate(c1, c2, ratio)
            
        else: # 70 - 100
            ratio = (health - 70) / 30
            c1 = COLOR_HEALTHY_PALE
            c2 = COLOR_HEALTHY_MAX # Verde saturat (doar pt fertilizati)
            self.color = self.interpolate(c1, c2, ratio)

    def interpolate(self, c1, c2, ratio):
        r = int(c1[0] * (1-ratio) + c2[0] * ratio)
        g = int(c1[1] * (1-ratio) + c2[1] * ratio)
        b = int(c1[2] * (1-ratio) + c2[2] * ratio)
        return (r, g, b)

    def calculate_final_yield(self, weather_profile):
        base = CROP_DATA[self.planted_crop]["base_yield"]
        bonus = FERTILIZER_RULES[self.fertilizer]["bonus_yield"]
        
        history_yield = 0
        if self.organic_cooldown > 0 and self.fertilizer == "Niciunul (Martor)":
            history_yield = 1.5 

        climate_factor = 1.0
        if weather_profile == "Secetos":
            climate_factor = 0.6 
            if self.fertilizer == "Organic (Gunoi)" or self.organic_cooldown > 0:
                climate_factor = 0.75 
        elif weather_profile == "Umed":
            climate_factor = 0.9 
        else:
            climate_factor = 1.1

        return (base + bonus + history_yield) * climate_factor

# =======================
# 3. INTERFATA SI LOGICA BULEI
# =======================

def draw_interface(screen, sim_state, parcels, selected_idx):
    screen.fill(WHITE)
    
    # Header
    pygame.draw.rect(screen, (240, 248, 255), (0, 0, WIDTH, 160))
    year_txt = f"ANUL: {sim_state.current_year} / {sim_state.total_years}"
    
    status_txt = "PLANIFICARE (Alege culturile)"
    month_info = ""
    
    if sim_state.phase == "SIMULATING":
        m_idx = sim_state.current_month_index
        m_data = sim_state.get_month_weather(m_idx)
        m_name = MONTHLY_MEANS[m_idx]["name"].upper()
        status_txt = f"LUNA: {m_name}"
        month_info = f"Meteo: {m_data['temp']:.1f}C | Precip: {m_data['precip']:.0f}mm ({m_data['profile']})"
    
    font_large = pygame.font.SysFont("Arial", 28)
    font_med = pygame.font.SysFont("Arial", 20)
    font_small = pygame.font.SysFont("Arial", 16)

    draw_text(screen, year_txt, 50, 20, font_large)
    draw_text(screen, status_txt, 50, 60, font_large, BLUE_PROGRESS)
    draw_text(screen, month_info, 50, 100, font_med)
    
    msg = "Apasa [ENTER] pentru a incepe anul" if sim_state.phase == "PLANNING" else "Apasa [SPACE] pentru Luna Urmatoare"
    draw_text(screen, msg, 50, 130, font_small, RED)

    # Parcele
    for p in parcels:
        pygame.draw.rect(screen, p.color, p.rect)
        th = 4 if p.index == selected_idx else 2
        col_b = RED if p.index == selected_idx else BLACK
        pygame.draw.rect(screen, col_b, p.rect, th)
        
        txt_col = WHITE if sum(p.color)<350 else BLACK
        draw_text(screen, f"P{p.index+1}: {p.planted_crop}", p.rect.x+10, p.rect.y+10, font_med, txt_col)
        
        # --- LOGICA TEXT ETICHETA SOL (FIXATA) ---
        label_sol = "Standard"
        if "Organic" in p.fertilizer:
            label_sol = "Organic (Activ)"
        elif "Mineral" in p.fertilizer:
            label_sol = "Mineral (Activ)"
        elif p.organic_cooldown > 0:
            label_sol = f"Remanent Org. ({p.organic_cooldown} ani)"
        elif p.planted_crop == "Parloagă":
             label_sol = "Odihna"
        else:
             label_sol = "Nefertilizat/Epuizat"
             
        draw_text(screen, label_sol, p.rect.x+10, p.rect.bottom-25, font_small, txt_col)

    # UI Configurare
    UI_X = 600
    if selected_idx is not None and sim_state.phase == "PLANNING":
        p = parcels[selected_idx]
        draw_text(screen, f"Configurare Parcela {p.index+1}", UI_X, 170, font_large)
        
        # Cultura
        draw_text(screen, "Cultura:", UI_X, 200, font_med)
        c_c, c_r = 0, 0
        for cr in CROP_DATA.keys():
            rr = pygame.Rect(UI_X+c_c*110, 230+c_r*40, 100, 30)
            col = HIGHLIGHT if p.planted_crop==cr else WHITE
            pygame.draw.rect(screen, col, rr); pygame.draw.rect(screen, BLACK, rr, 2)
            draw_text(screen, cr, rr.x+5, rr.y+5, font_small)
            c_c+=1; 
            if c_c>2: c_c=0; c_r+=1

        # Fertilizare
        draw_text(screen, "Fertilizare:", UI_X, 380, font_med)
        yy = 410
        for fert, rul in FERTILIZER_RULES.items():
            blocked = ("Organic" in fert and p.organic_cooldown > 0)
            rr = pygame.Rect(UI_X, yy, 300, 30)
            col = GRAY if blocked else (HIGHLIGHT if p.fertilizer==fert else WHITE)
            pygame.draw.rect(screen, col, rr); pygame.draw.rect(screen, BLACK, rr, 2)
            txt = fert + (f" (Blocat)" if blocked else "")
            draw_text(screen, txt, rr.x+10, rr.y+5, font_small, DARK_GRAY if blocked else BLACK)
            yy+=45
    
    # Legenda
    ly = HEIGHT - 40
    lg_items = [
        (COLOR_HEALTHY_MAX, "Sanatos Max"),
        (COLOR_HEALTHY_PALE, "Sanatos Mediu"),
        (COLOR_STRESSED, "Stres/Seceta"),
        (COLOR_FERTILE_SOIL, "Sol Fertil"),
        (COLOR_DEAD, "Epuizat")
    ]
    lx = 50
    for col, txt in lg_items:
        pygame.draw.rect(screen, col, (lx, ly, 20, 20))
        draw_text(screen, txt, lx+25, ly, font_small)
        lx += 150

def draw_text(surf, txt, x, y, font, col=BLACK):
    surf.blit(font.render(txt, True, col), (x, y))

# =======================
# 4. FUNCTIA GRAFIC FINAL
# =======================

def show_final_graph(sim_state):
    print("Se genereaza graficul...")
    fig, ax = plt.subplots(figsize=(10,6))
    ax.set_title("Evoluția Randamentului Agricol (Anual) - Studiu Narym", fontsize=14)
    ax.set_xlabel("Ani")
    ax.set_ylabel("Randament (q/ha) [Articol 2]")
    ax.grid(True, linestyle='--', alpha=0.5)
    
    years = list(range(1, sim_state.total_years+1))
    lines = []
    
    # Culori linii grafic
    colors = ['green', 'blue', 'red', 'orange']
    
    for i, data in sim_state.history_data.items():
        l, = ax.plot(years, data, marker='o', label=f"Parcela {i+1}", color=colors[i], picker=True, pickradius=5)
        lines.append(l)
    
    ax.legend()
    
    annot = ax.annotate("", xy=(0,0), xytext=(20,20), textcoords="offset points",
                        bbox=dict(boxstyle="round", fc="w"), arrowprops=dict(arrowstyle="->"))
    annot.set_visible(False)
    
    def hover(event):
        if event.inaxes == ax:
            found = False
            txt = ""
            for line in lines:
                cont, ind = line.contains(event)
                if cont:
                    idx = ind["ind"][0]
                    pidx = lines.index(line)
                    annot.xy = (line.get_data()[0][idx], line.get_data()[1][idx])
                    try:
                        d = sim_state.history_details[pidx][idx]
                        txt += (f"PARCELA {pidx+1} | ANUL {d['year']}\n"
                                f"Vreme: {d['weather']}\n"
                                f"Cultura: {d['crop']}\n"
                                f"Fertilizare: {d['fertilizer']}\n"
                                f"Randament: {d['yield']:.1f} q/ha\n\n")
                        found = True
                    except: pass
            if found:
                annot.set_text(txt.strip())
                annot.set_visible(True)
            else:
                annot.set_visible(False)
            fig.canvas.draw_idle()

    fig.canvas.mpl_connect("motion_notify_event", hover)
    plt.show()

# =======================
# 5. MAIN
# =======================

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Simulare Agricola Corecta")
    clock = pygame.time.Clock()
    
    # Input Ani
    font_big = pygame.font.SysFont("Arial", 32)
    input_text = "5"
    input_active = True
    sim_state = None
    
    # Grid
    parcels = []
    GRID_X, GRID_Y = 50, 200
    CELL_SIZE = 220
    GAP = 20
    for i in range(4):
        r, c = i // 2, i % 2
        parcels.append(Parcel(GRID_X + c*(CELL_SIZE+GAP), GRID_Y + r*(CELL_SIZE+GAP), CELL_SIZE, i))
    
    selected_parcel_index = None
    
    running = True
    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
                
            if input_active:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        try:
                            y = int(input_text)
                            if y > 0: sim_state = SimulationState(y); input_active = False
                        except: pass
                    elif event.key == pygame.K_BACKSPACE: input_text = input_text[:-1]
                    else: 
                        if event.unicode.isdigit(): input_text += event.unicode
            
            elif sim_state and not sim_state.game_over:
                if event.type == pygame.KEYDOWN:
                    if sim_state.phase == "PLANNING" and event.key == pygame.K_RETURN:
                        sim_state.start_simulation_year(parcels)
                    elif sim_state.phase == "SIMULATING" and event.key == pygame.K_SPACE:
                        sim_state.advance_month(parcels)
                
                if event.type == pygame.MOUSEBUTTONDOWN and sim_state.phase == "PLANNING":
                    mx, my = pygame.mouse.get_pos()
                    for p in parcels:
                        if p.rect.collidepoint(mx, my): selected_parcel_index = p.index
                    
                    # Logica Click Butoane
                    UI_X = 600
                    if selected_parcel_index is not None:
                        curr = parcels[selected_parcel_index]
                        # Click Cultura
                        cc, cr = 0, 0
                        for crop in CROP_DATA.keys():
                            r = pygame.Rect(UI_X+cc*110, 230+cr*40, 100, 30)
                            if r.collidepoint(mx, my): curr.planted_crop = crop
                            cc+=1; 
                            if cc>2: cc=0; cr+=1
                        # Click Fert
                        yy = 410
                        for fert in FERTILIZER_RULES.keys():
                            r = pygame.Rect(UI_X, yy, 300, 30)
                            blocked = ("Organic" in fert and curr.organic_cooldown > 0)
                            if r.collidepoint(mx, my) and not blocked:
                                curr.fertilizer = fert
                            yy+=45
        
        # Check Game Over
        if sim_state and sim_state.game_over:
            running = False # Iesim din bucla Pygame
        
        # Drawing
        if input_active:
            screen.fill(WHITE)
            txt = font_big.render("Introdu numar ani: " + input_text, True, BLACK)
            screen.blit(txt, (WIDTH//2 - 150, HEIGHT//2))
        elif sim_state:
            draw_interface(screen, sim_state, parcels, selected_parcel_index)
            
        pygame.display.flip()
        clock.tick(FPS)

    # Iesire curata Pygame
    pygame.quit()
    
    # Afisare Grafic (DOAR DACA SIMULAREA S-A TERMINAT COMPLET)
    if sim_state and sim_state.game_over:
        show_final_graph(sim_state)
    
    sys.exit()

if __name__ == "__main__":
    main()
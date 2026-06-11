import streamlit as st
from conn import HeroeRepo, TesoroRepo, MazmorrasRepo, Heroe, Tesoro

st.set_page_config(
    page_title="D&D Manager",
    page_icon="⚔️",
    layout="wide",
)

st.markdown("""
<style>
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(160deg, #0d0500 0%, #1e0a00 60%, #0d0500 100%);
        color: #f0e6d3;
    }
    [data-testid="stHeader"] { background: transparent; }
    section[data-testid="stSidebar"] { display: none; }

    h1, h2, h3 { color: #D4AF37 !important; font-family: serif; }

    [data-testid="metric-container"] {
        background: rgba(212,175,55,0.08);
        border: 1px solid #8B6914;
        border-radius: 10px;
        padding: 16px;
    }
    [data-testid="stMetricValue"] { color: #D4AF37 !important; font-size: 2em !important; }
    [data-testid="stMetricLabel"] { color: #c0a860 !important; }

    .stTabs [data-baseweb="tab-list"] {
        background: rgba(0,0,0,0.4);
        border-radius: 10px;
        gap: 4px;
        padding: 4px;
    }
    .stTabs [data-baseweb="tab"] {
        color: #c0a860 !important;
        font-size: 15px;
        font-weight: 600;
        border-radius: 8px;
        padding: 8px 20px;
    }
    .stTabs [aria-selected="true"] {
        background: rgba(212,175,55,0.15) !important;
        color: #FFD700 !important;
        border-bottom: 2px solid #D4AF37 !important;
    }

    .stButton > button {
        background: linear-gradient(135deg, #6B0000, #8B0000);
        color: #f0e6d3;
        border: 1px solid #D4AF37;
        border-radius: 6px;
        font-weight: bold;
        width: 100%;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #8B0000, #B22222);
        border-color: #FFD700;
        color: #FFD700;
    }

    .stTextInput input, .stNumberInput input {
        background: #150800 !important;
        color: #f0e6d3 !important;
        border: 1px solid #8B6914 !important;
        border-radius: 6px !important;
    }
    .stSelectbox > div > div {
        background: #150800 !important;
        color: #f0e6d3 !important;
        border: 1px solid #8B6914 !important;
    }
    .stSlider > div > div > div { background: #D4AF37 !important; }

    [data-testid="stForm"] {
        background: rgba(212,175,55,0.04);
        border: 1px solid #3a2500;
        border-radius: 12px;
        padding: 16px;
    }
    .stFormSubmitButton > button {
        background: linear-gradient(135deg, #1a5c1a, #228B22) !important;
        border-color: #90EE90 !important;
    }
    .stFormSubmitButton > button:hover {
        background: linear-gradient(135deg, #228B22, #32CD32) !important;
    }

    .card {
        background: rgba(255,255,255,0.04);
        border-radius: 10px;
        padding: 14px 16px;
        margin: 8px 0;
        transition: border 0.2s;
    }
    .card-title { font-size: 1.05em; font-weight: bold; }
    .card-sub { font-size: 0.82em; color: #c0a860; margin-top: 4px; }

    .badge {
        display: inline-block;
        padding: 2px 10px;
        border-radius: 12px;
        font-size: 11px;
        font-weight: bold;
        margin: 0 2px;
    }
    .divider { border: none; border-top: 1px solid #3a2500; margin: 20px 0; }

    [data-testid="stInfo"], [data-testid="stWarning"], [data-testid="stSuccess"], [data-testid="stError"] {
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)

heroes_repo    = HeroeRepo()
tesoros_repo   = TesoroRepo()
mazmorras_repo = MazmorrasRepo()

CLASE_COLOR  = {"Guerrero":"#DC143C", "Mago":"#9B59B6", "Clérigo":"#E8C84A", "Pícaro":"#27AE60"}
RAREZA_COLOR = {"Común":"#7F8C8D", "Raro":"#2980B9", "Legendario":"#E67E22"}
CLASE_EMOJI  = {"Guerrero":"⚔️", "Mago":"🔮", "Clérigo":"✨", "Pícaro":"🗡️"}
TIPO_EMOJI   = {"Arma":"⚔️", "Poción":"🧪", "Pergamino":"📜", "Armadura":"🛡️"}

def badge(text, color):
    return f'<span class="badge" style="background:{color};color:#fff">{text}</span>'

def diff_info(d):
    if d <= 5:   return "#27AE60", "Fácil"
    if d <= 10:  return "#F39C12", "Moderada"
    if d <= 15:  return "#E74C3C", "Difícil"
    return "#8B008B", "⚠️ Letal"

st.markdown("""
<div style="text-align:center;padding:24px 0 8px">
    <h1 style="font-size:2.8em;margin:0;letter-spacing:2px">⚔️ &nbsp; D&D Manager &nbsp; ⚔️</h1>
    <p style="color:#8B6914;font-style:italic;font-size:1.05em;margin-top:6px">
    Gestion de datos    </p>
</div>
""", unsafe_allow_html=True)
st.markdown('<hr class="divider">', unsafe_allow_html=True)

heroes_all    = heroes_repo.selectAll()
tesoros_all   = tesoros_repo.selectAll()
mazmorras_all = mazmorras_repo.selectAll()
completadas  = sum(1 for m in mazmorras_all if m[4] == 1)

c1, c2, c3, c4 = st.columns(4)
c1.metric("🧙 Héroes",      len(heroes_all))
c2.metric("💎 Tesoros",     len(tesoros_all))
c3.metric("🗺️ Mazmorras",   len(mazmorras_all))
c4.metric("✅ Completadas", f"{completadas}/{len(mazmorras_all)}")

st.markdown('<hr class="divider">', unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["🧙 Salón de Héroes", "💎 Cofre del Tesoro", "🗺️ Mapa de Mazmorras"])


with tab1:
    st.markdown("## 🧙 Salón de Héroes")
    col_lista, col_form = st.columns([3, 2], gap="large")

    with col_lista:
        st.markdown("#### Aventureros registrados")
        clases_opt = ["Todos", "Guerrero", "Mago", "Clérigo", "Pícaro"]
        filtro = st.selectbox("Filtrar por clase", clases_opt, key="f_clase")
        heroes = heroes_repo.selectAll(None if filtro == "Todos" else filtro)

        if not heroes:
            st.info("No hay héroes registrados con ese filtro.")
        else:
            for h in heroes:
                color  = CLASE_COLOR.get(h.clase, "#888")
                emoji  = CLASE_EMOJI.get(h.clase, "🧑")
                bonus  = round(h.nivel * 0.2, 1)
                st.markdown(f"""
                <div class="card" style="border-left:4px solid {color}">
                    <div class="card-title">{emoji} &nbsp;
                        <span style="color:{color}">#{h.id} {h.nombre}</span>
                        &nbsp;{badge(h.clase, color)}&nbsp;{badge(h.raza, "#555")}
                    </div>
                    <div class="card-sub">
                        ⚡ Nivel {h.nivel} &nbsp;·&nbsp; 🎯 Bonif. ataque: +{bonus}
                    </div>
                </div>
                """, unsafe_allow_html=True)

    with col_form:
        st.markdown("#### Reclutar aventurero")
        with st.form("form_heroe", clear_on_submit=True):
            nombre_h = st.text_input("Nombre del héroe")
            clase_h  = st.selectbox("Clase", ["Guerrero", "Mago", "Clérigo", "Pícaro"])
            raza_h   = st.selectbox("Raza", ["Humano", "Elfo", "Enano", "Mediano"])
            nivel_h  = st.number_input("Nivel (1-20)", min_value=1, max_value=20, value=1)
            if st.form_submit_button("⚔️ Reclutar"):
                if not nombre_h.strip():
                    st.error("El nombre no puede estar vacío.")
                else:
                    heroes_repo.create(Heroe(nombre=nombre_h.strip(), nivel=nivel_h, clase=clase_h, raza=raza_h, id=None))
                    st.success(f"¡{nombre_h} se unió a la Hermandad!")
                    st.rerun()

        st.markdown('<hr class="divider">', unsafe_allow_html=True)
        st.markdown("#### Editar aventurero")
        if heroes_all:
            opts_edit = {f"#{h.id}  {h.nombre}  ({h.clase})": h for h in heroes_all}
            sel_edit  = st.selectbox("Seleccionar héroe", list(opts_edit.keys()), key="sel_edit_h")
            h_edit    = opts_edit[sel_edit]
            with st.form("form_editar_heroe"):
                nuevo_nombre = st.text_input("Nombre", value=h_edit.nombre)
                nueva_clase  = st.selectbox("Clase", ["Guerrero", "Mago", "Clérigo", "Pícaro"],
                                            index=["Guerrero", "Mago", "Clérigo", "Pícaro"].index(h_edit.clase)
                                            if h_edit.clase in ["Guerrero", "Mago", "Clérigo", "Pícaro"] else 0)
                nueva_raza   = st.selectbox("Raza", ["Humano", "Elfo", "Enano", "Mediano"],
                                            index=["Humano", "Elfo", "Enano", "Mediano"].index(h_edit.raza)
                                            if h_edit.raza in ["Humano", "Elfo", "Enano", "Mediano"] else 0)
                nuevo_nivel  = st.number_input("Nivel (1-20)", min_value=1, max_value=20, value=h_edit.nivel)
                if st.form_submit_button("💾 Guardar cambios"):
                    if not nuevo_nombre.strip():
                        st.error("El nombre no puede estar vacío.")
                    else:
                        heroes_repo.update(Heroe(nombre=nuevo_nombre.strip(), nivel=nuevo_nivel,
                                                 clase=nueva_clase, raza=nueva_raza, id=h_edit.id))
                        st.success(f"¡{nuevo_nombre} actualizado!")
                        st.rerun()
        else:
            st.info("No hay héroes para editar.")

        st.markdown('<hr class="divider">', unsafe_allow_html=True)
        st.markdown("#### Retirar aventurero")
        if heroes_all:
            opts_h = {f"#{h.id}  {h.nombre}  ({h.clase})": h.id for h in heroes_all}
            sel_h  = st.selectbox("Seleccionar héroe", list(opts_h.keys()), key="sel_del_h")
            if st.button("🗑️ Retirar de la Hermandad", key="btn_del_h"):
                heroes_repo.delete(opts_h[sel_h])
                st.warning(f"{sel_h} retirado.")
                st.rerun()
        else:
            st.info("No hay héroes para retirar.")



with tab2:
    st.markdown("## 💎 Cofre del Tesoro")
    col_inv, col_tform = st.columns([3, 2], gap="large")

    with col_inv:
        st.markdown("#### Inventario de la Hermandad")
        rareza_opt = ["Todos", "Común", "Raro", "Legendario"]
        filtro_r   = st.selectbox("Filtrar por rareza", rareza_opt, key="f_rareza")
        tesoros    = tesoros_repo.selectAll(None if filtro_r == "Todos" else filtro_r)

        if not tesoros:
            st.info("El cofre está vacío.")
        else:
            for t in tesoros:
                tid, nombre_item, tipo, rareza, portador = t
                color = RAREZA_COLOR.get(rareza, "#888")
                emoji = TIPO_EMOJI.get(tipo, "🎁")
                st.markdown(f"""
                <div class="card" style="border-left:4px solid {color}">
                    <div class="card-title">{emoji} &nbsp;
                        <span style="color:{color}">#{tid} {nombre_item}</span>
                        &nbsp;{badge(rareza, color)}&nbsp;{badge(tipo, "#444")}
                    </div>
                    <div class="card-sub">👤 Portador: {portador}</div>
                </div>
                """, unsafe_allow_html=True)

    with col_tform:
        st.markdown("#### Agregar ítem al cofre")
        heroes_for_t = heroes_repo.selectAll()
        hero_map = {"— Sin propietario —": None}
        hero_map.update({f"#{h.id} {h.nombre}": h.id for h in heroes_for_t})

        with st.form("form_tesoro", clear_on_submit=True):
            nombre_t  = st.text_input("Nombre del ítem")
            tipo_t    = st.selectbox("Tipo", ["Arma", "Poción", "Pergamino", "Armadura"])
            rareza_t  = st.selectbox("Rareza", ["Común", "Raro", "Legendario"])
            prop_t    = st.selectbox("Propietario", list(hero_map.keys()))
            if st.form_submit_button("💎 Añadir al cofre"):
                if not nombre_t.strip():
                    st.error("El nombre del ítem no puede estar vacío.")
                else:
                    tesoros_repo.create(Tesoro(nombre_item=nombre_t.strip(), tipo=tipo_t, rareza=rareza_t), hero_map[prop_t])
                    st.success(f"¡{nombre_t} guardado en el cofre!")
                    st.rerun()

        st.markdown('<hr class="divider">', unsafe_allow_html=True)
        st.markdown("#### Quitar ítem")
        tesoros_fresh = tesoros_repo.selectAll()
        if tesoros_fresh:
            opts_t = {f"#{t[0]} {t[1]}  [{t[3]}]": t[0] for t in tesoros_fresh}
            sel_t  = st.selectbox("Seleccionar ítem", list(opts_t.keys()), key="sel_del_t")
            if st.button("🗑️ Retirar del cofre", key="btn_del_t"):
                tesoros_repo.delete(opts_t[sel_t])
                st.warning(f"{sel_t} removido.")
                st.rerun()
        else:
            st.info("No hay ítems para quitar.")



with tab3:
    st.markdown("## 🗺️ Mapa de Mazmorras")
    col_maz, col_mform = st.columns([3, 2], gap="large")

    with col_maz:
        st.markdown("#### Mazmorras descubiertas")
        mazmorras = mazmorras_repo.selectAll()

        if not mazmorras:
            st.info("No hay mazmorras registradas aún.")
        else:
            for m in mazmorras:
                mid, nombre_lugar, dificultad, enemigo_final, fue_completada = m
                color, label = diff_info(dificultad)
                border = "#27AE60" if fue_completada else color
                estado_txt = "✅ Completada" if fue_completada else "🔴 Pendiente"

                st.markdown(f"""
                <div class="card" style="border-left:4px solid {border}">
                    <div class="card-title">🏰 &nbsp;
                        <span style="color:{border}">#{mid} {nombre_lugar}</span>
                        &nbsp;{badge(label, color)}&nbsp;{badge(f"Niv. {dificultad}", "#333")}
                    </div>
                    <div class="card-sub">
                        👹 Jefe final: {enemigo_final} &nbsp;·&nbsp; {estado_txt}
                    </div>
                </div>
                """, unsafe_allow_html=True)

                b1, b2, b3 = st.columns(3)
                if not fue_completada:
                    if b1.button("✅ Completar", key=f"comp_{mid}"):
                        mazmorras_repo.toggleCompletada(mid, 1)
                        for h in heroes_repo.selectAll():
                            heroes_repo.subirNivel(h.id, 1)
                        st.success(f"¡Mazmorra completada! Todos los héroes subieron 1 nivel.")
                        st.rerun()
                else:
                    if b1.button("🔄 Pendiente", key=f"pend_{mid}"):
                        mazmorras_repo.toggleCompletada(mid, 0)
                        st.rerun()
                if b2.button("⬆️ +Nivel", key=f"lvl_{mid}", help="Subir 1 nivel a todos por esta mazmorra"):
                    for h in heroes_repo.selectAll():
                        heroes_repo.subirNivel(h.id, 1)
                    st.success("¡Todos los héroes subieron 1 nivel!")
                    st.rerun()
                if b3.button("🗑️ Eliminar", key=f"del_m_{mid}"):
                    mazmorras_repo.delete(mid)
                    st.rerun()

    with col_mform:
        st.markdown("#### Registrar nueva mazmorra")
        with st.form("form_maz", clear_on_submit=True):
            nombre_m    = st.text_input("Nombre del lugar")
            dificultad_m = st.slider("Dificultad", min_value=1, max_value=20, value=5)
            color_prev, label_prev = diff_info(dificultad_m)
            st.markdown(f'<small>Nivel: {badge(label_prev, color_prev)}</small>', unsafe_allow_html=True)
            enemigo_m   = st.text_input("Enemigo final")
            if st.form_submit_button("🗺️ Registrar mazmorra"):
                if not nombre_m.strip() or not enemigo_m.strip():
                    st.error("Nombre y enemigo final son obligatorios.")
                else:
                    mazmorras_repo.create(nombre_m.strip(), dificultad_m, enemigo_m.strip())
                    st.success(f"¡{nombre_m} añadida al mapa!")
                    st.rerun()

        st.markdown('<hr class="divider">', unsafe_allow_html=True)
        st.markdown("#### Leyenda de dificultad")
        st.markdown(f"""
        <div style="font-size:0.88em;line-height:2">
            {badge("1–5  · Fácil",    "#27AE60")} nivel de entrada<br>
            {badge("6–10 · Moderada", "#F39C12")} requiere preparación<br>
            {badge("11–15· Difícil",  "#E74C3C")} héroes experimentados<br>
            {badge("16–20· Letal",    "#8B008B")} ⚠️ mortal
        </div>
        """, unsafe_allow_html=True)

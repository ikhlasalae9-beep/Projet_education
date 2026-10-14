import json
import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import plotly.graph_objects as go

# ==============================================================================
# 1. CONFIGURATION DE LA PAGE & DESIGN SYSTEM (DARK NAVY POWER BI)
# ==============================================================================
st.set_page_config(
    page_title="CPGE Maroc - Analyse Territoriale et Capacitaire",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', 'Segoe UI', sans-serif;
}
.stApp {
    background-color: #061325;
    color: #F1F5F9;
}
header[data-testid="stHeader"] {
    display: none !important;
}
div[data-testid="stToolbar"] {
    display: none !important;
}
.block-container {
    padding-top: 1.6rem !important;
    padding-bottom: 1.5rem !important;
    max-width: 98% !important;
}

/* Style unifié des conteneurs st.container(border=True) */
div[data-testid="stVerticalBlockBorderWrapper"] {
    background-color: #0C213B !important;
    border: 1px solid #16365F !important;
    border-radius: 12px !important;
    padding: 14px 16px !important;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.32) !important;
}

/* Style propre et épuré des filtres (Selectbox & Text Input) */
div[data-baseweb="select"] > div {
    background-color: #091930 !important;
    border: 1px solid #1E4976 !important;
    border-radius: 8px !important;
    color: #F1F5F9 !important;
    min-height: 38px !important;
}
div[data-baseweb="select"] > div:hover {
    border-color: #00D4FF !important;
}
div[data-baseweb="input"] > div {
    background-color: #091930 !important;
    border: 1px solid #1E4976 !important;
    border-radius: 8px !important;
    color: #F1F5F9 !important;
    min-height: 38px !important;
}
div[data-testid="stWidgetLabel"] p {
    color: #94A3B8 !important;
    font-size: 0.76rem !important;
    font-weight: 600 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.4px !important;
}

/* Barre supérieure Power BI */
.top-nav {
    background-color: #0C213B;
    border: 1px solid #16365F;
    border-radius: 10px;
    padding: 14px 22px;
    margin-bottom: 12px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    box-shadow: 0 4px 18px rgba(0, 0, 0, 0.35);
}
.top-nav-title {
    color: #00D4FF;
    font-size: 1.3rem;
    font-weight: 700;
    margin: 0;
}
.top-nav-subtitle {
    color: #94A3B8;
    font-size: 0.78rem;
    margin-top: 3px;
}
.nav-pills {
    display: flex;
    gap: 8px;
}
.nav-pill-active {
    background-color: #00D4FF;
    color: #061325;
    font-weight: 600;
    font-size: 0.78rem;
    padding: 6px 14px;
    border-radius: 6px;
}
.nav-pill-outline {
    border: 1px solid #00D4FF;
    color: #00D4FF;
    font-weight: 500;
    font-size: 0.78rem;
    padding: 6px 14px;
    border-radius: 6px;
}

/* Cartes KPI */
.kpi-card {
    background-color: #0C213B;
    border: 1px solid #16365F;
    border-radius: 12px;
    padding: 15px 18px 10px 18px;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3);
    height: 172px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}
.kpi-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.kpi-title {
    color: #FFFFFF;
    font-size: 0.92rem;
    font-weight: 600;
}
.info-badge {
    width: 20px;
    height: 20px;
    border-radius: 50%;
    background-color: rgba(255, 255, 255, 0.12);
    color: #94A3B8;
    font-size: 0.72rem;
    font-weight: 700;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    font-style: italic;
}
.kpi-metrics-row {
    display: flex;
    align-items: baseline;
    gap: 8px;
    margin-top: 4px;
}
.kpi-primary {
    font-size: 1.1rem;
    font-weight: 700;
}
.kpi-divider {
    color: #475569;
    font-size: 0.85rem;
}
.kpi-secondary {
    color: #94A3B8;
    font-size: 0.8rem;
    font-weight: 500;
}
.kpi-delta {
    color: #00E5A3;
    font-size: 0.76rem;
    font-weight: 600;
    margin-top: 2px;
}
.kpi-sparkline {
    width: 100%;
    height: 54px;
    margin-top: 4px;
}

/* En-tête interne de chaque carte visuelle */
.visual-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 6px;
}
.visual-title {
    color: #FFFFFF;
    font-size: 0.95rem;
    font-weight: 600;
    margin: 0;
}
.visual-subtitle {
    color: #94A3B8;
    font-size: 0.74rem;
    margin-top: 2px;
}

/* Tableaux HTML sombres */
.pbi-table-wrap {
    max-height: 310px;
    overflow-y: auto;
    border-radius: 6px;
    margin-top: 6px;
}
.pbi-table-wrap::-webkit-scrollbar {
    width: 5px;
}
.pbi-table-wrap::-webkit-scrollbar-thumb {
    background: #1E4976;
    border-radius: 4px;
}
table.pbi-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 0.78rem;
    color: #E2E8F0;
}
table.pbi-table th {
    background-color: #091930;
    color: #94A3B8;
    font-weight: 600;
    text-align: left;
    padding: 8px 10px;
    border-bottom: 1px solid #1E3A5F;
    position: sticky;
    top: 0;
}
table.pbi-table td {
    padding: 7px 10px;
    border-bottom: 1px solid rgba(30, 58, 95, 0.45);
}
table.pbi-table tr:hover td {
    background-color: rgba(0, 212, 255, 0.08);
}
.num-col {
    text-align: right !important;
    font-variant-numeric: tabular-nums;
}
.highlight-cyan {
    color: #00D4FF;
    font-weight: 600;
}
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 2. CHARGEMENT ET PRÉPARATION DES DONNÉES (BASÉ SUR CPGE.ipynb)
# ==============================================================================
@st.cache_data
def load_data():
    dt = pd.read_csv("etablissements_publics_cpge_juillet-2026_fr.csv")
    dt.drop(columns=["NOM_ETABL", "AdresseL"], inplace=True)
    dt = dt.rename(columns={
        "NOM_ETABA": "nom_etablissement",
        "AdresseA": "adresse",
        "LL_COM": "commune",
        "LL_PROV": "province",
        "LL_REG": "region"
    })

    coords = [
        (30.4218, -9.5830), (33.8966, -5.5413), (33.8820, -5.5265), (32.3394, -6.3498),
        (32.3320, -6.3605), (33.5975, -7.6110), (33.5705, -7.6168), (33.2450, -8.5085),
        (31.9295, -4.4285), (34.0617, -4.9830), (28.9880, -10.0570), (34.2580, -6.5830),
        (32.8855, -6.9060), (32.8790, -6.9125), (27.1500, -13.1990), (31.6155, -8.0370),
        (31.6090, -8.0250), (33.6870, -7.3820), (35.1685, -2.9280), (23.6920, -15.9380),
        (23.7080, -15.9280), (30.9200, -6.9090), (34.6815, -1.9080), (33.9985, -6.8480),
        (34.0165, -6.8325), (32.2990, -9.2370), (34.0450, -6.8030), (33.0010, -7.6160),
        (33.0065, -7.6210), (35.7805, -5.8195), (34.2100, -4.0100), (35.5720, -5.3520),
    ]
    dt["lat"] = [c[0] for c in coords]
    dt["lon"] = [c[1] for c in coords]

    reg_counts = dt["region"].value_counts()
    def classify_pole(reg):
        c = reg_counts.get(reg, 0)
        if c >= 4:
            return "Pôles Majeurs (4 à 6 centres)"
        elif c >= 2:
            return "Pôles Intermédiaires (2 à 3 centres)"
        return "Pôles à Centre Unique (1 centre)"

    dt["pole_categorie"] = dt["region"].apply(classify_pole)
    return dt

dt = load_data()

# ==============================================================================
# 3. EN-TÊTE & BARRE DE FILTRES HORIZONTALE PROPRE (SANS TAGS ROUGES)
# ==============================================================================
st.markdown("""
<div class="top-nav">
<div>
<div class="top-nav-title">Analyse Territoriale et Répartition des Établissements CPGE au Maroc</div>
<div class="top-nav-subtitle">Source : Portail Open Data Maroc (data.gov.ma) | Données Officielles Juillet 2026 | 32 Centres Publics</div>
</div>
<div class="nav-pills">
<span class="nav-pill-active">Synopsis Global</span>
<span class="nav-pill-outline">Analyse Régionale</span>
<span class="nav-pill-outline">Cartographie</span>
</div>
</div>
""", unsafe_allow_html=True)

# Barre de filtres simple et alignée (4 listes déroulantes propres sur 1 seule ligne)
with st.container(border=True):
    f1, f2, f3, f4 = st.columns([1.1, 1.1, 1.1, 1.1])

    with f1:
        region_options = ["Toutes les régions (12)"] + sorted(dt["region"].unique().tolist())
        sel_region = st.selectbox("Région Administrative", options=region_options, index=0)

    # Filtrage en cascade de la province selon la région choisie
    if sel_region == "Toutes les régions (12)":
        avail_provs = sorted(dt["province"].unique().tolist())
    else:
        avail_provs = sorted(dt[dt["region"] == sel_region]["province"].unique().tolist())

    with f2:
        prov_options = [f"Toutes les provinces ({len(avail_provs)})"] + avail_provs
        sel_prov = st.selectbox("Province / Préfecture", options=prov_options, index=0)

    with f3:
        pole_options = [
            "Tous les types de pôles",
            "Pôles Majeurs (4 à 6 centres)",
            "Pôles Intermédiaires (2 à 3 centres)",
            "Pôles à Centre Unique (1 centre)"
        ]
        sel_pole = st.selectbox("Segment de Concentration", options=pole_options, index=0)

    with f4:
        search_text = st.text_input("Recherche Rapide (Lycée, Ville, Adresse)", value="", placeholder="Ex: Moulay Youssef, Tanger...")

# Application des filtres
dt_filtered = dt.copy()
if sel_region != "Toutes les régions (12)":
    dt_filtered = dt_filtered[dt_filtered["region"] == sel_region]
if not sel_prov.startswith("Toutes les provinces"):
    dt_filtered = dt_filtered[dt_filtered["province"] == sel_prov]
if sel_pole != "Tous les types de pôles":
    dt_filtered = dt_filtered[dt_filtered["pole_categorie"] == sel_pole]
if search_text.strip():
    q = search_text.strip().lower()
    dt_filtered = dt_filtered[
        dt_filtered["nom_etablissement"].str.lower().str.contains(q) |
        dt_filtered["commune"].str.lower().str.contains(q) |
        dt_filtered["province"].str.lower().str.contains(q) |
        dt_filtered["adresse"].str.lower().str.contains(q)
    ]

# ==============================================================================
# 4. LIGNE 1 : 4 CARTES KPI AVEC SPARKLINES
# ==============================================================================
total_etab = len(dt_filtered)
total_reg = dt_filtered["region"].nunique()
total_prov = dt_filtered["province"].nunique()
total_com = dt_filtered["commune"].nunique()
avg_per_reg = (total_etab / total_reg) if total_reg > 0 else 0.0

if total_etab > 0:
    top_reg = dt_filtered["region"].value_counts().index[0]
    top_reg_val = int(dt_filtered["region"].value_counts().values[0])
    top_reg_pct = (top_reg_val / total_etab) * 100
else:
    top_reg = "Aucune"
    top_reg_val = 0
    top_reg_pct = 0.0

prov_vc = dt_filtered["province"].value_counts()
dual_provs = int((prov_vc >= 2).sum())

k1, k2, k3, k4 = st.columns(4)

with k1:
    st.markdown(
        f'<div class="kpi-card">'
        f'<div>'
        f'<div class="kpi-header"><span class="kpi-title">Établissements CPGE</span><span class="info-badge">i</span></div>'
        f'<div class="kpi-metrics-row"><span class="kpi-primary" style="color:#00D4FF;">Actifs {total_etab}</span><span class="kpi-divider">|</span><span class="kpi-secondary">National 32</span></div>'
        f'<div class="kpi-delta">{(total_etab/32)*100:.1f}% du Réseau National &#9650;</div>'
        f'</div>'
        f'<svg class="kpi-sparkline" viewBox="0 0 240 55" preserveAspectRatio="none">'
        f'<defs><linearGradient id="gradCyan" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#00D4FF" stop-opacity="0.45"/><stop offset="100%" stop-color="#00D4FF" stop-opacity="0.02"/></linearGradient></defs>'
        f'<path d="M0,38 L35,28 L70,35 L105,32 L140,22 L175,12 L210,25 L240,14 L240,55 L0,55 Z" fill="url(#gradCyan)"/>'
        f'<polyline fill="none" stroke="#00D4FF" stroke-width="2.2" points="0,38 35,28 70,35 105,32 140,22 175,12 210,25 240,14"/>'
        f'</svg>'
        f'</div>',
        unsafe_allow_html=True
    )

with k2:
    st.markdown(
        f'<div class="kpi-card">'
        f'<div>'
        f'<div class="kpi-header"><span class="kpi-title">Couverture Régionale</span><span class="info-badge">i</span></div>'
        f'<div class="kpi-metrics-row"><span class="kpi-primary" style="color:#FF007F;">Régions {total_reg} / 12</span><span class="kpi-divider">|</span><span class="kpi-secondary">Moy. {avg_per_reg:.2f} / Rég.</span></div>'
        f'<div class="kpi-delta">{(total_reg/12)*100:.1f}% Couverture Territoriale &#9650;</div>'
        f'</div>'
        f'<svg class="kpi-sparkline" viewBox="0 0 240 55" preserveAspectRatio="none">'
        f'<defs><linearGradient id="gradPink" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#FF007F" stop-opacity="0.45"/><stop offset="100%" stop-color="#FF007F" stop-opacity="0.02"/></linearGradient></defs>'
        f'<path d="M0,30 L40,20 L80,45 L120,25 L160,32 L200,14 L240,22 L240,55 L0,55 Z" fill="url(#gradPink)"/>'
        f'<polyline fill="none" stroke="#FF007F" stroke-width="2.2" points="0,30 40,20 80,45 120,25 160,32 200,14 240,22"/>'
        f'</svg>'
        f'</div>',
        unsafe_allow_html=True
    )

with k3:
    st.markdown(
        f'<div class="kpi-card">'
        f'<div>'
        f'<div class="kpi-header"><span class="kpi-title">Maillage Provincial</span><span class="info-badge">i</span></div>'
        f'<div class="kpi-metrics-row"><span class="kpi-primary" style="color:#00D4FF;">Provinces {total_prov}</span><span class="kpi-divider">|</span><span class="kpi-secondary">Communes {total_com}</span></div>'
        f'<div class="kpi-delta">{dual_provs} Provinces Bi-Centres (2 CPGE) &#9650;</div>'
        f'</div>'
        f'<svg class="kpi-sparkline" viewBox="0 0 240 55" preserveAspectRatio="none">'
        f'<defs><linearGradient id="gradPurple" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#A855F7" stop-opacity="0.45"/><stop offset="100%" stop-color="#A855F7" stop-opacity="0.02"/></linearGradient></defs>'
        f'<path d="M0,32 L40,36 L80,26 L120,30 L160,34 L200,15 L240,28 L240,55 L0,55 Z" fill="url(#gradPurple)"/>'
        f'<polyline fill="none" stroke="#C084FC" stroke-width="2.2" points="0,32 40,36 80,26 120,30 160,34 200,15 240,28"/>'
        f'</svg>'
        f'</div>',
        unsafe_allow_html=True
    )

with k4:
    st.markdown(
        f'<div class="kpi-card">'
        f'<div>'
        f'<div class="kpi-header"><span class="kpi-title">Concentration Maximale</span><span class="info-badge">i</span></div>'
        f'<div class="kpi-metrics-row"><span class="kpi-primary" style="color:#FFB703;">Max {top_reg_val} Centres</span><span class="kpi-divider">|</span><span class="kpi-secondary">{top_reg[:17]}</span></div>'
        f'<div class="kpi-delta">{top_reg_pct:.1f}% de la Sélection &#9650;</div>'
        f'</div>'
        f'<svg class="kpi-sparkline" viewBox="0 0 240 55" preserveAspectRatio="none">'
        f'<defs><linearGradient id="gradAmber" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#FFB703" stop-opacity="0.45"/><stop offset="100%" stop-color="#FFB703" stop-opacity="0.02"/></linearGradient></defs>'
        f'<path d="M0,34 L40,26 L80,30 L120,36 L160,28 L200,10 L240,24 L240,55 L0,55 Z" fill="url(#gradAmber)"/>'
        f'<polyline fill="none" stroke="#FFB703" stroke-width="2.2" points="0,34 40,26 80,30 120,36 160,28 200,10 240,24"/>'
        f'</svg>'
        f'</div>',
        unsafe_allow_html=True
    )

st.write("")

# ==============================================================================
# 5. LIGNE 2 : CAPACITÉ PAR RÉGION + SYNTHÈSE PAR RÉGION + CARTE SANS API KEY
# ==============================================================================
col_left, col_mid, col_right = st.columns([1.05, 1.15, 1.2])

with col_left:
    with st.container(border=True):
        st.markdown(
            '<div class="visual-header">'
            '<div><div class="visual-title">Capacité CPGE par Région vs Moyenne</div>'
            '<div class="visual-subtitle">Nombre de centres par région comparé à la moyenne nationale (2.67)</div></div>'
            '<span class="info-badge">i</span>'
            '</div>',
            unsafe_allow_html=True
        )
        if len(dt_filtered) > 0:
            reg_df = dt_filtered["region"].value_counts().reset_index()
            reg_df.columns = ["region", "count"]

            fig_reg = go.Figure()
            fig_reg.add_trace(go.Bar(
                x=reg_df["region"],
                y=reg_df["count"],
                marker_color="#00D4FF",
                text=reg_df["count"],
                textposition="outside",
                textfont=dict(color="#E2E8F0", size=11),
                hovertemplate="<b>%{x}</b><br>Établissements : %{y}<extra></extra>"
            ))
            fig_reg.add_hline(
                y=2.67,
                line_dash="dot",
                line_color="#FF007F",
                annotation_text="Moy. (2.67)",
                annotation_position="top right",
                annotation_font=dict(color="#FF007F", size=10)
            )
            fig_reg.update_layout(
                height=315,
                margin=dict(t=15, r=10, b=80, l=30),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#94A3B8", size=10),
                xaxis=dict(title="", tickangle=-35, showgrid=False, tickfont=dict(color="#CBD5E1", size=10)),
                yaxis=dict(title="Nb Centres", gridcolor="rgba(148, 163, 184, 0.12)", dtick=1, range=[0, max(reg_df["count"]) + 1.2]),
                showlegend=False
            )
            st.plotly_chart(fig_reg, use_container_width=True, config={"displayModeBar": False})
        else:
            st.info("Aucune donnée disponible.")

with col_mid:
    with st.container(border=True):
        reg_summary = []
        for reg_name, group in dt_filtered.groupby("region"):
            nb_c = len(group)
            nb_p = group["province"].nunique()
            nb_com = group["commune"].nunique()
            part_pct = (nb_c / len(dt_filtered) * 100) if len(dt_filtered) > 0 else 0
            ratio_avg = nb_c / 2.6667
            reg_summary.append({
                "region": reg_name,
                "centres": nb_c,
                "provinces": nb_p,
                "communes": nb_com,
                "part": part_pct,
                "indice": ratio_avg
            })
        reg_summary = sorted(reg_summary, key=lambda x: x["centres"], reverse=True)

        # IMPORTANT: Aucune indentation de 4 espaces pour éviter que Markdown le transforme en bloc code
        rows_html = "".join([
            f'<tr>'
            f'<td>{r["region"]}</td>'
            f'<td class="num-col highlight-cyan">{r["centres"]}</td>'
            f'<td class="num-col">{r["provinces"]}</td>'
            f'<td class="num-col">{r["communes"]}</td>'
            f'<td class="num-col">{r["part"]:.1f}%</td>'
            f'<td class="num-col">{r["indice"]:.2f}x</td>'
            f'</tr>'
            for r in reg_summary
        ])

        table_region_html = (
            '<div class="visual-header">'
            '<div><div class="visual-title">Synthèse Territoriale par Région</div>'
            '<div class="visual-subtitle">Distribution des centres, provinces, communes, poids national et indice</div></div>'
            '<span class="info-badge">i</span>'
            '</div>'
            '<div class="pbi-table-wrap">'
            '<table class="pbi-table">'
            '<thead><tr>'
            '<th>Région</th>'
            '<th class="num-col">Centres</th>'
            '<th class="num-col">Provinces</th>'
            '<th class="num-col">Communes</th>'
            '<th class="num-col">Part (%)</th>'
            '<th class="num-col">Indice</th>'
            '</tr></thead>'
            f'<tbody>{rows_html}</tbody>'
            '</table>'
            '</div>'
        )
        st.markdown(table_region_html, unsafe_allow_html=True)

with col_right:
    with st.container(border=True):
        st.markdown(
            '<div class="visual-header">'
            '<div><div class="visual-title">Cartographie des 32 Établissements CPGE</div>'
            '<div class="visual-subtitle">Localisation interactive par catégorie de pôle (OpenStreetMap Dark)</div></div>'
            '<span class="info-badge">i</span>'
            '</div>',
            unsafe_allow_html=True
        )
        # Carte Leaflet + OpenStreetMap avec filtre sombre CSS (100% gratuit, AUCUNE clé API requise)
        map_records = []
        for _, r in dt_filtered.iterrows():
            map_records.append({
                "nom": str(r["nom_etablissement"]),
                "reg": str(r["region"]),
                "prov": str(r["province"]),
                "com": str(r["commune"]),
                "adr": str(r["adresse"]),
                "pole": str(r["pole_categorie"]),
                "lat": float(r["lat"]),
                "lon": float(r["lon"])
            })
        map_json = json.dumps(map_records, ensure_ascii=False)

        leaflet_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8" />
            <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
            <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
            <style>
                html, body {{ margin: 0; padding: 0; background: #0C213B; font-family: 'Inter', sans-serif; }}
                #map {{ width: 100%; height: 310px; border-radius: 8px; background: #061325; border: 1px solid #16365F; }}
                /* Filtre sombre sur les tuiles OpenStreetMap standards (zéro API key) */
                .leaflet-tile-pane {{
                    filter: invert(100%) hue-rotate(185deg) brightness(92%) contrast(90%);
                }}
                .legend-box {{
                    display: flex;
                    gap: 12px;
                    margin-top: 6px;
                    font-size: 11px;
                    color: #CBD5E1;
                    justify-content: center;
                }}
                .dot {{
                    width: 9px;
                    height: 9px;
                    border-radius: 50%;
                    display: inline-block;
                    margin-right: 4px;
                }}
            </style>
        </head>
        <body>
            <div id="map"></div>
            <div class="legend-box">
                <span><i class="dot" style="background:#00D4FF;"></i>Pôles Majeurs (4-6)</span>
                <span><i class="dot" style="background:#FF007F;"></i>Pôles Intermédiaires (2-3)</span>
                <span><i class="dot" style="background:#FFB703;"></i>Centre Unique (1)</span>
            </div>
            <script>
                const pts = {map_json};
                const map = L.map('map', {{ zoomControl: true }}).setView([29.2, -7.6], 5);
                L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{
                    attribution: '&copy; OpenStreetMap',
                    maxZoom: 18
                }}).addTo(map);

                const colors = {{
                    "Pôles Majeurs (4 à 6 centres)": "#00D4FF",
                    "Pôles Intermédiaires (2 à 3 centres)": "#FF007F",
                    "Pôles à Centre Unique (1 centre)": "#FFB703"
                }};

                const bounds = [];
                pts.forEach(p => {{
                    const c = colors[p.pole] || "#00D4FF";
                    const m = L.circleMarker([p.lat, p.lon], {{
                        radius: 7,
                        fillColor: c,
                        color: "#061325",
                        weight: 1.8,
                        opacity: 1,
                        fillOpacity: 0.95
                    }}).addTo(map);
                    m.bindPopup(
                        `<div style="font-size:12px; line-height:1.4; color:#0F172A;">` +
                        `<strong style="color:#005A9E;">${{p.nom}}</strong><br>` +
                        `<b>Région :</b> ${{p.reg}}<br>` +
                        `<b>Province :</b> ${{p.prov}}<br>` +
                        `<b>Commune :</b> ${{p.com}}<br>` +
                        `<b>Adresse :</b> ${{p.adr}}` +
                        `</div>`
                    );
                    bounds.push([p.lat, p.lon]);
                }});
                if (bounds.length > 0 && bounds.length < 32) {{
                    map.fitBounds(bounds, {{ padding: [30, 30], maxZoom: 12 }});
                }}
            </script>
        </body>
        </html>
        """
        components.html(leaflet_html, height=340)

# ==============================================================================
# 6. LIGNE 3 : DONUT (SEGMENTS) + PROVINCES BI-CENTRES + RÉPERTOIRE CLASSÉ
# ==============================================================================
b_left, b_mid, b_right = st.columns([1.05, 1.15, 1.2])

with b_left:
    with st.container(border=True):
        st.markdown(
            '<div class="visual-header">'
            '<div><div class="visual-title">Quel Segment Contribue le Plus à l&rsquo;Offre ?</div>'
            '<div class="visual-subtitle">Part des établissements selon la taille du pôle régional</div></div>'
            '<span class="info-badge">i</span>'
            '</div>',
            unsafe_allow_html=True
        )
        if len(dt_filtered) > 0:
            pole_df = dt_filtered["pole_categorie"].value_counts().reset_index()
            pole_df.columns = ["pole_categorie", "count"]
            color_map_pie = {
                "Pôles Majeurs (4 à 6 centres)": "#00D4FF",
                "Pôles Intermédiaires (2 à 3 centres)": "#FF007F",
                "Pôles à Centre Unique (1 centre)": "#FFB703"
            }
            pie_colors = [color_map_pie.get(k, "#00D4FF") for k in pole_df["pole_categorie"]]

            fig_pie = go.Figure(data=[go.Pie(
                labels=pole_df["pole_categorie"],
                values=pole_df["count"],
                hole=0.42,
                marker=dict(colors=pie_colors, line=dict(color="#0C213B", width=2)),
                textinfo="percent",
                textfont=dict(color="#FFFFFF", size=12),
                hovertemplate="<b>%{label}</b><br>Établissements : %{value} (%{percent})<extra></extra>"
            )])
            fig_pie.update_layout(
                height=300,
                margin=dict(t=10, r=10, b=40, l=10),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#E2E8F0", size=10),
                legend=dict(orientation="h", yanchor="bottom", y=-0.22, xanchor="center", x=0.5, font=dict(color="#CBD5E1", size=10))
            )
            st.plotly_chart(fig_pie, use_container_width=True, config={"displayModeBar": False})
        else:
            st.info("Aucune donnée disponible.")

with b_mid:
    with st.container(border=True):
        st.markdown(
            '<div class="visual-header">'
            '<div><div class="visual-title">Analyse des Provinces à Forte Densité CPGE</div>'
            '<div class="visual-subtitle">Les 7 provinces bi-centres (2 CPGE) face aux provinces mono-centre</div></div>'
            '<span class="info-badge">i</span>'
            '</div>',
            unsafe_allow_html=True
        )
        if len(dt_filtered) > 0:
            prov_df = dt_filtered["province"].value_counts().reset_index()
            prov_df.columns = ["province", "count"]
            top_prov_df = prov_df.head(9).sort_values(by="count", ascending=True)
            bar_colors = ["#00D4FF" if c >= 2 else "#1E4976" for c in top_prov_df["count"]]

            fig_prov = go.Figure(go.Bar(
                x=top_prov_df["count"],
                y=top_prov_df["province"].str.replace("Préfecture: ", "").str.replace("Province: ", ""),
                orientation="h",
                marker_color=bar_colors,
                text=[f"{v} centres (6.25%)" if v == 2 else f"{v} centre (3.13%)" for v in top_prov_df["count"]],
                textposition="outside",
                textfont=dict(color="#00E5A3", size=10),
                hovertemplate="<b>%{y}</b><br>Nombre de centres : %{x}<extra></extra>"
            ))
            fig_prov.update_layout(
                height=300,
                margin=dict(t=10, r=95, b=25, l=110),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#CBD5E1", size=10),
                xaxis=dict(title="Nombre de centres CPGE", gridcolor="rgba(148, 163, 184, 0.12)", dtick=1, range=[0, 2.8]),
                yaxis=dict(title="", showgrid=False)
            )
            st.plotly_chart(fig_prov, use_container_width=True, config={"displayModeBar": False})
        else:
            st.info("Aucune donnée disponible.")

with b_right:
    with st.container(border=True):
        # Construire le tableau sans aucune indentation de 4 espaces
        etab_rows = "".join([
            f'<tr>'
            f'<td class="highlight-cyan">{row["nom_etablissement"]}</td>'
            f'<td>{row["commune"].replace(" (Mun.)", "").replace(" (Arrond.)", "")}</td>'
            f'<td>{row["province"].replace("Préfecture: ", "").replace("Province: ", "")}</td>'
            f'<td>{row["region"]}</td>'
            f'</tr>'
            for _, row in dt_filtered.iterrows()
        ])

        etab_table_html = (
            '<div class="visual-header">'
            f'<div><div class="visual-title">Répertoire Classé des Établissements ({len(dt_filtered)})</div>'
            '<div class="visual-subtitle">Liste officielle filtrée par établissement, commune, province et région</div></div>'
            '<span class="info-badge">i</span>'
            '</div>'
            '<div class="pbi-table-wrap" style="max-height: 285px;">'
            '<table class="pbi-table">'
            '<thead><tr>'
            '<th>Établissement</th>'
            '<th>Commune</th>'
            '<th>Province</th>'
            '<th>Région</th>'
            '</tr></thead>'
            f'<tbody>{etab_rows}</tbody>'
            '</table>'
            '</div>'
        )
        st.markdown(etab_table_html, unsafe_allow_html=True)

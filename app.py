import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import os


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Material Selection Studio",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# COSMIC / NEON STYLE
# ============================================================

st.markdown("""
<style>

.stApp {
    background:
        radial-gradient(circle at 10% 10%, rgba(80, 40, 150, 0.28), transparent 30%),
        radial-gradient(circle at 90% 20%, rgba(0, 180, 255, 0.18), transparent 30%),
        radial-gradient(circle at 50% 100%, rgba(220, 0, 150, 0.18), transparent 35%),
        linear-gradient(135deg, #080b18 0%, #11152d 50%, #080b18 100%);
    color: #f2f4ff;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1500px;
}

/* Main title */

.hero-title {
    font-size: 3rem;
    font-weight: 800;
    letter-spacing: 1px;
    background: linear-gradient(
        90deg,
        #6ee7ff,
        #9b7cff,
        #ff5fc8
    );
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0;
}

.hero-subtitle {
    color: #aeb7d8;
    font-size: 1.05rem;
    margin-top: 0.2rem;
    margin-bottom: 1.5rem;
}

/* Cards */

.neon-card {
    background: rgba(20, 24, 50, 0.72);
    border: 1px solid rgba(126, 105, 255, 0.35);
    border-radius: 18px;
    padding: 20px;
    box-shadow:
        0 0 25px rgba(85, 60, 255, 0.08),
        inset 0 0 20px rgba(255,255,255,0.015);
}

.metric-card {
    background: linear-gradient(
        135deg,
        rgba(30, 35, 70, 0.85),
        rgba(17, 22, 45, 0.85)
    );
    border: 1px solid rgba(100, 200, 255, 0.22);
    border-radius: 16px;
    padding: 18px;
    text-align: center;
}

.metric-number {
    font-size: 2rem;
    font-weight: 800;
    color: #72ddff;
}

.metric-label {
    color: #9fa9c8;
    font-size: 0.85rem;
}

/* Sidebar */

section[data-testid="stSidebar"] {
    background:
        linear-gradient(
            180deg,
            rgba(13, 16, 36, 0.98),
            rgba(18, 13, 38, 0.98)
        );
    border-right: 1px solid rgba(120, 100, 255, 0.25);
}

/* Buttons */

.stButton > button {
    border-radius: 10px;
    border: 1px solid rgba(100, 220, 255, 0.35);
    background: rgba(35, 40, 80, 0.8);
    color: white;
    font-weight: 600;
}

.stButton > button:hover {
    border-color: #67e8f9;
    color: #67e8f9;
    box-shadow: 0 0 15px rgba(103,232,249,0.18);
}

/* Tabs */

button[data-baseweb="tab"] {
    color: #aab3d0 !important;
}

button[data-baseweb="tab"][aria-selected="true"] {
    color: #6ee7ff !important;
}

/* Dataframes */

div[data-testid="stDataFrame"] {
    border-radius: 12px;
    overflow: hidden;
}

/* Expander */

.streamlit-expanderHeader {
    color: #dfe7ff !important;
}

/* Divider */

hr {
    border-color: rgba(130, 120, 255, 0.20);
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# MATERIAL DATABASE
# ============================================================

MATERIAL_DATA = [
    # Metals
    ["Aluminum 6061-T6", "Metal", 2.70, 68.9, 276, 310, 167, 5.0, 0.33],
    ["Aluminum 7075-T6", "Metal", 2.81, 71.7, 503, 572, 130, 7.0, 0.33],
    ["Mild Steel", "Metal", 7.85, 200, 250, 400, 50, 1.5, 0.30],
    ["Stainless Steel 304", "Metal", 8.00, 193, 215, 505, 16, 5.0, 0.29],
    ["Stainless Steel 316", "Metal", 8.00, 193, 290, 580, 14, 6.0, 0.30],
    ["Titanium Grade 5", "Metal", 4.43, 114, 880, 950, 7.2, 35.0, 0.34],
    ["Copper", "Metal", 8.96, 117, 70, 220, 401, 10.0, 0.34],
    ["Brass", "Metal", 8.50, 100, 200, 350, 120, 8.0, 0.34],
    ["Cast Iron", "Metal", 7.20, 110, 250, 400, 50, 1.8, 0.26],
    ["Magnesium AZ31B", "Metal", 1.77, 45, 200, 290, 96, 8.0, 0.35],

    # Polymers
    ["ABS", "Polymer", 1.04, 2.3, 40, 45, 0.18, 2.5, 0.35],
    ["Nylon 6", "Polymer", 1.14, 2.8, 70, 75, 0.25, 4.0, 0.39],
    ["Polycarbonate", "Polymer", 1.20, 2.4, 65, 70, 0.20, 3.5, 0.37],
    ["PEEK", "Polymer", 1.32, 3.6, 100, 100, 0.25, 80.0, 0.38],
    ["HDPE", "Polymer", 0.95, 0.8, 25, 30, 0.50, 2.0, 0.46],
    ["LDPE", "Polymer", 0.92, 0.2, 8, 12, 0.33, 2.0, 0.46],
    ["PP", "Polymer", 0.90, 1.5, 30, 35, 0.22, 2.2, 0.42],
    ["PVC Rigid", "Polymer", 1.40, 3.0, 50, 55, 0.17, 2.5, 0.40],
    ["PTFE", "Polymer", 2.20, 0.5, 15, 25, 0.25, 10.0, 0.46],
    ["PEI", "Polymer", 1.27, 3.2, 110, 110, 0.22, 25.0, 0.36],

    # Composites
    ["Carbon Fiber/Epoxy", "Composite", 1.55, 70, 600, 900, 5.0, 25.0, 0.30],
    ["Glass Fiber/Polyester", "Composite", 1.80, 25, 300, 500, 0.30, 8.0, 0.30],
    ["Glass Fiber/Epoxy", "Composite", 1.90, 35, 450, 700, 0.35, 12.0, 0.30],
    ["Aramid/Epoxy", "Composite", 1.35, 50, 500, 900, 0.20, 30.0, 0.35],
    ["GFRP Pultruded", "Composite", 1.90, 30, 350, 600, 0.35, 7.0, 0.28],
    ["CFRP", "Composite", 1.60, 120, 800, 1500, 5.5, 40.0, 0.28],

    # Wood
    ["Oak", "Wood", 0.70, 11, 50, 100, 0.17, 4.0, 0.35],
    ["Pine", "Wood", 0.50, 9, 35, 70, 0.12, 2.0, 0.35],
    ["Balsa", "Wood", 0.16, 3.0, 10, 15, 0.06, 8.0, 0.30],
    ["Birch", "Wood", 0.65, 13, 55, 110, 0.18, 3.5, 0.35],

    # Ceramics
    ["Concrete", "Ceramic", 2.40, 30, 20, 5, 1.70, 0.15, 0.20],
    ["Alumina", "Ceramic", 3.90, 380, 300, 300, 25, 5.0, 0.22],
    ["Silicon Carbide", "Ceramic", 3.10, 410, 350, 350, 120, 20.0, 0.17],
    ["Glass", "Ceramic", 2.50, 70, 40, 50, 1.0, 1.0, 0.22],

    # Other
    ["Epoxy Resin", "Polymer", 1.20, 3.0, 50, 60, 0.20, 4.0, 0.35],
    ["Silicone Rubber", "Elastomer", 1.10, 0.01, 5, 8, 0.20, 8.0, 0.49],
    ["Natural Rubber", "Elastomer", 0.93, 0.005, 20, 25, 0.13, 3.0, 0.49],
    ["Neoprene", "Elastomer", 1.23, 0.01, 15, 20, 0.20, 5.0, 0.49],
    ["Cork", "Natural", 0.24, 0.03, 2, 3, 0.04, 3.0, 0.30],
    ["Bamboo", "Natural", 0.70, 20, 80, 160, 0.15, 3.0, 0.35],
]

COLUMNS = [
    "Material",
    "Family",
    "Density",
    "Young's Modulus",
    "Yield Strength",
    "Tensile Strength",
    "Thermal Conductivity",
    "Cost",
    "Poisson Ratio"
]

df = pd.DataFrame(MATERIAL_DATA, columns=COLUMNS)


# ============================================================
# SESSION STATE
# ============================================================

if "materials" not in st.session_state:
    st.session_state.materials = df.copy()

if "selected_materials" not in st.session_state:
    st.session_state.selected_materials = []


materials = st.session_state.materials


# ============================================================
# PROPERTY INFORMATION
# ============================================================

PROPERTY_INFO = {
    "Density": ("Density", "g/cm³"),
    "Young's Modulus": ("Young's Modulus", "GPa"),
    "Yield Strength": ("Yield Strength", "MPa"),
    "Tensile Strength": ("Tensile Strength", "MPa"),
    "Thermal Conductivity": ("Thermal Conductivity", "W/m·K"),
    "Cost": ("Relative Cost", "$/kg"),
    "Poisson Ratio": ("Poisson Ratio", "")
}


FAMILY_COLORS = {
    "Metal": "#4cc9f0",
    "Polymer": "#f72585",
    "Composite": "#7209b7",
    "Wood": "#f4a261",
    "Ceramic": "#90be6d",
    "Elastomer": "#ffca3a",
    "Natural": "#43aa8b"
}


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="hero-title">Material Selection Studio</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="hero-subtitle">'
    'Interactive materials database, comparison, Ashby-style plotting, '
    'and multi-criteria screening'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown("## ⚙️ Material Selection")

    page = st.radio(
        "Navigate",
        [
            "🗃️ Database",
            "📊 Compare",
            "📈 Ashby Plot",
            "🎯 Screening"
        ]
    )

    st.divider()

    st.markdown("### Database")

    st.metric(
        "Materials",
        len(materials)
    )

    st.metric(
        "Families",
        materials["Family"].nunique()
    )

    st.divider()

    st.caption(
        "Educational material-selection tool. "
        "Property values are illustrative and should be verified "
        "against appropriate engineering references before design use."
    )


# ============================================================
# DATABASE
# ============================================================

if page == "🗃️ Database":

    st.header("Materials Database")

    c1, c2, c3 = st.columns([2, 1, 1])

    with c1:
        search = st.text_input(
            "🔎 Search",
            placeholder="Search material name..."
        )

    with c2:
        family_options = ["All"] + sorted(
            materials["Family"].unique().tolist()
        )

        family = st.selectbox(
            "Family",
            family_options
        )

    with c3:
        sort_by = st.selectbox(
            "Sort by",
            COLUMNS
        )

    filtered = materials.copy()

    if search:
        filtered = filtered[
            filtered["Material"]
            .str.contains(search, case=False, na=False)
        ]

    if family != "All":
        filtered = filtered[
            filtered["Family"] == family
        ]

    filtered = filtered.sort_values(sort_by)

    st.markdown(
        f"**Showing {len(filtered)} of {len(materials)} materials**"
    )

    st.dataframe(
        filtered,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Density": st.column_config.NumberColumn(
                "Density (g/cm³)",
                format="%.2f"
            ),
            "Young's Modulus": st.column_config.NumberColumn(
                "Young's Modulus (GPa)",
                format="%.2f"
            ),
            "Yield Strength": st.column_config.NumberColumn(
                "Yield Strength (MPa)",
                format="%.0f"
            ),
            "Tensile Strength": st.column_config.NumberColumn(
                "Tensile Strength (MPa)",
                format="%.0f"
            ),
            "Thermal Conductivity": st.column_config.NumberColumn(
                "Thermal Conductivity (W/m·K)",
                format="%.2f"
            ),
            "Cost": st.column_config.NumberColumn(
                "Relative Cost ($/kg)",
                format="%.2f"
            ),
            "Poisson Ratio": st.column_config.NumberColumn(
                "Poisson Ratio",
                format="%.2f"
            )
        }
    )

    st.divider()

    st.subheader("➕ Add Material")

    with st.expander("Add a custom material"):

        with st.form("add_material_form"):

            a1, a2 = st.columns(2)

            with a1:
                new_name = st.text_input("Material name")
                new_family = st.selectbox(
                    "Family",
                    sorted(materials["Family"].unique())
                )
                new_density = st.number_input(
                    "Density (g/cm³)",
                    min_value=0.0,
                    value=1.0
                )
                new_modulus = st.number_input(
                    "Young's Modulus (GPa)",
                    min_value=0.0,
                    value=1.0
                )
                new_yield = st.number_input(
                    "Yield Strength (MPa)",
                    min_value=0.0,
                    value=10.0
                )

            with a2:
                new_tensile = st.number_input(
                    "Tensile Strength (MPa)",
                    min_value=0.0,
                    value=10.0
                )
                new_thermal = st.number_input(
                    "Thermal Conductivity (W/m·K)",
                    min_value=0.0,
                    value=1.0
                )
                new_cost = st.number_input(
                    "Relative Cost ($/kg)",
                    min_value=0.0,
                    value=1.0
                )
                new_poisson = st.number_input(
                    "Poisson Ratio",
                    min_value=0.0,
                    max_value=0.5,
                    value=0.30
                )

            submitted = st.form_submit_button(
                "Add Material"
            )

            if submitted:

                if not new_name.strip():
                    st.error("Please enter a material name.")

                elif new_name in materials["Material"].values:
                    st.error("That material already exists.")

                else:

                    new_row = pd.DataFrame([[
                        new_name,
                        new_family,
                        new_density,
                        new_modulus,
                        new_yield,
                        new_tensile,
                        new_thermal,
                        new_cost,
                        new_poisson
                    ]], columns=COLUMNS)

                    st.session_state.materials = pd.concat(
                        [materials, new_row],
                        ignore_index=True
                    )

                    st.success(
                        f"{new_name} added to this session."
                    )

                    st.rerun()

    st.divider()

    csv_data = materials.to_csv(index=False).encode("utf-8")

    st.download_button(
        "⬇️ Download Database CSV",
        csv_data,
        "materials_database.csv",
        "text/csv"
    )


# ============================================================
# COMPARE
# ============================================================

elif page == "📊 Compare":

    st.header("Compare Materials")

    material_names = materials["Material"].tolist()

    selected = st.multiselect(
        "Select materials to compare",
        material_names,
        default=st.session_state.selected_materials
    )

    st.session_state.selected_materials = selected

    if not selected:

        st.info(
            "Select two or more materials above to begin a comparison."
        )

    else:

        comparison = materials[
            materials["Material"].isin(selected)
        ].copy()

        comparison = comparison.set_index("Material")

        st.subheader("Property Comparison")

        st.dataframe(
            comparison.T,
            use_container_width=True
        )

        st.subheader("Visual Comparison")

        numeric_properties = [
            "Density",
            "Young's Modulus",
            "Yield Strength",
            "Tensile Strength",
            "Thermal Conductivity",
            "Cost",
            "Poisson Ratio"
        ]

        property = st.selectbox(
            "Property",
            numeric_properties
        )

        chart_data = materials[
            materials["Material"].isin(selected)
        ]

        fig = px.bar(
            chart_data,
            x="Material",
            y=property,
            color="Family",
            color_discrete_map=FAMILY_COLORS,
            title=f"{property} Comparison"
        )

        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="white"),
            height=500
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


# ============================================================
# ASHBY PLOT
# ============================================================

elif page == "📈 Ashby Plot":

    st.header("Ashby-Style Material Plot")

    properties = [
        "Density",
        "Young's Modulus",
        "Yield Strength",
        "Tensile Strength",
        "Thermal Conductivity",
        "Cost",
        "Poisson Ratio"
    ]

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        x_property = st.selectbox(
            "X-axis",
            properties,
            index=0
        )

    with c2:
        y_property = st.selectbox(
            "Y-axis",
            properties,
            index=1
        )

    with c3:
        plot_family = st.selectbox(
            "Family",
            ["All"] + sorted(
                materials["Family"].unique().tolist()
            )
        )

    with c4:
        log_axes = st.checkbox(
            "Logarithmic axes",
            value=True
        )

    plot_df = materials.copy()

    if plot_family != "All":
        plot_df = plot_df[
            plot_df["Family"] == plot_family
        ]

    fig = px.scatter(
        plot_df,
        x=x_property,
        y=y_property,
        color="Family",
        hover_name="Material",
        color_discrete_map=FAMILY_COLORS,
        custom_data=["Density", "Young's Modulus",
                    "Yield Strength", "Tensile Strength",
                    "Thermal Conductivity", "Cost",
                    "Poisson Ratio"]
    )

    if log_axes:

        fig.update_xaxes(
            type="log"
        )

        fig.update_yaxes(
            type="log"
        )

    fig.update_traces(
        marker=dict(
            size=12,
            line=dict(
                width=1,
                color="rgba(255,255,255,0.5)"
            )
        )
    )

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(10,15,35,0.35)",
        font=dict(color="white"),
        height=650,
        legend_title="Material Family",
        margin=dict(l=30, r=30, t=60, b=30)
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.info(
        "Tip: Logarithmic axes are often useful when material properties "
        "span several orders of magnitude."
    )


# ============================================================
# SCREENING
# ============================================================

elif page == "🎯 Screening":

    st.header("Material Screening")

    st.markdown(
        "Define engineering criteria and calculate a weighted screening score."
    )

    properties = [
        "Density",
        "Young's Modulus",
        "Yield Strength",
        "Tensile Strength",
        "Thermal Conductivity",
        "Cost",
        "Poisson Ratio"
    ]

    default_directions = {
        "Density": "≤",
        "Young's Modulus": "≥",
        "Yield Strength": "≥",
        "Tensile Strength": "≥",
        "Thermal Conductivity": "≥",
        "Cost": "≤",
        "Poisson Ratio": "≥"
    }

    criteria = []

    st.subheader("Criteria")

    for prop in properties:

        enabled = st.checkbox(
            prop,
            key=f"enable_{prop}"
        )

        if enabled:

            unit = PROPERTY_INFO[prop][1]

            c1, c2, c3 = st.columns([2, 1, 1])

            with c1:

                target = st.number_input(
                    f"Target ({unit})",
                    value=float(
                        materials[prop].median()
                    ),
                    key=f"target_{prop}"
                )

            with c2:

                direction = st.selectbox(
                    "Direction",
                    ["≤", "≥"],
                    index=0 if default_directions[prop] == "≤" else 1,
                    key=f"direction_{prop}"
                )

            with c3:

                weight = st.number_input(
                    "Weight",
                    min_value=0.0,
                    value=1.0,
                    key=f"weight_{prop}"
                )

            criteria.append(
                {
                    "property": prop,
                    "target": target,
                    "direction": direction,
                    "weight": weight
                }
            )

    if not criteria:

        st.info(
            "Enable one or more properties to screen the materials."
        )

    else:

        results = materials.copy()

        # Hard screening
        for criterion in criteria:

            prop = criterion["property"]
            target = criterion["target"]
            direction = criterion["direction"]

            if direction == "≤":
                results = results[
                    results[prop] <= target
                ]
            else:
                results = results[
                    results[prop] >= target
                ]

        if results.empty:

            st.warning(
                "No materials satisfy all selected criteria."
            )

        else:

            st.subheader(
                f"{len(results)} materials satisfy all criteria"
            )

            # ------------------------------------------------
            # Weighted score
            # ------------------------------------------------

            scored = materials.copy()

            scores = np.zeros(len(scored))

            total_weight = sum(
                c["weight"] for c in criteria
            )

            if total_weight == 0:
                total_weight = 1

            for criterion in criteria:

                prop = criterion["property"]
                target = criterion["target"]
                weight = criterion["weight"]
                direction = criterion["direction"]

                values = scored[prop].astype(float)

                if direction == "≤":

                    ratio = target / values.replace(
                        0, np.nan
                    )

                else:

                    ratio = values / target

                ratio = ratio.replace(
                    [np.inf, -np.inf],
                    np.nan
                ).fillna(0)

                ratio = ratio.clip(
                    lower=0,
                    upper=1
                )

                scores += (
                    ratio *
                    weight /
                    total_weight
                )

            scored["Weighted Score"] = scores * 100

            ranked = scored.sort_values(
                "Weighted Score",
                ascending=False
            )

            st.subheader("Weighted Screening Results")

            st.dataframe(
                ranked[
                    [
                        "Material",
                        "Family",
                        "Weighted Score"
                    ] + [
                        c["property"]
                        for c in criteria
                    ]
                ],
                use_container_width=True,
                hide_index=True,
                column_config={
                    "Weighted Score": st.column_config.ProgressColumn(
                        "Weighted Score",
                        min_value=0,
                        max_value=100,
                        format="%.1f"
                    )
                }
            )

            st.subheader("Materials Passing All Criteria")

            st.dataframe(
                results,
                use_container_width=True,
                hide_index=True
            )

            result_csv = ranked.to_csv(
                index=False
            ).encode("utf-8")

            st.download_button(
                "⬇️ Download Screening Results",
                result_csv,
                "material_screening_results.csv",
                "text/csv"
            )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "Material Selection Studio • Educational engineering materials "
    "selection tool • Property values are illustrative"
)

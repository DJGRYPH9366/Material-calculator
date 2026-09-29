import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import os

# ============================================================
# MATERIAL SELECTION STUDIO
# Streamlit Web Application
# ============================================================

st.set_page_config(
    page_title="Material Selection Studio",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# COSMIC / NEON UI
# ============================================================

st.markdown("""
<style>

.stApp {
    background:
        radial-gradient(circle at 10% 10%, rgba(80, 0, 180, 0.28), transparent 35%),
        radial-gradient(circle at 90% 20%, rgba(0, 200, 255, 0.18), transparent 35%),
        radial-gradient(circle at 50% 100%, rgba(255, 0, 150, 0.14), transparent 40%),
        linear-gradient(135deg, #050014 0%, #09001f 45%, #020817 100%);
    color: white;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
}

h1, h2, h3 {
    color: white !important;
}

p, label, .stMarkdown {
    color: #e8e8f5;
}

[data-testid="stSidebar"] {
    background:
        linear-gradient(180deg, #08001d 0%, #050014 100%);
    border-right: 1px solid rgba(150, 100, 255, 0.25);
}

[data-testid="stSidebar"] * {
    color: white !important;
}

div[data-testid="stMetric"] {
    background: rgba(255,255,255,0.055);
    border: 1px solid rgba(150,100,255,0.25);
    padding: 15px;
    border-radius: 15px;
}

div.stButton > button {
    border-radius: 10px;
    border: 1px solid rgba(150,100,255,0.5);
    background: linear-gradient(90deg, #24105c, #4a147e);
    color: white;
}

div.stButton > button:hover {
    border-color: #00d9ff;
    color: white;
}

.stSelectbox, .stMultiSelect, .stTextInput,
.stNumberInput, .stSlider {
    color: white;
}

div[data-baseweb="select"] > div {
    background-color: rgba(15, 8, 40, 0.95);
}

div[data-baseweb="input"] > div {
    background-color: rgba(15, 8, 40, 0.95);
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# LOAD DATABASE
# ============================================================

DATA_FILE = "materials.csv"

if not os.path.exists(DATA_FILE):
    st.error(
        "materials.csv was not found. "
        "Place materials.csv in the same folder as app.py."
    )
    st.stop()

df = pd.read_csv(DATA_FILE)

expected_columns = [
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

missing = [c for c in expected_columns if c not in df.columns]

if missing:
    st.error(f"Missing columns in materials.csv: {missing}")
    st.stop()

numeric_columns = [
    "Density",
    "Young's Modulus",
    "Yield Strength",
    "Tensile Strength",
    "Thermal Conductivity",
    "Cost",
    "Poisson Ratio"
]

for col in numeric_columns:
    df[col] = pd.to_numeric(df[col], errors="coerce")


# ============================================================
# SESSION STATE
# ============================================================

if "materials" not in st.session_state:
    st.session_state.materials = df.copy()

if "selected_materials" not in st.session_state:
    st.session_state.selected_materials = []


# ============================================================
# HEADER
# ============================================================

st.title("🔬 Material Selection Studio")

st.markdown(
    """
    **Interactive materials database, comparison, Ashby plotting,
    screening, and material-selection tool.**
    """
)

st.markdown("---")


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("🧭 Navigation")

page = st.sidebar.radio(
    "Go to",
    [
        "Database",
        "Compare",
        "Ashby Plot",
        "Screening",
        "⭐ Material Selection"
    ]
)

st.sidebar.markdown("---")

st.sidebar.caption(
    "Educational material-selection tool. "
    "Values are illustrative and should not be treated as certified engineering data."
)


# ============================================================
# DATABASE
# ============================================================

if page == "Database":

    st.header("📚 Material Database")

    col1, col2 = st.columns([2, 1])

    with col1:
        search = st.text_input(
            "Search materials",
            placeholder="e.g. aluminum, steel, polymer..."
        )

    with col2:
        families = ["All"] + sorted(
            st.session_state.materials["Family"].dropna().unique().tolist()
        )

        family = st.selectbox(
            "Family",
            families
        )

    display_df = st.session_state.materials.copy()

    if search:
        mask = display_df["Material"].str.contains(
            search,
            case=False,
            na=False
        )

        display_df = display_df[mask]

    if family != "All":
        display_df = display_df[
            display_df["Family"] == family
        ]

    sort_column = st.selectbox(
        "Sort by",
        expected_columns
    )

    ascending = st.checkbox(
        "Ascending",
        value=True
    )

    display_df = display_df.sort_values(
        sort_column,
        ascending=ascending
    )

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True
    )

    st.download_button(
        "⬇ Download Database CSV",
        display_df.to_csv(index=False),
        file_name="material_database.csv",
        mime="text/csv"
    )

    st.markdown("---")

    st.subheader("➕ Add Custom Material")

    c1, c2 = st.columns(2)

    with c1:
        new_material = st.text_input("Material name")
        new_family = st.selectbox(
            "Family",
            sorted(df["Family"].dropna().unique())
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

    with c2:
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
            "Cost ($/kg)",
            min_value=0.0,
            value=1.0
        )
        new_poisson = st.number_input(
            "Poisson Ratio",
            min_value=0.0,
            max_value=0.5,
            value=0.30
        )

    if st.button("Add Material"):

        if not new_material.strip():
            st.warning("Please enter a material name.")

        else:

            new_row = pd.DataFrame([{
                "Material": new_material,
                "Family": new_family,
                "Density": new_density,
                "Young's Modulus": new_modulus,
                "Yield Strength": new_yield,
                "Tensile Strength": new_tensile,
                "Thermal Conductivity": new_thermal,
                "Cost": new_cost,
                "Poisson Ratio": new_poisson
            }])

            st.session_state.materials = pd.concat(
                [st.session_state.materials, new_row],
                ignore_index=True
            )

            st.success(f"{new_material} added for this session.")


# ============================================================
# COMPARE
# ============================================================

elif page == "Compare":

    st.header("⚖️ Compare Materials")

    materials = st.multiselect(
        "Select materials",
        st.session_state.materials["Material"].tolist(),
        max_selections=10
    )

    if materials:

        selected = st.session_state.materials[
            st.session_state.materials["Material"].isin(materials)
        ]

        st.dataframe(
            selected,
            use_container_width=True,
            hide_index=True
        )

        property_choice = st.selectbox(
            "Property to compare",
            numeric_columns
        )

        fig = px.bar(
            selected,
            x="Material",
            y=property_choice,
            color="Family",
            title=f"{property_choice} Comparison"
        )

        fig.update_layout(
            template="plotly_dark",
            height=550
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


# ============================================================
# ASHBY PLOT
# ============================================================

elif page == "Ashby Plot":

    st.header("📈 Ashby-Style Material Plot")

    c1, c2 = st.columns(2)

    with c1:
        x_property = st.selectbox(
            "X-axis",
            numeric_columns,
            index=0
        )

    with c2:
        y_property = st.selectbox(
            "Y-axis",
            numeric_columns,
            index=1
        )

    log_x = st.checkbox(
        "Logarithmic X-axis"
    )

    log_y = st.checkbox(
        "Logarithmic Y-axis"
    )

    fig = px.scatter(
        st.session_state.materials,
        x=x_property,
        y=y_property,
        color="Family",
        hover_name="Material",
        hover_data=numeric_columns,
        title=f"{y_property} vs {x_property}"
    )

    fig.update_layout(
        template="plotly_dark",
        height=650
    )

    if log_x:
        fig.update_xaxes(type="log")

    if log_y:
        fig.update_yaxes(type="log")

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ============================================================
# SCREENING
# ============================================================

elif page == "Screening":

    st.header("🔎 Material Screening")

    st.write(
        "Apply hard constraints to eliminate materials that do not meet "
        "your design requirements."
    )

    screening_df = st.session_state.materials.copy()

    constraints = []

    st.subheader("Constraints")

    for prop in numeric_columns:

        use_constraint = st.checkbox(
            f"Constrain {prop}",
            key=f"screen_{prop}"
        )

        if use_constraint:

            c1, c2 = st.columns(2)

            with c1:
                operator = st.selectbox(
                    f"Requirement for {prop}",
                    ["≤", "≥"],
                    key=f"operator_{prop}"
                )

            with c2:
                value = st.number_input(
                    f"Limit for {prop}",
                    value=float(
                        screening_df[prop].median()
                    ),
                    key=f"value_{prop}"
                )

            constraints.append(
                (prop, operator, value)
            )

    for prop, operator, value in constraints:

        if operator == "≤":
            screening_df = screening_df[
                screening_df[prop] <= value
            ]

        else:
            screening_df = screening_df[
                screening_df[prop] >= value
            ]

    st.markdown("---")

    st.metric(
        "Materials Remaining",
        len(screening_df)
    )

    st.dataframe(
        screening_df,
        use_container_width=True,
        hide_index=True
    )

    st.download_button(
        "⬇ Download Screening Results",
        screening_df.to_csv(index=False),
        file_name="screened_materials.csv",
        mime="text/csv"
    )


# ============================================================
# MATERIAL SELECTION
# ============================================================

elif page == "⭐ Material Selection":

    st.header("⭐ Ashby-Style Material Selection")

    st.markdown(
        """
        ### Design → Constraints → Screening → Ranking

        Use this workflow to move from a general design requirement
        toward a ranked set of candidate materials.
        """
    )

    st.info(
        "The ranking score used here is a normalized educational "
        "selection score. It is not a universal Ashby material index. "
        "Specific engineering material indices can be added for individual "
        "design cases."
    )

    # --------------------------------------------------------
    # OBJECTIVE
    # --------------------------------------------------------

    st.subheader("1️⃣ Choose the Design Objective")

    objective_options = {
        "Minimize Mass / Density": {
            "property": "Density",
            "direction": "min"
        },
        "Minimize Cost": {
            "property": "Cost",
            "direction": "min"
        },
        "Maximize Stiffness": {
            "property": "Young's Modulus",
            "direction": "max"
        },
        "Maximize Yield Strength": {
            "property": "Yield Strength",
            "direction": "max"
        },
        "Maximize Tensile Strength": {
            "property": "Tensile Strength",
            "direction": "max"
        },
        "Maximize Thermal Conductivity": {
            "property": "Thermal Conductivity",
            "direction": "max"
        }
    }

    objective = st.selectbox(
        "Primary objective",
        list(objective_options.keys())
    )

    objective_property = objective_options[objective]["property"]
    objective_direction = objective_options[objective]["direction"]

    st.write(
        f"**Objective property:** {objective_property}"
    )

    # --------------------------------------------------------
    # OPTIONAL FAMILY FILTER
    # --------------------------------------------------------

    st.subheader("2️⃣ Select Material Families")

    all_families = sorted(
        st.session_state.materials["Family"].dropna().unique()
    )

    selected_families = st.multiselect(
        "Families allowed in the selection",
        all_families,
        default=all_families
    )

    selection_df = st.session_state.materials[
        st.session_state.materials["Family"].isin(selected_families)
    ].copy()

    # --------------------------------------------------------
    # CONSTRAINTS
    # --------------------------------------------------------

    st.subheader("3️⃣ Define Design Constraints")

    st.caption(
        "Only materials satisfying every selected constraint will remain."
    )

    constraints = []

    constraint_columns = st.columns(2)

    for i, prop in enumerate(numeric_columns):

        with constraint_columns[i % 2]:

            enabled = st.checkbox(
                f"Use {prop} constraint",
                key=f"selection_constraint_{prop}"
            )

            if enabled:

                operator = st.selectbox(
                    "Requirement",
                    ["≤", "≥"],
                    key=f"selection_operator_{prop}"
                )

                default_value = float(
                    selection_df[prop].median()
                ) if len(selection_df) else 0.0

                value = st.number_input(
                    f"Limit ({prop})",
                    value=default_value,
                    key=f"selection_value_{prop}"
                )

                constraints.append(
                    (prop, operator, value)
                )

    # --------------------------------------------------------
    # APPLY HARD CONSTRAINTS
    # --------------------------------------------------------

    screened = selection_df.copy()

    for prop, operator, value in constraints:

        if operator == "≤":
            screened = screened[
                screened[prop] <= value
            ]
        else:
            screened = screened[
                screened[prop] >= value
            ]

    # --------------------------------------------------------
    # SCORE
    # --------------------------------------------------------

    if len(screened) > 0:

        values = screened[objective_property].astype(float)

        minimum = values.min()
        maximum = values.max()

        if np.isclose(maximum, minimum):

            screened["Selection Score"] = 100.0

        else:

            if objective_direction == "max":

                screened["Selection Score"] = (
                    (values - minimum) /
                    (maximum - minimum)
                ) * 100

            else:

                screened["Selection Score"] = (
                    (maximum - values) /
                    (maximum - minimum)
                ) * 100

        screened = screened.sort_values(
            "Selection Score",
            ascending=False
        )

        # ----------------------------------------------------
        # SUMMARY
        # ----------------------------------------------------

        st.subheader("4️⃣ Selection Results")

        c1, c2, c3 = st.columns(3)

        with c1:
            st.metric(
                "Starting Materials",
                len(selection_df)
            )

        with c2:
            st.metric(
                "After Constraints",
                len(screened)
            )

        with c3:
            st.metric(
                "Objective",
                objective_property
            )

        # ----------------------------------------------------
        # TOP CANDIDATES
        # ----------------------------------------------------

        st.subheader("🏆 Candidate Materials")

        top_n = st.slider(
            "Number of candidates to display",
            min_value=3,
            max_value=min(10, len(screened)),
            value=min(5, len(screened))
        )

        top_candidates = screened.head(top_n)

        st.dataframe(
            top_candidates,
            use_container_width=True,
            hide_index=True
        )

        # ----------------------------------------------------
        # SCORE CHART
        # ----------------------------------------------------

        fig = px.bar(
            top_candidates.sort_values(
                "Selection Score",
                ascending=True
            ),
            x="Selection Score",
            y="Material",
            orientation="h",
            color="Family",
            title="Top Candidate Selection Scores"
        )

        fig.update_layout(
            template="plotly_dark",
            height=max(400, top_n * 65)
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        # ----------------------------------------------------
        # ASHBY-STYLE VISUALIZATION
        # ----------------------------------------------------

        st.subheader("📊 Selection Map")

        c1, c2 = st.columns(2)

        with c1:
            map_x = st.selectbox(
                "Selection map X-axis",
                numeric_columns,
                index=numeric_columns.index(
                    "Density"
                )
            )

        with c2:
            map_y = st.selectbox(
                "Selection map Y-axis",
                numeric_columns,
                index=numeric_columns.index(
                    objective_property
                )
            )

        plot_df = selection_df.copy()

        plot_df["Status"] = np.where(
            plot_df["Material"].isin(
                screened["Material"]
            ),
            "PASS",
            "REJECTED"
        )

        fig2 = px.scatter(
            plot_df,
            x=map_x,
            y=map_y,
            color="Status",
            symbol="Family",
            hover_name="Material",
            hover_data=numeric_columns,
            title=f"Material Selection Map: {map_y} vs {map_x}"
        )

        fig2.update_layout(
            template="plotly_dark",
            height=650
        )

        st.plotly_chart(
            fig2,
            use_container_width=True
        )

        # ----------------------------------------------------
        # DOWNLOAD
        # ----------------------------------------------------

        st.subheader("⬇ Export Results")

        export_df = screened.copy()

        st.download_button(
            "Download Ranked Selection CSV",
            export_df.to_csv(index=False),
            file_name="material_selection_results.csv",
            mime="text/csv"
        )

    else:

        st.warning(
            "No materials satisfy the current constraints. "
            "Try relaxing one or more requirements."
        )

        st.subheader("Current Constraints")

        if constraints:

            for prop, operator, value in constraints:

                st.write(
                    f"• **{prop}** {operator} **{value}**"
                )

        else:

            st.write(
                "No constraints have been applied yet."
            )


# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.caption(
    "Material Selection Studio • Educational engineering tool • "
    "Material properties are illustrative."
)

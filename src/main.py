"""Main Streamlit application entry point."""

import streamlit as st

# Page configuration
st.set_page_config(
    page_title="Don't Stop Til You Get Enough",
    page_icon="🎰",
    layout="wide",
)

# Session state initialization
if "current_page" not in st.session_state:
    st.session_state.current_page = "Home"

if "game_config" not in st.session_state:
    st.session_state.game_config = None

if "model_config" not in st.session_state:
    st.session_state.model_config = None


def main():
    """Main application entry point."""

    # Sidebar navigation
    st.sidebar.title("🎰 Don't Stop Til You Get Enough")

    pages = ["Home", "Config Jeu", "Config Modèle", "Batch Run", "Résultats"]
    selected_page = st.sidebar.radio("Navigation", pages)

    # Route to selected page
    if selected_page == "Home":
        show_home()
    elif selected_page == "Config Jeu":
        show_game_config()
    elif selected_page == "Config Modèle":
        show_model_config()
    elif selected_page == "Batch Run":
        show_batch_run()
    elif selected_page == "Résultats":
        show_results()


def show_home():
    """Home page."""
    st.title("🎰 Don't Stop Til You Get Enough")
    st.markdown("""
    ## Analyse et prédiction des jeux de hasard

    Ce programme vous permet d'analyser différents modèles de prédiction
    sur les jeux de la Française des Jeux (Loto, Euromillion).

    ### Fonctionnalités

    - **Analyse historique** : Testez vos modèles sur l'historique des tirages
    - **Prédiction** : Générez des prédictions pour les prochains tirages
    - **Comparaison** : Comparez les performances de différents modèles
    - **ROI** : Calculez le retour sur investissement de chaque stratégie
    """)

    # Quick stats
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Jeux disponibles", "2")
    with col2:
        st.metric("Modèles", "2")
    with col3:
        st.metric("Batchs exécutés", "0")


def show_game_config():
    """Game configuration page."""
    st.title("⚙️ Configuration du Jeu")

    game_type = st.selectbox("Jeu", ["Loto", "Euromillion"])

    if game_type == "Loto":
        show_loto_config()
    else:
        show_euromillion_config()


def show_loto_config():
    """Loto-specific configuration."""
    st.subheader("Paramètres Loto")

    loto_type = st.selectbox("Type de Loto", ["Loto", "Grand-Loto", "Super-Loto"])

    prices = {"Loto": 2.20, "Grand-Loto": 3.00, "Super-Loto": 5.00}

    prix_grille = st.number_input(
        "Prix de la grille (€)", min_value=0.0, value=prices[loto_type], step=0.10
    )

    # Double slider for grilles range
    grille_range = st.slider(
        "Nombre de grilles",
        min_value=1,
        max_value=1000,
        value=(1, 10),
        help="Sélectionnez une valeur ou une plage",
    )

    second_tirage = st.radio(
        "2nd tirage",
        [False, True, "both"],
        format_func=lambda x: (
            "Désactivé" if x is False else "Activé" if x is True else "Les deux"
        ),
    )

    prix_second = st.number_input(
        "Prix 2nd tirage (€)", min_value=0.0, value=0.80, step=0.10
    )

    # Date range for historical draws
    st.subheader("Tirages historiques")
    date_range = st.date_input(
        "Plage de dates",
        value=[],
        help="Sélectionnez la plage de dates pour les tirages historiques",
    )

    include_future = st.checkbox("Inclure le prochain tirage")

    if st.button("Valider la configuration"):
        st.session_state.game_config = {
            "type": loto_type,
            "prix_grille": prix_grille,
            "nombre_grilles": grille_range,
            "second_tirage": second_tirage,
            "prix_second_tirage": prix_second,
            "tirages_historiques": date_range,
            "tirages_futurs": include_future,
        }
        st.success("Configuration du jeu enregistrée!")


def show_euromillion_config():
    """Euromillion-specific configuration."""
    st.subheader("Paramètres Euromillion")

    prix_grille = st.number_input(
        "Prix de la grille (€)", min_value=0.0, value=2.50, step=0.10
    )

    grille_range = st.slider(
        "Nombre de grilles",
        min_value=1,
        max_value=1000,
        value=(1, 10),
        help="Sélectionnez une valeur ou une plage",
    )

    etoile_plus = st.radio(
        "Etoile+",
        [False, True, "both"],
        format_func=lambda x: (
            "Désactivé" if x is False else "Activé" if x is True else "Les deux"
        ),
    )

    prix_etoile = st.number_input(
        "Prix Etoile+ (€)", min_value=0.0, value=1.00, step=0.10
    )

    st.subheader("Tirages historiques")
    date_range = st.date_input(
        "Plage de dates",
        value=[],
        help="Sélectionnez la plage de dates pour les tirages historiques",
    )

    include_future = st.checkbox("Inclure le prochain tirage")

    if st.button("Valider la configuration"):
        st.session_state.game_config = {
            "prix_grille": prix_grille,
            "nombre_grilles": grille_range,
            "etoile_plus": etoile_plus,
            "prix_etoile_plus": prix_etoile,
            "tirages_historiques": date_range,
            "tirages_futurs": include_future,
        }
        st.success("Configuration du jeu enregistrée!")


def show_model_config():
    """Model configuration page."""
    st.title("🎯 Configuration du Modèle")

    model_type = st.selectbox("Modèle", ["Random", "SameValue"])

    if model_type == "Random":
        show_random_config()
    else:
        show_same_value_config()


def show_random_config():
    """Random model configuration."""
    st.subheader("Paramètres Random")

    seed_type = st.selectbox(
        "Type de seed",
        ["timestamp", "fixed"],
        format_func=lambda x: "Timestamp" if x == "timestamp" else "Valeur fixe",
    )

    if st.button("Valider le modèle"):
        st.session_state.model_config = {
            "name": "Random",
            "seed_type": seed_type,
        }
        st.success("Configuration du modèle enregistrée!")


def show_same_value_config():
    """SameValue model configuration."""
    st.subheader("Paramètres SameValue")

    # Check which game is configured
    game_config = st.session_state.get("game_config")

    is_euromillion = game_config and "etoile_plus" in str(game_config)

    if is_euromillion:
        # Euromillion numbers
        st.markdown("#### Numéros (1-50)")
        cols = st.columns(5)
        numeros = []
        for i, col in enumerate(cols):
            with col:
                numeros.append(
                    st.number_input(
                        f"Numéro {i + 1}",
                        min_value=1,
                        max_value=50,
                        value=i + 1,
                        key=f"num{i}",
                    )
                )

        st.markdown("#### Étoiles (1-12)")
        cols = st.columns(2)
        etoiles = []
        for i, col in enumerate(cols):
            with col:
                etoiles.append(
                    st.number_input(
                        f"Étoile {i + 1}",
                        min_value=1,
                        max_value=12,
                        value=i + 1,
                        key=f"etoile{i}",
                    )
                )
    else:
        # Loto numbers
        st.markdown("#### Numéros (1-49)")
        cols = st.columns(5)
        numeros = []
        for i, col in enumerate(cols):
            with col:
                numeros.append(
                    st.number_input(
                        f"Numéro {i + 1}",
                        min_value=1,
                        max_value=49,
                        value=i + 1,
                        key=f"num{i}",
                    )
                )

        st.markdown("#### Numéro complémentaire (1-10)")
        numero_comp = st.number_input(
            "Numéro complémentaire", min_value=1, max_value=10, value=6
        )

    if st.button("Valider le modèle"):
        if is_euromillion:
            st.session_state.model_config = {
                "name": "SameValue",
                "is_euromillion": True,
                "numeros": numeros,
                "etoiles": etoiles,
            }
        else:
            st.session_state.model_config = {
                "name": "SameValue",
                "is_euromillion": False,
                "numeros": numeros,
                "numero_comp": numero_comp,
            }
        st.success("Configuration du modèle enregistrée!")


def show_batch_run():
    """Batch execution page."""
    st.title("🚀 Lancement des Batchs")

    st.info("Cette page permettra de lancer les batchs de prédiction.")

    # Show current configuration
    if st.session_state.game_config:
        st.json(st.session_state.game_config)
    else:
        st.warning("Veuillez d'abord configurer le jeu.")

    if st.session_state.model_config:
        st.json(st.session_state.model_config)
    else:
        st.warning("Veuillez d'abord configurer le modèle.")


def show_results():
    """Results page."""
    st.title("📊 Résultats")

    st.info("Cette page affichera les résultats et comparaisons.")


if __name__ == "__main__":
    main()

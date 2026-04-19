
import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

# ── Client Groq ──────────────────────────────────────────────
_client = None

def get_client():
    global _client
    if _client is None:
        api_key = os.getenv("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", "")
        if not api_key:
            raise ValueError(
                "GROQ_API_KEY manquant. "
                "Ajoutez-le dans Streamlit Cloud : Settings > Secrets.\n"
                "[secrets]\nGROQ_API_KEY = 'gsk_xxxxx'"
            )
        _client = Groq(api_key=api_key)
    return _client


MODEL = "llama3-8b-8192"   # gratuit sur groq.com, 8k context

# ── Fonction d'appel générique ────────────────────────────────
def call_agent(system_prompt: str, user_prompt: str) -> str:
    """Appelle le LLM Groq avec un rôle système et un message utilisateur."""
    try:
        client = get_client()
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user",   "content": user_prompt},
            ],
            temperature=0.3,
            max_tokens=1024,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"⚠️ Erreur agent : {e}"


# ── Définition des agents (system prompts) ────────────────────
AGENTS = {
    "Marketing": (
        "Tu es un expert Marketing S&OP. Tu analyses la demande, identifies "
        "les tendances, les produits à fort potentiel et les risques marché. "
        "Tu donnes 3 recommandations prioritaires numérotées, claires et chiffrées."
    ),
    "Ventes": (
        "Tu es un expert Ventes S&OP. Tu valides les volumes commerciaux, "
        "compares Forecast vs Sales_Orders, signales les écarts > 15% "
        "et proposes des actions correctives concrètes."
    ),
    "Supply": (
        "Tu es un expert Supply Chain S&OP. Tu analyses les contraintes de "
        "production, identifies chaque goulot, sa cause probable et une "
        "solution chiffrée (ex: +X heures sup = +Y unités)."
    ),
    "Achats": (
        "Tu es un expert Achats S&OP. Tu évalues les risques fournisseurs, "
        "classes les fournisseurs par niveau de risque et proposes un plan "
        "d'action pour les lead times > 45 jours."
    ),
    "Finance": (
        "Tu es un expert Finance S&OP. Tu calcules la rentabilité "
        "(Profit = Volume × Marge), donnes le ROI du plan et l'impact "
        "sur le cash-flow de façon précise et chiffrée."
    ),
    "Rapport": (
        "Tu es l'orchestrateur S&OP. Tu synthétises les analyses de tous les "
        "départements et rédiges un rapport S&OP final structuré en 5 sections :\n"
        "1. SYNTHÈSE EXÉCUTIVE (3 lignes max)\n"
        "2. ANALYSE OFFRE / DEMANDE\n"
        "3. IMPACT FINANCIER (chiffré)\n"
        "4. TABLEAU DE DÉCISION (tableau markdown avec colonnes : "
        "Produit | Décision | Action | Responsable | Délai | Impact Marge)\n"
        "5. RECOMMANDATION FINALE (Feu vert / Réserves / Veto avec conditions)"
    ),
}


def run_agent(agent_name: str, data_text: str, contexte: str = "") -> str:
    """Lance un agent nommé avec les données fournies."""
    system = AGENTS.get(agent_name, "Tu es un expert S&OP.")
    user   = f"Contexte : {contexte}\n\nDonnées :\n{data_text}"
    return call_agent(system, user)


def run_all_agents(txt_mkt: str, txt_prod: str, txt_fin: str,
                   focus: str, contexte: str) -> dict:
    """
    Lance les 6 agents séquentiellement et retourne un dict {nom: réponse}.
    """
    results = {}

    # Agents opérationnels
    results["Marketing"] = run_agent(
        "Marketing",
        f"Focus : {focus}\nDemande :\n{txt_mkt}",
        contexte
    )
    results["Ventes"] = run_agent(
        "Ventes",
        f"Focus : {focus}\nDemande :\n{txt_mkt}",
        contexte
    )
    results["Supply"] = run_agent(
        "Supply",
        f"Focus : {focus}\nProduction :\n{txt_prod}",
        contexte
    )
    results["Achats"] = run_agent(
        "Achats",
        f"Focus : {focus}\nFinance/Achats :\n{txt_fin}",
        contexte
    )
    results["Finance"] = run_agent(
        "Finance",
        f"Focus : {focus}\nFinance/Achats :\n{txt_fin}",
        contexte
    )

    # Rapport final — synthèse de tous les agents
    synthese = "\n\n".join(
        f"=== {k} ===\n{v}" for k, v in results.items()
    )
    results["Rapport"] = run_agent(
        "Rapport",
        f"Focus : {focus}\n\nSynthèses des agents :\n{synthese}\n\n"
        f"Données brutes — Demande :\n{txt_mkt}\n"
        f"Production :\n{txt_prod}\nFinance :\n{txt_fin}",
        contexte
    )

    return results

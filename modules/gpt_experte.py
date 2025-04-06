
import openai
import streamlit as st

client = openai.OpenAI(api_key=st.secrets["openai"]["api_key"])

def experteneinschaetzung_gpt(finanzdaten: dict, lageinfo: dict):
    system_prompt = (
        "Du bist ein Immobilienfinanzierungsexperte. "
        "Bewerte die Tragfähigkeit und Wirtschaftlichkeit folgender Immobilienfinanzierung. "
        "Berücksichtige alle Finanzkennzahlen, Steuervorteile, Mieteinnahmen und reale Belastung. "
        "Beziehe auch die Lageinformationen ein (Stadt, Region, Qualität, Marktumfeld). "
        "Weise auf Risiken hin, nenne Verbesserungsvorschläge und vergleiche mit typischen Finanzierungskonzepten."
    )

    lage_text = ", ".join(f"{k} = {v}" for k, v in lageinfo.items())
    user_prompt = f"""Eckdaten der Finanzierung:
    {finanzdaten}
    
    Lage der Immobilie:
    {lage_text}
    """


    try:
        response = client.chat.completions.create(
            # model="gpt-3.5-turbo",
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7,
            max_tokens=800
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Fehler beim Abrufen der Experteneinschätzung: {e}"

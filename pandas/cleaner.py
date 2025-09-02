import pandas as pd
import json

# Lê o JSON original
df = pd.read_json("../output/pokemons.json")

# Função auxiliar para limpar listas (remover duplicatas mantendo a ordem)
def clean_list(x):
    if isinstance(x, list):
        seen = set()
        return [i for i in x if not (i in seen or seen.add(i))]
    return x

# Função auxiliar para limpar evoluções
def clean_evolution(evolutions, name):
    if isinstance(evolutions, list):
        cleaned = []
        seen = set()
        for evo in evolutions:
            if isinstance(evo, dict):
                evo_name = evo.get("name")
                # remove evolução para ele mesmo
                if evo_name == name:
                    continue
                # evita duplicatas
                evo_tuple = (evo_name, evo.get("variant"))
                if evo_tuple not in seen:
                    seen.add(evo_tuple)
                    cleaned.append(evo)
        return cleaned
    return evolutions

# Aplicando as limpezas
df["types"] = df["types"].apply(clean_list)
df["abilities"] = df["abilities"].apply(clean_list)
df["evolution"] = df.apply(lambda row: clean_evolution(row["evolution"], row["name"]), axis=1)

# Exporta para um novo JSON
df.to_json("./pokemons_clean.json", orient="records", indent=2, force_ascii=False)

print("✅ Arquivo 'pokemons_clean.json' gerado com sucesso!")

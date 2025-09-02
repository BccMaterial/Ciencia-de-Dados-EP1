import pandas as pd
import json

#Lê o arquivo json
df = pd.read_json("../output/pokemons.json")

#Remove duplicata de listas mantendo a ordem
def clean_list(x):
    if isinstance(x, list): #isinstance verifica se evolutions é do tipo list
        seen = set() #Sets não permitem repetição de elementos e ajudam a fazer a checagem de duplicatas rapidamente
        return [i for i in x if not (i in seen or seen.add(i))] #.add() sempre retorna None(None em um if é considerado falso)
    return x


def clean_evolution(evolutions, name):
    if isinstance(evolutions, list): 
        cleaned = []
        seen = set() 
        for evo in evolutions:
            if isinstance(evo, dict):
                evo_name = evo.get("name")
                #Caso contenha evolução para si mesmo, remove
                if evo_name == name:
                    continue
                
                evo_tuple = (evo_name, evo.get("variant"))
                if evo_tuple not in seen:
                    seen.add(evo_tuple)
                    cleaned.append(evo)
        return cleaned
    return evolutions

#Limpeza:
df["types"] = df["types"].apply(clean_list)
df["abilities"] = df["abilities"].apply(clean_list)
df["evolution"] = df.apply(lambda row: clean_evolution(row["evolution"], row["name"]), axis=1)

#Exporta de data frame para json novamente:
df.to_json("./pokemons_clean.json", orient="records", indent=2, force_ascii=False)

print("Arquivo gerado com sucesso")

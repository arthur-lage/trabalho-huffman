import os
import re
import huffman

# Função que limpa o texto e o separa em uma lista de palavras
def tokenizer(text):
    """Limpa o texto e constrói uma lista de palavras."""
    clean_text = re.sub(r'[^\w\s]', ' ', text.lower())
    words = clean_text.split(" ")
    return words
        
# Função que calcula a frequência de cada palavra e retorna um dicionário
def calculate_frequency(words):
    """Calcula a frequência de cada palavra e retorna um dicionário."""
    f = {}
    for word in words:
        f[word] = f.get(word, 0) + 1

    return f

def main():
    os.makedirs(name="data", exist_ok=True)

    try:
        with open("data/input.dat", "r") as f:
            content = f.read()
    except FileNotFoundError:
        print("ERRO: Não foi possível encontrar o arquivo 'data/input.dat'.")
        return
    
    # Separa os textos por linha em branco
    text_parts = [t.strip() for t in content.split('\n\n') if t.strip()]
    
    if not text_parts:
        print("AVISO: Nenhum texto encontrado no input.dat.")
        return
    
    with open("data/output.dat", "w", encoding="utf-8") as out:
        for i, original in enumerate(text_parts):
            out.write(f"========= TEXTO {i+1} =========\n\n")
            
            # quebra a frase em palavras minusculas e sem pontuações.
            tokens = tokenizer(original)
            
            if not tokens:
                print("Esse texto não possui palavras válidas.\n\n")
                continue
            
            # conta as palavras mais frequentes
            frequencies = calculate_frequency(tokens)

            # cria a árvore de huffman
            tree = huffman.build_tree(frequencies)
            
            # gera a tabela de codigos de huffman
            code_table = huffman.generate_codes(tree)
            
            # gera o texto codificado
            encoded_text = huffman.encode_text(tokens, code_table)
            
            # mostra a estrutura da árvore, com: raiz, direita, esquerda
            out.write("1 - Estrutura da Árvore \n")
            out.write(huffman.huffman_tree_to_string(tree) + "\n\n")
            
            out.write("2 - Tabela de Códigos: \n")
            for symbol, code in sorted(code_table.items(), key=lambda item: len(item[1])):
                out.write(f"'{symbol}': {code}\n")
            out.write("\n")

            out.write("3 - Texto Codificado: \n")
            out.write(encoded_text + "\n\n")

if __name__ == "__main__":
    main()
    print("✅ Processamento concluído.")
    print("ℹ️  Verifique 'data/output.dat' para os resultados da compressão.")
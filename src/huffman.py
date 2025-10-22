import heapq


class Node:
    """Classe responsável por representar os nós da árvore binária no algoritmo de Huffman"""
    def __init__(self, symbol, frequency, left=None, right=None):
        self.symbol = symbol
        self.frequency = frequency
        self.left = left
        self.right = right

    def __lt__(self, other):
        return self.frequency < other.frequency

    def is_leaf(self):
        return self.left is None and self.right is None

def build_tree(frequencies):
    """Constrói a árvore baseada na frequência de cada palavra no texto"""
    priority_queue = []
    
    # Monta árvore usando heapq, implementação de um min-heap.
    # Essa estrutura é ótima para Huffman, já que permite acesso eficiente
    # aos elementos de menor frequência.
    for symbol, freq in frequencies.items():
        heapq.heappush(priority_queue, Node(symbol, freq))
        
    if not priority_queue:
        return None
    
    if len(priority_queue) == 1:
        root = Node(None, priority_queue[0].frequency)
        root.left = heapq.heappop(priority_queue)
        return root

    while len(priority_queue) > 1:
        n1 = heapq.heappop(priority_queue)
        n2 = heapq.heappop(priority_queue)
        
        new_node = Node(None, n1.frequency + n2.frequency)
        new_node.left = n1
        new_node.right = n2
        
        heapq.heappush(priority_queue, new_node)

    return priority_queue[0]
    
def generate_codes(root, curr="", code_table=None):
    """Cria a tabela de códigos ao percorrer a árvore. 0 - Esquerda, 1 - Direita."""
    
    if code_table is None:
        code_table = {}
    
    if root is None:
        return code_table
    
    if root.symbol is not None:
        if not curr:
            code_table[root.symbol] = '0'
        else:
            code_table[root.symbol] = curr
            
        return code_table
        
    generate_codes(root.left, curr + "0", code_table)
    generate_codes(root.right, curr + "1", code_table)
    return code_table

        
def huffman_tree_to_string(root, code="", prefix="", is_left=True):
    """
    Retorna a representação em string da árvore de Huffman
    """
    if root is None:
        return ""
    
    result = ""
    
    if root.is_leaf():
        symbol_display = f"'{root.symbol}'" if root.symbol else "EOF"
        result += f"{prefix}{'├── ' if not is_left else '└── '}{symbol_display} (freq: {root.frequency}, código: '{code}')\n"
    else:
        result += f"{prefix}{'├── ' if not is_left else '└── '}Interno (freq: {root.frequency})\n"
    
    new_prefix = prefix + ("│   " if not is_left else "    ")
    
    if root.right:
        result += huffman_tree_to_string(root.right, code + "1", new_prefix, False)
    if root.left:
        result += huffman_tree_to_string(root.left, code + "0", new_prefix, True)
    
    return result
        
def encode_text(words, code_table):
    """Transforma as palavras desejadas na versão codificada."""
    
    encoded = ""
    for word in words:
        if word in code_table:
            encoded += code_table[word]
    
    return encoded
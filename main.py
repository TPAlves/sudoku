import random,requests, json;


def eValido(sudoku, linha, coluna, numero):
    # Verefica se o numero já existe na linha ou coluna
    for x in range(9):
        if sudoku[linha][x] == numero or sudoku[x][coluna] == numero:
            return False;
    
    # Verifica se o número existe no 3x3
    linha_inicial = linha - linha % 3;
    coluna_inicial = coluna - coluna % 3;
    
    for i in range(3):
        for j in range(3):
            if sudoku[i + linha_inicial][j + coluna_inicial] == numero:
                return False;
    
    return True;

def resolve_sudoku(sudoku, linha=0, coluna=0):
    if linha == 9: # Se chegou a última linha, o sudoku está resolvido
        return True;
    
    if coluna == 9:
        return resolve_sudoku(sudoku,linha + 1, 0);
    
    if sudoku[linha][coluna] != 0: # Se a célula já está preenchida, passamos para a próxima
        return resolve_sudoku(sudoku,linha, coluna +1);
    
    for numero in random.sample(range(1,10),9): # Testando números de 1 a 9 em ordem aleatória 
        if eValido(sudoku,linha,coluna,numero):
            sudoku[linha][coluna] = numero;

            if resolve_sudoku(sudoku,linha,coluna + 1):
                return True;
        
        sudoku[linha][coluna] = 0
        
    return False;


def conexao_api():
    request = requests.get("https://sudoku-api.vercel.app/api/dosuku");
    data = json.loads(request.content);
    return data;

def gera_sudoku():
    data = conexao_api();
    sudoku_api = data['newboard']['grids'][0]['value'];
    dificuldade = data['newboard']['grids'][0]['difficulty'];
    solucao_api = data['newboard']['grids'][0]['solution']
    sudoku = (sudoku_api, dificuldade, solucao_api);
    return sudoku;


sudoku = gera_sudoku(); 

print(""" 
███████╗██╗   ██╗██████╗  ██████╗ ██╗  ██╗██╗   ██╗
██╔════╝██║   ██║██╔══██╗██╔═══██╗██║ ██╔╝██║   ██║
███████╗██║   ██║██║  ██║██║   ██║█████╔╝ ██║   ██║
╚════██║██║   ██║██║  ██║██║   ██║██╔═██╗ ██║   ██║
███████║╚██████╔╝██████╔╝╚██████╔╝██║  ██╗╚██████╔╝
╚══════╝ ╚═════╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ 
""")

print(f"Dificuldade: {sudoku[1]}\n");

print("Antes da solução: ");

for linha in sudoku[0]:
    print(linha);
print("\n-------------------------\n");

print("Solucionado: ");

resolve_sudoku(sudoku[0]);
for linha in sudoku[0]:
    print(linha);
print("\n-------------------------\n");

print("Solução da API: ")
for linha in sudoku[2]:
    print(linha);

# 📊 ANÁLISE COMPLETA DO PROJETO - IMPORTAÇÃO DE FRETES

## 1️⃣ OBJETIVO DA APLICAÇÃO: FastLog

**FastLog** é um sistema de rastreamento de pedidos de entrega para a UNIVESP.

### Fluxo Principal:
```
Usuário acessa www.localhost:8000
        ↓
Insere CNPJ e NFE do pedido
        ↓
Sistema consulta banco de dados
        ↓
Mostra status: ENTREGUE ou PENDENTE
```

---

## 2️⃣ ESTRUTURA DO ARQUIVO EXCEL

Arquivo: `VALORES DE FRETE 2.6 - TESTE LEANDRO.xlsx`

### 🗂️ ABA 1: "FRETES CONSOLIDADA"
**É a aba PRINCIPAL que será importada para o banco de dados**

Contém dados de fretes reais com as seguintes colunas:

| Coluna | Tipo | Descrição | Exemplo |
|--------|------|-----------|---------|
| **TRANSPORTADORA** | Texto | Nome da empresa transportadora | "TAF", "ALFA" |
| **DT. PEDIDO** | Data | Data em que o pedido foi realizado | 2024-01-03 |
| **DT. COLETA** | Data | Data em que a transportadora coletou | 2024-01-08 |
| **DT. ENTREGA** | Data | Data em que chegou ao destino | 2024-01-12 |
| **TEMPO ENT.** | Número | Dias de entrega (DT. ENTREGA - DT. COLETA) | 4 |
| **NFE** | Número | Número da Nota Fiscal Eletrônica | 3945, 3946 |
| **RAZAO SOCIAL** | Texto | Nome da empresa cliente | "ARMARINHOS FERNANDO LTDA" |
| **CIDADE** | Texto | Cidade de destino | "OSASCO", "SÃO PAULO" |
| **UF** | Texto | Estado de destino (2 letras) | "SP", "MG", "GO" |
| **PAÍS** | Texto | País de destino | "BRASIL" |
| **VALOR PEDIDO** | Moeda | Valor total do pedido | 4.588,00 |
| **VALOR FRETE** | Moeda | Valor cobrado de frete | 300,00 |
| Outras... | Diversos | Colunas calculadas | (ignorar) |

---

### 🗂️ ABA 2: "Base NUNOTA" (19.445 linhas)
**Mapeamento auxiliar (não será usada agora)**
- Nro. Único ↔ Nro. Nota
- Seria útil para relacionar com outros sistemas

---

### 🗂️ ABA 3: "MUNICÍPIOS-UF" (5.570 linhas)
**Base de referência de localidades brasileiras**

Útil para:
- Validar se a CIDADE + UF existe
- Encontrar código IBGE do município
- Corrigir digitação de cidades

Formato:
| UF | COD. UF | COD. MUNIC | NOME DO MUNICÍPIO |
|----|---------|-----------|----|
| SP | 35 | 7107 | SÃO PAULO |
| MG | 31 | 3141 | BELO HORIZONTE |

---

### 🗂️ ABA 4: "TRANSPORTADORAS" (32 linhas)
**Lista de transportadoras cadastradas**

Apenas nomes:
- ALFA
- ATUAL CARGAS
- BARONI
- JET
- TAF
- (etc...)

---

## 3️⃣ MODELOS DE BANCO DE DADOS DJANGO

Seu banco de dados foi criado com estes modelos:

```
┌─────────────────────────────────────────────┐
│                   PAÍS                       │
├─────────────────────────────────────────────┤
│ id (auto)                                   │
│ name: "BRASIL", "EUA", etc                  │
└──────────────┬────────────────────────────┘
               │ (1:N)
               ├────────────────────────────┐
               ▼                            ▼
    ┌──────────────────────┐    ┌──────────────────────┐
    │      ESTADO          │    │      ESTADO          │
    ├──────────────────────┤    ├──────────────────────┤
    │ id: "SP" (PK)        │    │ id: "MG" (PK)        │
    │ name: "São Paulo"    │    │ name: "Minas Gerais" │
    │ country_id: 1        │    │ country_id: 1        │
    └──────┬───────────────┘    └──────┬───────────────┘
           │ (1:N)                    │ (1:N)
           ▼                          ▼
    ┌──────────────────────┐    ┌──────────────────────┐
    │      CIDADE          │    │      CIDADE          │
    ├──────────────────────┤    ├──────────────────────┤
    │ id (auto)            │    │ id (auto)            │
    │ name: "São Paulo"    │    │ name: "Belo Horiz."  │
    │ state_id: "SP"       │    │ state_id: "MG"       │
    └─────┬────────────────┘    └─────┬────────────────┘
          │ (1:N)                    │ (1:N)
          ├──────────────┬───────────┤
          ▼              ▼           ▼
    ┌─────────────────────────────────────────┐
    │        CLIENTE (Customer)               │
    ├─────────────────────────────────────────┤
    │ id (auto)                               │
    │ name: "ARMARINHOS FERNANDO LTDA"        │
    │ code: "12345"                           │
    │ cnpj: "00000000000000" (vazio/padrão)   │
    │ city_id: → City                         │
    └──────────────┬────────────────────────┘
                   │ (1:N)
                   ▼
    ┌─────────────────────────────────────────┐
    │    PEDIDO (Order) ← DADOS PRINCIPAIS   │
    ├─────────────────────────────────────────┤
    │ id (auto)                               │
    │ nfe: "3945"                             │
    │ order_date: 2024-01-03                  │
    │ delivery_date: 2024-01-12               │
    │ status: "ENTREGUE"                      │
    │ customer_id: → Customer                 │
    │ carrier_id: → Carrier                   │
    └─────────────────────────────────────────┘
           ▲
           │ (N:1)
           │
    ┌──────┴───────────────────────────────────┐
    │    TRANSPORTADORA (Carrier)              │
    ├─────────────────────────────────────────┤
    │ id (auto)                               │
    │ name: "TAF"                             │
    │ cnpj: "00000000000000" (vazio/padrão)   │
    │ city_id: → City                         │
    └─────────────────────────────────────────┘
```

---

## 4️⃣ MAPEAMENTO: EXCEL → BANCO DE DADOS

Quando você fizer upload do Excel, cada linha da aba "FRETES CONSOLIDADA" será processada assim:

### Exemplo: Linha do Excel

```
TRANSPORTADORA: "TAF"
DT. PEDIDO:     2024-01-03
DT. COLETA:     2024-01-08
DT. ENTREGA:    2024-01-12
NFE:            3945
RAZAO SOCIAL:   "ARMARINHOS FERNANDO LTDA"
CIDADE:         "OSASCO"
UF:             "SP"
PAÍS:           "BRASIL"
```

### Processo de Importação (Passo a Passo):

```
1️⃣ PAÍS
   ├─ Procura país "BRASIL" no banco
   ├─ Se não existe → CRIA
   └─ Resultado: country_id = 1 (BRASIL)

2️⃣ ESTADO
   ├─ Procura estado "SP" no banco
   ├─ Se não existe → CRIA (vinculado ao BRASIL)
   └─ Resultado: state_id = "SP"

3️⃣ CIDADE
   ├─ Procura cidade "OSASCO" + estado "SP" no banco
   ├─ Se não existe → CRIA (vinculada ao SP)
   └─ Resultado: city_id = 123 (exemplo)

4️⃣ CLIENTE
   ├─ Procura cliente com nome "ARMARINHOS FERNANDO LTDA" no banco
   ├─ Se não existe → CRIA (vinculado à cidade OSASCO)
   └─ Resultado: customer_id = 456 (exemplo)

5️⃣ TRANSPORTADORA
   ├─ Procura transportadora "TAF" no banco
   ├─ Se não existe → CRIA (precisa de city, pode ser a origem ou um padrão)
   └─ Resultado: carrier_id = 789 (exemplo)

6️⃣ PEDIDO (Order)
   └─ CRIA novo pedido com:
      ├─ nfe: "3945"
      ├─ order_date: 2024-01-03
      ├─ delivery_date: 2024-01-12
      ├─ status: "ENTREGUE" (porque tem data de entrega)
      ├─ customer_id: 456
      └─ carrier_id: 789
```

---

## 5️⃣ SITUAÇÕES ESPECIAIS A TRATAR

### ⚠️ Problema 1: Cidade pode não estar na base
**Se:** "OSASCO" + "SP" não existe em CITY
**Solução:** 
- Opção A: Criar automaticamente (mais simples)
- Opção B: Consultar MUNICÍPIOS-UF e validar (mais seguro)
- Opção C: Registrar erro e pular a linha

### ⚠️ Problema 2: Status do Pedido não vem no Excel
**Como saber se está ENTREGUE ou PENDENTE?**
```
IF DT. ENTREGA não é vazio:
   status = "ENTREGUE"
ELSE:
   status = "PENDENTE"
```

### ⚠️ Problema 3: NFE pode repetir
**Se:** Mesma NFE aparece em 2 linhas diferentes
**Solução:** 
- Opção A: Atualizar o pedido existente
- Opção B: Criar error log
- Opção C: Ignorar duplicata

### ⚠️ Problema 4: CNPJ não vem no Excel
**Cliente e Transportadora não têm CNPJ**
**Solução:**
- Deixar campo vazio ("")
- Ou preenchimento manual depois

### ⚠️ Problema 5: Cidade origem da Transportadora
**Carrier precisa de city_id, mas não sabemos de onde é a transportadora**
**Solução:**
- Usar a cidade de destino (não ideal, mas funciona)
- Ou criar uma cidade fictícia "ORIGEM"
- Ou deixar como NULL (se permitir)

---

## 6️⃣ CÓDIGO ATUAL VS O QUE PRECISA SER FEITO

### Arquivo Atual: `order_excel_import.py`

```python
class OrderExcelImportService:
    
    def importfile(self, file):
        if not file:
            raise ValueError("Nenhum arquivo fornecido.")
        
        #TODO: importação da planilha excel com os pedidos
        
        # Se o arquivo for válido, ele será processado       
        
        #le linhas       
        # valida
        # se ok, insere
        # se não ok, insere na planilha de erros
```

### Precisa Implementar:

1. **Leitura do Excel**
   - Usar `pandas` ou `openpyxl` para ler arquivo
   - Extrair aba "FRETES CONSOLIDADA"
   - Iterar sobre as linhas

2. **Validações**
   - Verificar campos obrigatórios (NFE, RAZAO SOCIAL, CIDADE, UF, DT. PEDIDO)
   - Validar formato de datas
   - Verificar se UF tem 2 caracteres
   - Verificar se NFE já existe

3. **Criação de Hierarquia**
   - Country → State → City (em cadeia)
   - Customer (vinculado à City)
   - Carrier (vinculado à City)

4. **Criação de Order**
   - Inserir novo Order com os dados mapeados
   - Definir status corretamente

5. **Tratamento de Erros**
   - Registrar linhas com problemas
   - Retornar relatório de sucesso/erro
   - Rollback em caso de falha crítica

---

## 7️⃣ FLUXO VISUAL COMPLETO

```
┌─────────────────────────────────────────┐
│ Usuário faz upload do arquivo Excel     │
│ "VALORES DE FRETE 2.6 - TESTE LEANDRO"  │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│ Django Admin → Botão "Upload Planilha"  │
│ → admin_orderadmin.py (upload method)   │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│ OrderExcelImportService.importfile()    │
│ ← AQUI VAI TODA LÓGICA DE IMPORTAÇÃO    │
└──────────────┬──────────────────────────┘
               │
               ├──→ Lê arquivo Excel
               ├──→ Para cada linha:
               │    ├──→ Cria/Busca Country
               │    ├──→ Cria/Busca State
               │    ├──→ Cria/Busca City
               │    ├──→ Cria/Busca Customer
               │    ├──→ Cria/Busca Carrier
               │    ├──→ Cria Order
               │    ├──→ Registra sucesso ou erro
               │
               ▼
┌─────────────────────────────────────────┐
│ Banco de dados atualizado com novos     │
│ Pedidos, Clientes, Transportadoras, etc │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│ Usuário pode consultar pedidos via      │
│ www.localhost:8000/tracking/orders/     │
│ Informando CNPJ e NFE                   │
└─────────────────────────────────────────┘
```

---

## ✅ PRÓXIMAS AÇÕES

Vamos implementar a lógica de importação **passo a passo**:

1. ✅ **Entender a estrutura** (FEITO)
2. ⏳ **Implementar leitura do Excel**
3. ⏳ **Implementar validações**
4. ⏳ **Implementar criação de hierarquia (Country→State→City)**
5. ⏳ **Implementar criação de Customer e Carrier**
6. ⏳ **Implementar criação de Order**
7. ⏳ **Testar com arquivo real**
8. ⏳ **Tratar casos especiais e erros**

---

**Você quer que comecemos a implementação?**
Quando estiver pronto, me avise qual passo quer que implementemos primeiro!
## ✅ PASSO 1: LEITURA DO EXCEL - CONCLUÍDO!

### Resultado do Teste:
`
================================================================================
🧪 TESTE DO PASSO 1: LEITURA DO EXCEL
================================================================================
📁 Arquivo encontrado: VALORES DE FRETE 2.6 - TESTE LEANDRO.xlsx
📖 Lendo arquivo Excel...
✅ Arquivo lido com sucesso!
   📊 Shape: 99 linhas, 17 colunas
   📋 Colunas encontradas: ['TRANSPORTADORA', 'DT. PEDIDO', 'DT. COLETA', 'DT. ENTREGA', 'TEMPO ENT.', 'NFE', 'RAZAO SOCIAL', 'CIDADE', 'UF', 'PAÍS', 'VALOR PEDIDO', 'VALOR FRETE', 'VALOR %', 'C', 'TDE', 'C, E, R, D', 'OBSERVAÇÃO']

🔍 PRIMEIRAS 3 LINHAS:
  TRANSPORTADORA DT. PEDIDO DT. COLETA DT. ENTREGA  TEMPO ENT.    NFE              RAZAO SOCIAL     CIDADE  UF    PAÍS  VALOR PEDIDO  VALOR FRETE   VALOR %  C  TDE  C, E, R, D  OBSERVAÇÃO
0            TAF 2024-01-03 2024-01-08  2024-01-12           4   3945  ARMARINHOS FERNANDO LTDA     OSASCO  SP  BRASIL       4588.00        300.0  0.065388  C  NaN         NaN         NaN
1            TAF 2024-01-03 2024-01-08  2024-01-12           4   3946  ARMARINHOS FERNANDO LTDA  SÃO PAULO  SP  BRASIL       2013.60        250.0  0.124156  C  NaN         NaN         NaN
2            TAF 2024-01-03 2024-01-08  2024-01-12           4  44071  ARMARINHOS FERNANDO LTDA  SÃO PAULO  SP  BRASIL       3933.96        250.0  0.063549  C  NaN         NaN         NaN

✅ SUCESSO! Arquivo lido com sucesso. 99 linhas encontradas.
`

### O que foi implementado:
1. ✅ **Leitura do Excel** usando pandas
2. ✅ **Extração da aba correta** 'FRETES CONSOLIDADA'
3. ✅ **Identificação de colunas** (17 colunas encontradas)
4. ✅ **Validação de dados** (99 linhas lidas)
5. ✅ **Tratamento de erros** básico
6. ✅ **Retorno estruturado** com sucesso/falha

### Código implementado em order_excel_import.py:
`python
def importfile(self, file):
    try:
        # PASSO 1: Ler arquivo Excel com pandas
        df = pd.read_excel(file, sheet_name='FRETES CONSOLIDADA')
        
        print(f'✅ Arquivo lido com sucesso!')
        print(f'   📊 Shape: {df.shape[0]} linhas, {df.shape[1]} colunas')
        print(f'   📋 Colunas encontradas: {list(df.columns)}')
        
        return {
            'success': True,
            'message': f'Arquivo lido com sucesso. {df.shape[0]} linhas encontradas.',
            'rows_read': df.shape[0],
            'columns': list(df.columns)
        }
    except Exception as e:
        return {
            'success': False,
            'message': f'Erro ao processar arquivo: {str(e)}'
        }
`

---

## 📋 PRÓXIMOS PASSOS

Agora que o **PASSO 1** está funcionando, podemos prosseguir:

1. ✅ ~~Implementar leitura do Excel (pandas para ler arquivo)~~
2. ⏳ **Implementar validações** (verificar dados obrigatórios)
3. ⏳ **Implementar hierarquia de criação** (País → Estado → Cidade)
4. ⏳ **Implementar Cliente e Transportadora**
5. ⏳ **Implementar Pedido**
6. ⏳ **Testar com arquivo real**

**Qual passo você quer implementar agora?** Sugiro o **PASSO 2: VALIDAÇÕES**.

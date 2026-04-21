# 🔍 PASSO 2: Validação de Dados

## O que faz?
Verifica se os dados do Excel estão corretos e completos antes de inserir no banco de dados.

## Como funciona?

### Métodos principais:

#### `_validate_row()` - Valida uma linha individual
```python
def _validate_row(self, row_index, row):
    """Verifica se uma linha tem todos os dados necessários"""
```

**Validações executadas:**

1. **Campos obrigatórios** ✓
   - Verifica se não estão vazios:
     - TRANSPORTADORA, DT. PEDIDO, NFE, RAZAO SOCIAL, CIDADE, UF, PAÍS
   - Cada campo vazio gera um erro

2. **Formato de UF** ✓
   - Valida se tem **exatamente 2 caracteres** (SP, MG, GO, etc)
   - Converte para maiúsculas

3. **Formato de Data** ✓
   - Verifica se DT. PEDIDO é uma data válida
   - Tenta converter com `pd.to_datetime()`

4. **País válido** ✓
   - Verifica se é "BRASIL"
   - Rejeita outros países

5. **NFE válido** ✓
   - Verifica se é um **número inteiro**
   - Tenta converter com `int(nfe)`

#### `_validate_dataframe()` - Valida todo o arquivo
```python
def _validate_dataframe(self, df):
    """Valida todas as linhas do Excel"""
```

**Processo:**

1. Detecta **duplicatas de NFE** (mesma NFE em 2 linhas)
2. Percorre cada linha chamando `_validate_row()`
3. Classifica como **válida** ou **inválida**
4. Armazena erros e sucessos em listas
5. Retorna total de linhas válidas e inválidas

## Resultado esperado

```
🔍 PASSO 2: VALIDANDO DADOS...
   ✅ Linhas válidas: 99
   ❌ Linhas inválidas: 0

✅ VALIDAÇÃO CONCLUÍDA: 99 linhas válidas
```

## Se houver erros

Se alguma linha tiver problema, você vê:
```
⚠️  VALIDAÇÃO ENCONTROU ERROS:
   Linha 5: Campo obrigatório vazio: TRANSPORTADORA, UF inválido: "A"
   Linha 12: NFE duplicada: 3945
```

## Dados retornados

```python
{
    'rows_valid': 99,           # Linhas sem erro
    'rows_invalid': 0,          # Linhas com erro
    'validation_errors': [...], # Lista de erros
    'validation_success': [...]  # Lista de sucessos
}
```

## Próximo passo
Se os dados passaram na validação, eles vão para a **Criação da Hierarquia (Passo 3)** para ser inseridos no banco.

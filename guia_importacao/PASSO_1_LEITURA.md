# 📖 PASSO 1: Leitura do Arquivo Excel

## O que faz?
Lê o arquivo Excel e extrai os dados da aba "FRETES CONSOLIDADA".

## Como funciona?

```python
df = pd.read_excel(file, sheet_name='FRETES CONSOLIDADA')
```

### Passo a passo:

1. **Recebe o arquivo** - A função `importfile()` recebe um arquivo Excel
2. **Valida se existe** - Verifica se o arquivo não é vazio
3. **Lê com pandas** - Usa a biblioteca `pandas` para ler o Excel
4. **Extrai a aba correta** - Especifica `sheet_name='FRETES CONSOLIDADA'`
5. **Carrega em DataFrame** - Armazena em `df` (tabela em memória)
6. **Mostra informações** - Exibe quantas linhas e colunas foram lidas

## Resultado esperado

```
📖 PASSO 1: LENDO ARQUIVO EXCEL...
✅ Arquivo lido com sucesso!
   📊 Shape: 99 linhas, 17 colunas
```

## Dados extraídos

O DataFrame contém 17 colunas:
- TRANSPORTADORA, DT. PEDIDO, DT. COLETA, DT. ENTREGA
- TEMPO ENT., NFE, RAZAO SOCIAL, CIDADE, UF, PAÍS
- VALOR PEDIDO, VALOR FRETE, VALOR %, C, TDE, C E R D, OBSERVAÇÃO

## Próximo passo
Depois de ler, os dados passam pela **Validação (Passo 2)** para garantir que estão corretos.

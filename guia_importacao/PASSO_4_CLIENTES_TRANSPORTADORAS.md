# 👥 PASSO 4: Criação de Clientes e Transportadoras

## O que faz?
Cria os registros de **Clientes (Customer)** e **Transportadoras (Carrier)** no banco de dados.

## Como funciona?

### Estrutura de dados

```
CLIENTE (Customer)
  └─ Vinculado a: CIDADE
      └─ Que está em: ESTADO
          └─ Que está em: PAÍS

TRANSPORTADORA (Carrier)
  └─ Vinculado a: CIDADE
      └─ Que está em: ESTADO
          └─ Que está em: PAÍS
```

### Métodos principais:

#### `_get_or_create_customer()` - Busca ou cria um Cliente
```python
def _get_or_create_customer(self, customer_name, city):
    """Busca o cliente no banco, ou cria se não existir"""
```

**O que faz:**
- Recebe o nome do cliente (RAZAO SOCIAL) e a cidade
- Tenta encontrar o cliente **com esse nome nessa cidade**
- Se não existe, cria com:
  - `name`: Nome da empresa (ex: "ARMARINHOS FERNANDO LTDA")
  - `code`: Vazio (não vem no Excel)
  - `cnpj`: Vazio (não vem no Excel)
  - `city`: Vinculado à cidade correta

**Por que precisa da cidade?**
- Um cliente pode ter o mesmo nome em cidades diferentes
- A combinação (nome + cidade) é única

**Resultado:**
```
✨ Cliente criado: ARMARINHOS FERNANDO LTDA
ℹ️  Cliente encontrado: ARMARINHOS FERNANDO LTDA
```

#### `_get_or_create_carrier()` - Busca ou cria uma Transportadora
```python
def _get_or_create_carrier(self, carrier_name, city):
    """Busca a transportadora no banco, ou cria se não existir"""
```

**O que faz:**
- Recebe o nome da transportadora e a cidade
- Tenta encontrar a transportadora no banco
- Se não existe, cria com:
  - `name`: Nome da empresa (ex: "TAF", "ALFA")
  - `cnpj`: Vazio (não vem no Excel)
  - `city`: Vinculado à cidade correta

**Resultado:**
```
✨ Transportadora criada: TAF
✨ Transportadora criada: ALFA
ℹ️  Transportadora encontrada: TAF
```

#### `_create_customers_and_carriers()` - Orquestra tudo
```python
def _create_customers_and_carriers(self, df, hierarchy_data):
    """Cria todos os clientes e transportadoras"""
```

**Processo passo a passo:**

1. **Extrai dados do Excel** - Percorre cada linha
2. **Coleta clientes únicos** - Agrupa por RAZAO SOCIAL
3. **Coleta transportadoras únicas** - Agrupa por TRANSPORTADORA
4. **Associa à cidade** - Cada cliente/transportadora é vinculado à sua cidade
5. **Cria no banco** - Para cada um, busca/cria o registro

**Exemplo:**
```
Linha 1: ARMARINHOS FERNANDO LTDA + OSASCO
Linha 2: ARMARINHOS FERNANDO LTDA + SÃO PAULO
Linha 3: OUTRO CLIENTE + BELO HORIZONTE

Resultado:
- 2 clientes criados (são cidades diferentes!)
- 1 outro cliente
- Total: 3 clientes
```

## Resultado esperado

```
👥 PASSO 4: CRIANDO CLIENTES E TRANSPORTADORAS...
   👥 Clientes únicos encontrados: 15
   🚚 Transportadoras únicas encontradas: 8
   ✨ Cliente criado: ARMARINHOS FERNANDO LTDA
   ✨ Cliente criado: EMPRESA A
   ... mais clientes ...
   ✨ Transportadora criada: TAF
   ✨ Transportadora criada: ALFA
   ... mais transportadoras ...

✅ CLIENTES E TRANSPORTADORAS CRIADOS:
   ✅ 15 Clientes
   ✅ 8 Transportadoras
```

## Dados retornados

```python
{
    'customers': {
        'ARMARINHOS FERNANDO LTDA': <Customer: ARMARINHOS...>,
        'EMPRESA A': <Customer: EMPRESA A>,
        ...
    },
    'carriers': {
        'TAF': <Carrier: TAF>,
        'ALFA': <Carrier: ALFA>,
        ...
    }
}
```

## Por que isso é importante?

- **Organização** - Cada cliente e transportadora tem um registro único
- **Reutilização** - Se aparecer novamente no Excel, usa o mesmo registro
- **Vinculação** - Clientes e transportadoras estão ligados às cidades
- **Dados consistentes** - Evita duplicação

## Dados que NÃO vêm do Excel

- **CNPJ** - Precisa ser preenchido manualmente depois
- **Código do Cliente** - Não está no arquivo

Esses campos podem ser adicionados **manualmente no Django Admin** depois da importação.

## Próximo passo
Com clientes e transportadoras criados, agora vamos criar os **Pedidos (Passo 5)** que vincula tudo junto.

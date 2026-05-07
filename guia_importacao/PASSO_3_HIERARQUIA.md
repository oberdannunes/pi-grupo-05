# 📊 PASSO 3: Criação da Hierarquia (País → Estado → Cidade)

## O que faz?
Cria a estrutura hierárquica no banco de dados: BRASIL → Estados → Cidades.

## Como funciona?

### Estrutura de dados (Hierarquia)

```
PAÍS (BRASIL)
  └─ ESTADO (SP, MG, GO, etc)
      └─ CIDADE (São Paulo, Belo Horizonte, etc)
```

Essa hierarquia é **obrigatória** porque:
- Uma **Cidade** precisa estar vinculada a um **Estado**
- Um **Estado** precisa estar vinculado a um **País**

### Métodos principais:

#### `_get_or_create_country()` - Busca ou cria o País
```python
def _get_or_create_country(self, country_name='BRASIL'):
    """Busca BRASIL no banco, ou cria se não existir"""
    country, created = Country.objects.get_or_create(
        name=country_name,
        defaults={'name': country_name}
    )
```

**O que faz:**
- Tenta encontrar "BRASIL" no banco de dados
- Se não existe, cria um novo registro
- Retorna o objeto Country

**Resultado:**
```
✨ País criado: BRASIL    (primeira vez)
ℹ️  País encontrado: BRASIL (próximas vezes)
```

#### `_get_or_create_state()` - Busca ou cria um Estado
```python
def _get_or_create_state(self, uf, country):
    """Busca o estado (SP, MG) no banco, ou cria se não existir"""
```

**O que faz:**
- Converte UF para maiúsculas (sp → SP)
- Tenta encontrar o estado no banco
- Se não existe, cria com:
  - `id`: "SP" (identificador único)
  - `name`: "SP" (nome do estado)
  - `country`: Vinculado ao país BRASIL

**Resultado:**
```
✨ Estado criado: SP
✨ Estado criado: MG
✨ Estado criado: GO
ℹ️  Estado encontrado: SP (já existia)
```

#### `_get_or_create_city()` - Busca ou cria uma Cidade
```python
def _get_or_create_city(self, city_name, state):
    """Busca a cidade no banco, ou cria se não existir"""
```

**O que faz:**
- Converte nome da cidade para maiúsculas
- Tenta encontrar a cidade **vinculada ao estado**
- Se não existe, cria com:
  - `name`: "SÃO PAULO" (maiúsculas)
  - `state`: Vinculada ao estado correto

**Resultado:**
```
✨ Cidade criada: SÃO PAULO (SP)
✨ Cidade criada: OSASCO (SP)
✨ Cidade criada: BELO HORIZONTE (MG)
ℹ️  Cidade encontrada: SÃO PAULO (SP)
```

#### `_create_hierarchy()` - Orquestra tudo
```python
def _create_hierarchy(self, df):
    """Cria a hierarquia completa: País → Estados → Cidades"""
```

**Processo passo a passo:**

1. **Cria o País** - BRASIL
2. **Identifica Estados únicos** - Percorre o Excel e coleta todos os UF diferentes
3. **Cria os Estados** - Para cada UF único, cria um State vinculado a BRASIL
4. **Identifica Cidades únicas** - Coleta todas as cidades e qual estado cada uma pertence
5. **Cria as Cidades** - Para cada cidade, cria um City vinculado ao estado correto

## Resultado esperado

```
📊 PASSO 3: CRIANDO HIERARQUIA (PAÍS → ESTADO → CIDADE)...
   ✨ País criado: BRASIL
   📍 Estados únicos encontrados: 5
   📍 Cidades únicas encontradas: 23
   ✨ Estado criado: GO
   ✨ Estado criado: MG
   ✨ Estado criado: SP
   ... mais estados ...
   ✨ Cidade criada: BELO HORIZONTE (MG)
   ✨ Cidade criada: GOIÂNIA (GO)
   ... mais cidades ...

✅ HIERARQUIA CRIADA:
   ✅ 1 País (BRASIL)
   ✅ 5 Estados
   ✅ 23 Cidades
```

## Dados retornados

```python
{
    'country': <Country: BRASIL>,
    'states': {
        'SP': <State: SP>,
        'MG': <State: MG>,
        'GO': <State: GO>,
        ...
    },
    'cities': {
        'SÃO PAULO': <City: SÃO PAULO>,
        'BELO HORIZONTE': <City: BELO HORIZONTE>,
        ...
    }
}
```

## Por que isso é importante?

- **Integridade referencial** - Dados conectados corretamente
- **Busca e filtro** - Pode achar cidades por estado
- **Dados reutilizáveis** - Se duas linhas têm "SP", usa o mesmo State
- **Banco organizado** - Sem duplicação de dados

## Próximo passo
Com a hierarquia criada, agora vamos criar os **Clientes e Transportadoras (Passo 4)** vinculados às cidades.

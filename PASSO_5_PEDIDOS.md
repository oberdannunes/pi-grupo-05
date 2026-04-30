# 📦 PASSO 5: Criação de Pedidos (Order)

## O que faz?
Cria os registros de **Pedidos (Order)** no banco de dados, vinculando cliente, transportadora, datas e status.

## Como funciona?

### Estrutura final

```
PEDIDO (Order)
  ├─ NFE: "3945"
  ├─ order_date: 2024-01-03
  ├─ delivery_date: 2024-01-12
  ├─ status: "ENTREGUE"
  ├─ customer: ARMARINHOS FERNANDO LTDA
  └─ carrier: TAF
```

### Método principal:

#### `_create_orders()` - Cria todos os pedidos
```python
def _create_orders(self, df, customer_carrier_data):
    """Cria os Pedidos (Orders)"""
```

**Processo passo a passo:**

1. **Extrai dados de cada linha** do Excel:
   - `RAZAO SOCIAL` → Nome do cliente
   - `TRANSPORTADORA` → Nome da transportadora
   - `NFE` → Número do pedido (identidade única)
   - `DT. PEDIDO` → Data de quando o pedido foi feito
   - `DT. ENTREGA` → Data de entrega (pode estar vazia)

2. **Converte as datas** para formato DATE do Django:
   ```python
   order_date = pd.to_datetime(row.get('DT. PEDIDO')).date()
   delivery_date = pd.to_datetime(row.get('DT. ENTREGA')).date()
   ```

3. **Define o STATUS automaticamente**:
   ```
   Se tem data de entrega:
      status = "ENTREGUE"
   Senão:
      status = "PENDENTE"
   ```

4. **Busca o Cliente e Transportadora** criados no Passo 4:
   ```python
   customer = customers.get(cliente_nome)
   carrier = carriers.get(transportadora_nome)
   ```

5. **Cria ou atualiza o Pedido**:
   - Se NFE não existe → **Cria novo**
   - Se NFE já existe → **Atualiza dados**

   ```python
   order, created = Order.objects.get_or_create(
       nfe=nfe,
       defaults={
           'nfe': nfe,
           'order_date': order_date,
           'delivery_date': delivery_date,
           'status': status,
           'customer': customer,
           'carrier': carrier
       }
   )
   ```

## Resultado esperado

```
📦 PASSO 5: CRIANDO PEDIDOS...
   ✨ Pedido criado: NFE 3945
   ✨ Pedido criado: NFE 3946
   ✨ Pedido criado: NFE 44071
   ... mais pedidos ...

✅ PEDIDOS CRIADOS:
   ✅ 99 Pedidos inseridos/atualizados
   ❌ 0 Erros

✅ IMPORTAÇÃO CONCLUÍDA! 99 pedidos criados.
```

## Campos do Pedido

| Campo | Valor | Origem |
|-------|-------|--------|
| `nfe` | "3945" | Coluna NFE do Excel |
| `order_date` | 2024-01-03 | Coluna DT. PEDIDO |
| `delivery_date` | 2024-01-12 | Coluna DT. ENTREGA |
| `status` | "ENTREGUE" | Inferido (se delivery_date existe) |
| `customer` | ARMARINHOS... | Coluna RAZAO SOCIAL |
| `carrier` | TAF | Coluna TRANSPORTADORA |

## Status do Pedido

O status é **calculado automaticamente**:

```
┌─────────────────────────────────────────┐
│ DT. ENTREGA está preenchida?            │
└─────────────────────────────────────────┘
         ↓                    ↓
        SIM                  NÃO
         ↓                    ↓
   "ENTREGUE"          "PENDENTE"
```

### Exemplos:

| Linha | DT. PEDIDO | DT. ENTREGA | Status |
|-------|-----------|------------|--------|
| 2 | 2024-01-03 | 2024-01-12 | **ENTREGUE** |
| 3 | 2024-01-05 | 2024-01-18 | **ENTREGUE** |
| 99 | 2024-02-10 | (vazio) | **PENDENTE** |

## Tratamento de Erros

Se algo der errado ao criar um pedido:
```
❌ Erro ao criar pedido: Cliente ou Transportadora não encontrado
```

Mas o processo continua - não para na primeira falha!

## Dados que podem estar vazios

- **DT. ENTREGA** - Se o pedido ainda não foi entregue
- **CNPJ** - Não vem do Excel (deve ser preenchido manualmente)
- **Código do Cliente** - Não vem do Excel

## Por que isso é importante

1. **Visibilidade** - Você pode ver todos os pedidos no banco
2. **Status** - Sabe qual está entregue e qual está pendente
3. **Rastreamento** - Pode filtrar por cliente, transportadora, data
4. **Histórico** - Mantém registro de todas as transações

## Resultado final no banco de dados

```
PAÍS: 1 (BRASIL)
ESTADO: 5 (SP, MG, GO, ...)
CIDADE: 23 (São Paulo, Osasco, ...)
CLIENTE: 15 (Clientes únicos)
TRANSPORTADORA: 8 (Transportadoras únicas)
PEDIDO: 99 (Todos os pedidos)
```

## Próximo passo

✅ **Importação Completa!** 

Agora você pode:
1. **Acessar Django Admin** - Ver clientes, transportadoras, pedidos
2. **Testar a página de rastreamento** - Consultar pedido por NFE
3. **Filtrar dados** - Por cliente, transportadora, data, status
4. **Editar manualmente** - Adicionar CNPJ, código do cliente, etc

---

## 🎉 Parabéns!

Você completou toda a pipeline de importação de Excel! 

**Próximos passos recomendados:**
1. Testar a consulta de pedidos na página
2. Verificar dados no Django Admin
3. Corrigir dados manuais que faltarem (CNPJ, etc)
4. Importar mais arquivos Excel com outros dados

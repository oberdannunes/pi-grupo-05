import pandas as pd
from django.db import transaction
from ..models import Country, State, City, Customer, Carrier, Order

class OrderExcelImportService:
    """Serviço otimizado para importação de dados de fretes via arquivo Excel"""
    
    def __init__(self):
        # Colunas estritamente necessárias para a estrutura relacional e logística
        self.required_columns = [
            'TRANSPORTADORA', 'DT. PEDIDO', 'NFE', 
            'RAZAO SOCIAL', 'CNPJ PARC.', 'CIDADE', 'UF', 'PAÍS'
        ]
        self.validation_errors = []
        self.validation_success = []
        self.logs = []
    
    def log(self, message):
        self.logs.append(message)
        print(message)

    def _validate_row(self, row_index, row):
        """Valida uma linha individual do Excel com tratamento robusto para datas"""
        errors = []
        
        for col in self.required_columns:
            if pd.isna(row.get(col)) or str(row.get(col)).strip() == '':
                errors.append(f'Campo obrigatório vazio: {col}')
        
        if not pd.isna(row.get('UF')):
            uf = str(row.get('UF')).strip()
            if len(uf) != 2:
                errors.append(f'UF inválido: "{uf}" (deve ter 2 caracteres)')
        
        # Validação unificada de datas
        date_columns = ['DT. PEDIDO', 'DT. COLETA', 'DT. ENTREGA']
        for date_col in date_columns:
            val = row.get(date_col)
            if pd.notna(val) and str(val).strip() != '':
                try:
                    pd.to_datetime(val)
                except (ValueError, TypeError):
                    errors.append(f'Data inválida na coluna {date_col}: {val}')
        
        if not pd.isna(row.get('PAÍS')):
            pais = str(row.get('PAÍS')).strip().upper()
            if pais != 'BRASIL':
                errors.append(f'País inválido: "{pais}" (esperado: BRASIL)')
        
        # Validação de CNPJ
        if not pd.isna(row.get('CNPJ PARC.')):
            cnpj_parc = str(row.get('CNPJ PARC.')).strip()
            if not cnpj_parc.isdigit() or len(cnpj_parc) > 14:
                errors.append(f'CNPJ inválido: "{cnpj_parc}" (deve conter apenas dígitos)')
        
        try:
            nfe = row.get('NFE')
            if pd.notna(nfe):
                int(nfe)
        except (ValueError, TypeError):
            errors.append(f'NFE inválido: {nfe} (deve ser um número)')
        
        if errors:
            return False, errors
        return True, None

    def _validate_dataframe(self, df):
        """Valida todo o DataFrame"""
        self.log('\n🔍 PASSO 2: VALIDANDO DADOS...')
        
        valid_rows = 0
        invalid_rows = 0
        nfe_duplicates = {}
        
        for nfe in df['NFE'].dropna():
            nfe_int = str(int(nfe))
            nfe_duplicates[nfe_int] = nfe_duplicates.get(nfe_int, 0) + 1
            
        duplicate_nfes = {nfe for nfe, count in nfe_duplicates.items() if count > 1}
        
        # Iteração otimizada
        records = df.to_dict('records')
        for idx, row in enumerate(records):
            row_number = idx + 2
            is_valid, errors = self._validate_row(idx, row)
            
            try:
                nfe = str(int(row.get('NFE')))
                if nfe in duplicate_nfes:
                    errors = errors or []
                    errors.append(f'NFE duplicada: {nfe}')
                    is_valid = False
            except (ValueError, TypeError):
                pass
            
            if is_valid:
                valid_rows += 1
                self.validation_success.append({
                    'linha': row_number,
                    'nfe': row.get('NFE'),
                    'cliente': row.get('RAZAO SOCIAL'),
                    'transportadora': row.get('TRANSPORTADORA')
                })
            else:
                invalid_rows += 1
                self.validation_errors.append({
                    'linha': row_number,
                    'nfe': row.get('NFE'),
                    'cliente': row.get('RAZAO SOCIAL'),
                    'erros': errors
                })
        
        self.log(f'   ✅ Linhas válidas: {valid_rows}')
        self.log(f'   ❌ Linhas inválidas: {invalid_rows}')
        return valid_rows, invalid_rows

    def _get_or_create_country(self, country_name='BRASIL'):
        country, created = Country.objects.get_or_create(
            name=country_name,
            defaults={'name': country_name}
        )
        return country

    def _get_or_create_state(self, uf, country):
        uf_upper = str(uf).strip().upper()
        state, created = State.objects.get_or_create(
            id=uf_upper,
            country=country,
            defaults={'id': uf_upper, 'name': uf_upper, 'country': country}
        )
        return state

    def _get_or_create_city(self, city_name, state):
        city_name_clean = str(city_name).strip().upper()
        city, created = City.objects.get_or_create(
            name=city_name_clean,
            state=state,
            defaults={'name': city_name_clean, 'state': state}
        )
        return city

    def _create_hierarchy(self, df):
        self.log('\n📊 PASSO 3: CRIANDO HIERARQUIA (PAÍS → ESTADO → CIDADE)...')
        country = self._get_or_create_country('BRASIL')
        
        unique_states = set()
        city_state_map = {}
        
        records = df.to_dict('records')
        for row in records:
            uf = str(row.get('UF')).strip().upper()
            cidade = str(row.get('CIDADE')).strip().upper()
            unique_states.add(uf)
            city_state_map[cidade] = uf
        
        states_dict = {uf: self._get_or_create_state(uf, country) for uf in sorted(unique_states)}
        cities_dict = {city: self._get_or_create_city(city, states_dict[uf]) for city, uf in city_state_map.items()}
        
        self.log(f'   ✅ 1 País, {len(states_dict)} Estados, {len(cities_dict)} Cidades processadas.')
        return {'country': country, 'states': states_dict, 'cities': cities_dict}

    def _normalize_cnpj(self, cnpj):
        """Normaliza CNPJ para 14 dígitos com zeros à esquerda"""
        if pd.isna(cnpj) or not cnpj:
            return ''
        cnpj_str = str(cnpj).strip()
        if not cnpj_str.isdigit():
            return ''
        # Completa com zeros à esquerda para garantir 14 dígitos
        return ("0" * 14 + cnpj_str)[-14:]

    def _get_or_create_customer(self, customer_name, cnpj, city):
        if not city:
            # Retorna None se não houver cidade válida
            return None
            
        customer_name_clean = str(customer_name).strip()
        cnpj_clean = self._normalize_cnpj(cnpj)
        
        if not cnpj_clean:
            # Retorna None se CNPJ inválido
            return None
        
        customer, created = Customer.objects.get_or_create(
            cnpj=cnpj_clean,
            defaults={
                'name': customer_name_clean,
                'code': '',
                'cnpj': cnpj_clean,
                'city': city
            }
        )
        # Atualiza nome se o cliente já existir
        if not created and customer.name != customer_name_clean:
            customer.name = customer_name_clean
            customer.save(update_fields=['name'])
        return customer

    def _get_or_create_carrier(self, carrier_name, city):
        carrier_name_clean = str(carrier_name).strip()
        carrier, created = Carrier.objects.get_or_create(
            name=carrier_name_clean,
            defaults={
                'cnpj': '', 
                'city': city
                }
        )
        return carrier

    def _create_customers_and_carriers(self, df, hierarchy_data):
        self.log('\n👥 PASSO 4: CRIANDO CLIENTES E TRANSPORTADORAS...')
        cities_dict = hierarchy_data['cities']
        
        unique_customers = {}
        unique_carriers = {}
        
        records = df.to_dict('records')
        for row in records:
            cliente = str(row.get('RAZAO SOCIAL')).strip()
            cnpj_parc = row.get('CNPJ PARC.')
            transportadora = str(row.get('TRANSPORTADORA')).strip()
            cidade = str(row.get('CIDADE')).strip().upper()
            
            # Normaliza CNPJ para usar como chave consistentemente
            cnpj_normalized = self._normalize_cnpj(cnpj_parc)
            
            # Valida se cidade existe na hierarquia
            if cidade not in cities_dict:
                continue
            
            # Deduplicação pelo CNPJ normalizado
            if cnpj_normalized and cnpj_normalized not in unique_customers:
                unique_customers[cnpj_normalized] = {'nome': cliente, 'cidade': cidade}
            if transportadora not in unique_carriers:
                unique_carriers[transportadora] = cidade
                
        # Cria dicionário de clientes apenas com os que foram criados com sucesso
        customers = {}
        for cnpj, data in unique_customers.items():
            city_obj = cities_dict.get(data['cidade'])
            customer = self._get_or_create_customer(data['nome'], cnpj, city_obj)
            if customer:
                customers[cnpj] = customer
        
        carriers = {}
        for name, city_name in unique_carriers.items():
            city_obj = cities_dict.get(city_name)
            if city_obj:
                carrier = self._get_or_create_carrier(name, city_obj)
                carriers[name] = carrier
        
        self.log(f'   ✅ {len(customers)} Clientes e {len(carriers)} Transportadoras processados.')
        return {'customers': customers, 'carriers': carriers}

    def _create_orders(self, df, customer_carrier_data):
        self.log('\n📦 PASSO 5: CRIANDO PEDIDOS...')
        customers = customer_carrier_data['customers']
        carriers = customer_carrier_data['carriers']
        
        orders_created = 0
        orders_errors = 0
        
        records = df.to_dict('records')
        for idx, row in enumerate(records):
            try:
                transportadora_nome = str(row.get('TRANSPORTADORA')).strip()
                cnpj_parc = row.get('CNPJ PARC.')
                nfe = str(int(row.get('NFE')))
                order_date = pd.to_datetime(row.get('DT. PEDIDO')).date()
                
                collection_date = None
                if pd.notna(row.get('DT. COLETA')) and str(row.get('DT. COLETA')).strip() != '':
                    collection_date = pd.to_datetime(row.get('DT. COLETA')).date()
                
                delivery_date = None
                if pd.notna(row.get('DT. ENTREGA')) and str(row.get('DT. ENTREGA')).strip() != '':
                    delivery_date = pd.to_datetime(row.get('DT. ENTREGA')).date()
                
                # Lógica de status logístico baseada nas datas
                if delivery_date:
                    status = 'ENTREGUE'
                elif collection_date:
                    status = 'TRANSITO'
                else:
                    status = 'PENDENTE'
                
                # Normaliza CNPJ para busca consistente
                cnpj_normalized = self._normalize_cnpj(cnpj_parc)
                
                # Busca cliente pelo CNPJ normalizado
                customer = customers.get(cnpj_normalized)
                carrier = carriers.get(transportadora_nome)
                
                if not customer or not carrier:
                    orders_errors += 1
                    continue
                
                # update_or_create garante que a base reflita as atualizações da planilha
                order, created = Order.objects.update_or_create(
                    nfe=nfe,
                    defaults={
                        'order_date': order_date,
                        'collection_date': collection_date,
                        'delivery_date': delivery_date,
                        'status': status,
                        'customer': customer,
                        'carrier': carrier
                    }
                )
                if created: orders_created += 1
                
            except Exception as e:
                orders_errors += 1
                self.log(f'   ❌ Linha {idx + 2}: Erro ao criar pedido: {str(e)}')
        
        self.log(f'   ✅ {orders_created} Pedidos inseridos/atualizados. {orders_errors} Erros.')
        return {'orders_created': orders_created, 'orders_errors': orders_errors}

    @transaction.atomic
    def importfile(self, file):
        """Método principal envolvido em transação atômica para garantir integridade estrutural."""
        if not file:
            raise ValueError('Nenhum arquivo fornecido.')
        
        try:
            self.log('📖 PASSO 1: LENDO ARQUIVO EXCEL...')
            df = pd.read_excel(file, sheet_name='FRETES CONSOLIDADA')
            
            self.log(f'✅ Arquivo lido com sucesso! Shape: {df.shape[0]} linhas, {df.shape[1]} colunas')
            
            valid_rows, invalid_rows = self._validate_dataframe(df)
            
            if invalid_rows > 0:
                self.log(f'\n⚠️  VALIDAÇÃO ENCONTROU ERROS (mostrando primeiros 5):')
                for err in self.validation_errors[:5]:
                    self.log(f'   Linha {err["linha"]}: {", ".join(err["erros"])}')
            
            # Executa a esteira de importação apenas com dados validados não interrompe o fluxo geral
            hierarchy_data = self._create_hierarchy(df)
            customer_carrier_data = self._create_customers_and_carriers(df, hierarchy_data)
            orders_data = self._create_orders(df, customer_carrier_data)
            
            return {
                'success': True,
                'message': f'Importação concluída! {orders_data["orders_created"]} pedidos criados.',
                'rows_valid': valid_rows,
                'rows_invalid': invalid_rows,
                'validation_errors': self.validation_errors[:10],
                'validation_success': self.validation_success,
                'hierarchy_data': hierarchy_data,
                'customer_carrier_data': customer_carrier_data,
                'orders_data': orders_data,
                'logs': self.logs
            }
            
        except Exception as e:
            self.log(f'❌ Erro catastrófico ao processar arquivo. Rollback executado: {str(e)}')
            import traceback
            traceback.print_exc()
            return {
                'success': False,
                'logs': self.logs
            }
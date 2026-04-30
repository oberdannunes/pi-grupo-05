import pandas as pd
from django.db import transaction
from ..models import Country, State, City, Customer, Carrier, Order


class OrderExcelImportService:
    """Serviço para importação de dados de fretes via arquivo Excel"""
    
    def __init__(self):
        self.required_columns = ['TRANSPORTADORA', 'DT. PEDIDO', 'NFE', 'RAZAO SOCIAL', 'CIDADE', 'UF', 'PAÍS']
        self.validation_errors = []
        self.validation_success = []

    def _validate_row(self, row_index, row):
        """Valida uma linha individual do Excel"""
        errors = []
        
        for col in self.required_columns:
            if pd.isna(row.get(col)) or str(row.get(col)).strip() == '':
                errors.append(f'Campo obrigatório vazio: {col}')
        
        if not pd.isna(row.get('UF')):
            uf = str(row.get('UF')).strip()
            if len(uf) != 2:
                errors.append(f'UF inválido: "{uf}" (deve ter 2 caracteres)')
        
        if not pd.isna(row.get('DT. PEDIDO')):
            try:
                pd.to_datetime(row.get('DT. PEDIDO'))
            except:
                errors.append(f'Data de pedido inválida: {row.get("DT. PEDIDO")}')
        
        if not pd.isna(row.get('PAÍS')):
            pais = str(row.get('PAÍS')).strip().upper()
            if pais != 'BRASIL':
                errors.append(f'País inválido: "{pais}" (esperado: BRASIL)')
        
        try:
            nfe = row.get('NFE')
            int(nfe)
        except (ValueError, TypeError):
            errors.append(f'NFE inválido: {nfe} (deve ser um número)')
        
        if errors:
            return False, errors
        return True, None

    def _validate_dataframe(self, df):
        """Valida todo o DataFrame"""
        print('\n🔍 PASSO 2: VALIDANDO DADOS...')
        
        valid_rows = 0
        invalid_rows = 0
        nfe_duplicates = {}
        duplicate_nfes = set()
        
        for nfe in df['NFE'].dropna():
            nfe_int = str(int(nfe))
            if nfe_int in nfe_duplicates:
                nfe_duplicates[nfe_int] += 1
            else:
                nfe_duplicates[nfe_int] = 1
        
        duplicate_nfes = {nfe for nfe, count in nfe_duplicates.items() if count > 1}
        
        for idx, row in df.iterrows():
            row_number = idx + 2
            is_valid, errors = self._validate_row(idx, row)
            
            try:
                nfe = str(int(row.get('NFE')))
                if nfe in duplicate_nfes:
                    if errors is None:
                        errors = []
                    errors.append(f'NFE duplicada: {nfe}')
                    is_valid = False
            except:
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
        
        print(f'   ✅ Linhas válidas: {valid_rows}')
        print(f'   ❌ Linhas inválidas: {invalid_rows}')
        
        return valid_rows, invalid_rows

    def _get_or_create_country(self, country_name='BRASIL'):
        """Busca ou cria um País"""
        country, created = Country.objects.get_or_create(
            name=country_name,
            defaults={'name': country_name}
        )
        if created:
            print(f'   ✨ País criado: {country_name}')
        else:
            print(f'   ℹ️  País encontrado: {country_name}')
        return country

    def _get_or_create_state(self, uf, country):
        """Busca ou cria um Estado"""
        uf_upper = str(uf).strip().upper()
        state, created = State.objects.get_or_create(
            id=uf_upper,
            country=country,
            defaults={
                'id': uf_upper,
                'name': uf_upper,
                'country': country
            }
        )
        if created:
            print(f'   ✨ Estado criado: {uf_upper}')
        else:
            print(f'   ℹ️  Estado encontrado: {uf_upper}')
        return state

    def _get_or_create_city(self, city_name, state):
        """Busca ou cria uma Cidade"""
        city_name_clean = str(city_name).strip().upper()
        city, created = City.objects.get_or_create(
            name=city_name_clean,
            state=state,
            defaults={
                'name': city_name_clean,
                'state': state
            }
        )
        if created:
            print(f'   ✨ Cidade criada: {city_name_clean} ({state.id})')
        else:
            print(f'   ℹ️  Cidade encontrada: {city_name_clean} ({state.id})')
        return city

    def _create_hierarchy(self, df):
        """PASSO 3: Cria a hierarquia Country → State → City"""
        print('\n📊 PASSO 3: CRIANDO HIERARQUIA (PAÍS → ESTADO → CIDADE)...')
        
        country = self._get_or_create_country('BRASIL')
        
        unique_states = set()
        city_state_map = {}
        
        for idx, row in df.iterrows():
            uf = str(row.get('UF')).strip().upper()
            cidade = str(row.get('CIDADE')).strip().upper()
            
            unique_states.add(uf)
            city_state_map[cidade] = uf
        
        print(f'   📍 Estados únicos encontrados: {len(unique_states)}')
        print(f'   📍 Cidades únicas encontradas: {len(city_state_map)}')
        
        states_dict = {}
        for uf in sorted(unique_states):
            state = self._get_or_create_state(uf, country)
            states_dict[uf] = state
        
        cities_dict = {}
        for city_name, uf in city_state_map.items():
            state = states_dict.get(uf)
            if state:
                city = self._get_or_create_city(city_name, state)
                cities_dict[city_name] = city
        
        print(f'\n✅ HIERARQUIA CRIADA:')
        print(f'   ✅ 1 País (BRASIL)')
        print(f'   ✅ {len(states_dict)} Estados')
        print(f'   ✅ {len(cities_dict)} Cidades')
        
        return {
            'country': country,
            'states': states_dict,
            'cities': cities_dict
        }

    def _get_or_create_customer(self, customer_name, city):
        """Busca ou cria um Cliente"""
        customer_name_clean = str(customer_name).strip()
        customer, created = Customer.objects.get_or_create(
            name=customer_name_clean,
            city=city,
            defaults={
                'name': customer_name_clean,
                'code': '',
                'cnpj': '',
                'city': city
            }
        )
        if created:
            print(f'   ✨ Cliente criado: {customer_name_clean}')
        else:
            print(f'   ℹ️  Cliente encontrado: {customer_name_clean}')
        return customer

    def _get_or_create_carrier(self, carrier_name, city):
        """Busca ou cria uma Transportadora"""
        carrier_name_clean = str(carrier_name).strip()
        carrier, created = Carrier.objects.get_or_create(
            name=carrier_name_clean,
            city=city,
            defaults={
                'name': carrier_name_clean,
                'cnpj': '',
                'city': city
            }
        )
        if created:
            print(f'   ✨ Transportadora criada: {carrier_name_clean}')
        else:
            print(f'   ℹ️  Transportadora encontrada: {carrier_name_clean}')
        return carrier

    def _create_customers_and_carriers(self, df, hierarchy_data):
        """PASSO 4: Cria Clientes e Transportadoras"""
        print('\n👥 PASSO 4: CRIANDO CLIENTES E TRANSPORTADORAS...')
        
        cities_dict = hierarchy_data['cities']
        
        customers = {}
        carriers = {}
        customers_count = 0
        carriers_count = 0
        
        # Extrair clientes e transportadoras únicas
        unique_customers = {}
        unique_carriers = {}
        
        for idx, row in df.iterrows():
            cliente = str(row.get('RAZAO SOCIAL')).strip()
            transportadora = str(row.get('TRANSPORTADORA')).strip()
            cidade = str(row.get('CIDADE')).strip().upper()
            
            if cliente not in unique_customers:
                unique_customers[cliente] = cidade
            if transportadora not in unique_carriers:
                unique_carriers[transportadora] = cidade
        
        print(f'   👥 Clientes únicos encontrados: {len(unique_customers)}')
        print(f'   🚚 Transportadoras únicas encontradas: {len(unique_carriers)}')
        
        # Criar clientes
        for customer_name, city_name in unique_customers.items():
            city_name_upper = city_name.upper()
            city = cities_dict.get(city_name_upper)
            if city:
                customer = self._get_or_create_customer(customer_name, city)
                customers[customer_name] = customer
                customers_count += 1
        
        # Criar transportadoras
        for carrier_name, city_name in unique_carriers.items():
            city_name_upper = city_name.upper()
            city = cities_dict.get(city_name_upper)
            if city:
                carrier = self._get_or_create_carrier(carrier_name, city)
                carriers[carrier_name] = carrier
                carriers_count += 1
        
        print(f'\n✅ CLIENTES E TRANSPORTADORAS CRIADOS:')
        print(f'   ✅ {customers_count} Clientes')
        print(f'   ✅ {carriers_count} Transportadoras')
        
        return {
            'customers': customers,
            'carriers': carriers
        }

    def _create_orders(self, df, customer_carrier_data):
        """PASSO 5: Cria os Pedidos (Orders)"""
        print('\n📦 PASSO 5: CRIANDO PEDIDOS...')
        
        customers = customer_carrier_data['customers']
        carriers = customer_carrier_data['carriers']
        
        orders_created = 0
        orders_errors = 0
        
        for idx, row in df.iterrows():
            try:
                cliente_nome = str(row.get('RAZAO SOCIAL')).strip()
                transportadora_nome = str(row.get('TRANSPORTADORA')).strip()
                nfe = str(int(row.get('NFE')))
                order_date = pd.to_datetime(row.get('DT. PEDIDO')).date()
                delivery_date = None
                
                # Tentar converter data de entrega
                if not pd.isna(row.get('DT. ENTREGA')):
                    try:
                        delivery_date = pd.to_datetime(row.get('DT. ENTREGA')).date()
                    except:
                        pass
                
                # Definir status baseado na data de entrega
                status = 'ENTREGUE' if delivery_date else 'PENDENTE'
                
                # Buscar cliente e transportadora
                customer = customers.get(cliente_nome)
                carrier = carriers.get(transportadora_nome)
                
                if not customer or not carrier:
                    orders_errors += 1
                    print(f'   ⚠️  Linha {idx + 2}: Cliente ou Transportadora não encontrado')
                    continue
                
                # Criar ou atualizar pedido
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
                
                if created:
                    orders_created += 1
                else:
                    # Atualizar pedido existente
                    order.order_date = order_date
                    order.delivery_date = delivery_date
                    order.status = status
                    order.customer = customer
                    order.carrier = carrier
                    order.save()
                
            except Exception as e:
                orders_errors += 1
                print(f'   ❌ Linha {idx + 2}: Erro ao criar pedido: {str(e)}')
        
        print(f'\n✅ PEDIDOS CRIADOS:')
        print(f'   ✅ {orders_created} Pedidos inseridos/atualizados')
        print(f'   ❌ {orders_errors} Erros')
        
        return {
            'orders_created': orders_created,
            'orders_errors': orders_errors
        }

    def importfile(self, file):
        if not file:
            raise ValueError('Nenhum arquivo fornecido.')
        
        try:
            print('📖 PASSO 1: LENDO ARQUIVO EXCEL...')
            
            df = pd.read_excel(file, sheet_name='FRETES CONSOLIDADA')
            
            print(f'✅ Arquivo lido com sucesso!')
            print(f'   📊 Shape: {df.shape[0]} linhas, {df.shape[1]} colunas')
            
            valid_rows, invalid_rows = self._validate_dataframe(df)
            
            if invalid_rows > 0:
                print(f'\n⚠️  VALIDAÇÃO ENCONTROU ERROS:')
                for err in self.validation_errors[:5]:
                    print(f'   Linha {err["linha"]}: {", ".join(err["erros"])}')
                if len(self.validation_errors) > 5:
                    print(f'   ... e mais {len(self.validation_errors) - 5} erros')
            
            print(f'\n✅ VALIDAÇÃO CONCLUÍDA: {valid_rows} linhas válidas')
            
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
                'orders_data': orders_data
            }
            
        except Exception as e:
            print(f'❌ Erro ao processar arquivo: {str(e)}')
            import traceback
            traceback.print_exc()
            return {
                'success': False,
                'message': f'Erro ao processar arquivo: {str(e)}'
            }

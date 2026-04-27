-- =====================================================
-- SCRIPT COMPLETO DE INSERÇÃO - PLANEAMENTO DE ESTIVA
-- SCHEMA ATUALIZADO COM channel_depth NA TABELA port
-- =====================================================

-- -----------------------------------------------------
-- COMPANY
-- -----------------------------------------------------
INSERT INTO company (id, name) VALUES
(1, 'Mediterranean Shipping Company (MSC)'),
(2, 'Transatlântica - Transportes Marítimos Portugueses'),
(3, 'Portline - Transportes Marítimos Internacionais'),
(4, 'CMA CGM Portugal'),
(5, 'Maersk Line Portugal'),
(6, 'ColdChain Logistics Portugal'),
(7, 'Atlantic RoRo Solutions');

-- -----------------------------------------------------
-- SHIP_TYPE
-- -----------------------------------------------------
INSERT INTO ship_type (id, name) VALUES
(1, 'Porta-contentores'),
(2, 'Químico / produtos líquidos a granel'),
(3, 'Ro-Ro (Roll-on/Roll-off)'),
(4, 'Graneleiro'),
(5, 'Porta-automóveis (PCTC)'),
(6, 'Navio frigorífico'),
(7, 'Contentor/RO-RO combinado (ConRo)');

-- -----------------------------------------------------
-- FUEL_EFFICIENCY
-- -----------------------------------------------------
INSERT INTO fuel_efficiency (id, name, fuel_consumption_t_per_day) VALUES
(1, 'Consumo médio — linha contentores', 42.50),
(2, 'Consumo médio — tanqueiro', 38.00),
(3, 'Alta eficiência — eco design', 28.50),
(4, 'Consumo elevado — navio mais antigo', 65.00),
(5, 'Média eficiência — feeder', 18.20),
(6, 'Baixo consumo — navio pequeno', 12.00),
(7, 'Alto consumo — grande graneleiro', 55.00);

-- -----------------------------------------------------
-- WEATHER_CONDITION
-- -----------------------------------------------------
INSERT INTO weather_condition (id, name) VALUES
(1, 'Bom'),
(2, 'Moderado'),
(3, 'Mau');

-- -----------------------------------------------------
-- TANK_TYPE
-- -----------------------------------------------------
INSERT INTO tank_type (id, code, name) VALUES
(1, 'BALLAST', 'Lastro'),
(2, 'FUEL', 'Combustível'),
(3, 'FW', 'Água doce'),
(4, 'LIQUID_CARGO', 'Carga líquida'),
(5, 'LUBE_OIL', 'Óleo lubrificante'),
(6, 'SLUDGE', 'Lamas'),
(7, 'CHEMICAL', 'Produto químico'),
(8, 'BUNKER', 'Bunker C');

-- -----------------------------------------------------
-- ROUTE
-- -----------------------------------------------------
INSERT INTO route (id, name, distance_nm, frequency_days) VALUES
(1, 'Rotterdam — Leixões', 950.00, 15),
(2, 'Sines — Rotterdam', 1100.00, 7),
(3, 'Rotterdam — Sines', 2650.00, 21),
(4, 'Leixões — Lisboa — Algeciras', 580.00, 10),
(5, 'Sines — Luanda', 3850.00, 30),
(6, 'Leixões — Southampton — Hamburgo', 1250.00, 14),
(7, 'Lisboa — Funchal — Santa Cruz (Tenerife)', 680.00, 7),
(8, 'Sines — Houston (EUA)', 4200.00, 35),
(9, 'Rotterdam — Sines — Durban', 6540.00, 45),
(10, 'Leixões — Santos (Brasil)', 4650.00, 28),
(11, 'Rotterdam — Gdansk — São Petersburgo', 1120.00, 12),
(12, 'Valência — Barcelona — Génova', 450.00, 5);

-- -----------------------------------------------------
-- PORT (com channel_depth adicionado)
-- -----------------------------------------------------
INSERT INTO port (id, name, country, latitude, longitude, max_draft, channel_depth, max_ship_length, tidal_restrictions, description) VALUES
(1, 'Rotterdam', 'Países Baixos', 51.9225000, 4.4791700, 20.00, 24.00, 400.00, 1, 'Maior porto da Europa, hub de contentores'),
(2, 'Leixões', 'Portugal', 41.1833333, -8.7000000, 16.00, 18.00, 350.00, 0, 'Principal porto do norte de Portugal'),
(3, 'Sines', 'Portugal', 37.9500000, -8.8666667, 21.00, 25.00, 400.00, 0, 'Terminal de águas profundas e líquidos'),
(4, 'Hamburgo', 'Alemanha', 53.5419444, 9.9961111, 16.50, 18.50, 400.00, 0, 'Hub Norte da Europa'),
(5, 'Antuérpia', 'Bélgica', 51.2300000, 4.4000000, 17.50, 18.50, 430.00, 0, 'Maior porto de contentores da Europa'),
(6, 'Lisboa', 'Portugal', 38.7166700, -9.1333300, 15.50, 17.00, 350.00, 1, 'Porto da capital portuguesa'),
(7, 'Algeciras', 'Espanha', 36.1288889, -5.4436111, 22.00, 24.00, 420.00, 0, 'Porto estratégico no estreito de Gibraltar'),
(8, 'Valência', 'Espanha', 39.4597222, -0.3169444, 18.00, 20.00, 400.00, 0, 'Principal porto contentores de Espanha'),
(9, 'Barcelona', 'Espanha', 41.3472222, 2.1566667, 17.50, 19.00, 400.00, 0, 'Porto da capital da Catalunha'),
(10, 'Génova', 'Itália', 44.4122222, 8.9288889, 15.00, 16.50, 350.00, 1, 'Principal porto italiano'),
(11, 'Southampton', 'Reino Unido', 50.8952778, -1.4022222, 17.00, 18.00, 400.00, 1, 'Porto no sul de Inglaterra'),
(12, 'Luanda', 'Angola', -8.7688889, 13.2786111, 16.00, 17.50, 350.00, 0, 'Principal porto angolano'),
(13, 'Houston', 'EUA', 29.7600000, -95.3700000, 15.00, 16.00, 305.00, 0, 'Porto do Texas, especializado em petróleo'),
(14, 'Santos', 'Brasil', -23.9600000, -46.3300000, 15.00, 16.50, 350.00, 1, 'Maior porto da América Latina'),
(15, 'Durban', 'África do Sul', -29.8800000, 31.0300000, 19.00, 21.00, 370.00, 1, 'Principal porto sul-africano'),
(16, 'Funchal', 'Portugal', 32.6500000, -16.9166700, 11.00, 12.00, 280.00, 0, 'Porto da Madeira'),
(17, 'Santa Cruz', 'Espanha', 28.4688889, -16.2544444, 15.00, 16.00, 350.00, 0, 'Porto de Tenerife, Canárias'),
(18, 'Gdansk', 'Polónia', 54.3947222, 18.6561111, 15.50, 17.00, 380.00, 0, 'Principal porto polaco'),
(19, 'São Petersburgo', 'Rússia', 59.9311111, 30.3075000, 13.00, 14.00, 320.00, 1, 'Porto russo no Báltico'),
(20, 'Setúbal', 'Portugal', 38.5175000, -8.8938889, 14.00, 15.00, 300.00, 1, 'Porto industrial a sul de Lisboa'),
(21, 'Aveiro', 'Portugal', 40.6458333, -8.7486111, 9.50, 10.50, 250.00, 1, 'Porto da região centro'),
(22, 'Portimão', 'Portugal', 37.1186111, -8.5255556, 10.00, 11.00, 200.00, 1, 'Porto do Algarve');

-- -----------------------------------------------------
-- ROUTE_PORT
-- -----------------------------------------------------
INSERT INTO route_port (id, id_route, id_port, port_order) VALUES
-- Rota 1: Rotterdam - Leixões
(1, 1, 1, 1), (2, 1, 2, 2),
-- Rota 2: Sines - Rotterdam
(3, 2, 3, 1), (4, 2, 1, 2),
-- Rota 3: Rotterdam - Sines (longa)
(5, 3, 1, 1), (6, 3, 4, 2), (7, 3, 5, 3), (8, 3, 2, 4), (9, 3, 3, 5),
-- Rota 4: Leixões - Lisboa - Algeciras
(10, 4, 2, 1), (11, 4, 6, 2), (12, 4, 7, 3),
-- Rota 5: Sines - Luanda
(13, 5, 3, 1), (14, 5, 12, 2),
-- Rota 6: Leixões - Southampton - Hamburgo
(15, 6, 2, 1), (16, 6, 11, 2), (17, 6, 4, 3),
-- Rota 7: Lisboa - Funchal - Santa Cruz
(18, 7, 6, 1), (19, 7, 16, 2), (20, 7, 17, 3),
-- Rota 8: Sines - Houston
(21, 8, 3, 1), (22, 8, 13, 2),
-- Rota 9: Rotterdam - Sines - Durban
(23, 9, 1, 1), (24, 9, 3, 2), (25, 9, 15, 3),
-- Rota 10: Leixões - Santos
(26, 10, 2, 1), (27, 10, 14, 2),
-- Rota 11: Rotterdam - Gdansk - São Petersburgo
(28, 11, 1, 1), (29, 11, 18, 2), (30, 11, 19, 3),
-- Rota 12: Valência - Barcelona - Génova
(31, 12, 8, 1), (32, 12, 9, 2), (33, 12, 10, 3);

-- -----------------------------------------------------
-- PORT_FEES
-- -----------------------------------------------------
INSERT INTO port_fees (id, id_port, name, price) VALUES
(1, 1, 'Taxa atracação', 12500.00),
(2, 2, 'Taxa atracação', 9800.00),
(3, 3, 'Taxa terminal líquidos', 15200.00),
(4, 4, 'Taxa atracação', 14200.00),
(5, 5, 'Taxa atracação', 16800.00),
(6, 6, 'Taxa atracação', 8700.00),
(7, 7, 'Taxa atracação', 13500.00),
(8, 8, 'Taxa atracação', 11800.00),
(9, 9, 'Taxa atracação', 12500.00),
(10, 10, 'Taxa atracação', 11200.00),
(11, 11, 'Taxa atracação', 14500.00),
(12, 12, 'Taxa atracação', 15600.00),
(13, 13, 'Taxa atracação', 18900.00),
(14, 14, 'Taxa atracação', 13200.00),
(15, 15, 'Taxa atracação', 14300.00),
(16, 16, 'Taxa atracação', 5200.00),
(17, 17, 'Taxa atracação', 7800.00),
(18, 18, 'Taxa atracação', 10500.00),
(19, 19, 'Taxa atracação', 9600.00),
(20, 3, 'Taxa de amarração', 2500.00),
(21, 3, 'Taxa de pilotagem', 1800.00),
(22, 2, 'Taxa de resíduos', 750.00);

-- -----------------------------------------------------
-- CARGO_TYPE
-- -----------------------------------------------------
INSERT INTO cargo_type (id, name, need_container, description) VALUES
(1, 'DRY CONTAINER', 1, 'Seca em contentor'),
(2, 'REEFER', 1, 'Reefer (temperatura controlada)'),
(3, 'DANGEROUS CONTAINER', 1, 'ADR / IMDG em contentor'),
(4, 'LIQUID BULK', 0, 'Líquido a granel (tanques)'),
(5, 'DRY BULK', 0, 'Granel sólido'),
(6, 'RO RO CARGO', 0, 'Carga Roll-on/Roll-off'),
(7, 'PROJECT CARGO', 0, 'Carga de projecto (oversize)'),
(8, 'GAS BULK', 0, 'Gás liquefeito (LNG/LPG)');

-- -----------------------------------------------------
-- CARGO
-- -----------------------------------------------------
INSERT INTO cargo (id, id_cargo_type, cargo_name, weight, volume, priority, imdg_class, temperature_required, quantity, unit) VALUES
-- Contentores secos
(1, 1, 'Peças automóveis — lote A', 22.50, 68.00, 1, 'N/A', NULL, 22.5000, 't'),
(2, 1, 'Têxteis embalados', 18.20, 55.00, 2, 'N/A', NULL, 18.2000, 't'),
(3, 1, 'Mobiliário flat-pack', 16.00, 62.00, 3, 'N/A', NULL, 800.0000, 'm3'),
(16, 1, 'Eletrónicos e componentes', 15.50, 70.00, 1, 'N/A', NULL, 15.5000, 't'),
(17, 1, 'Calçado português', 12.80, 58.00, 2, 'N/A', NULL, 12.8000, 't'),
(18, 1, 'Cortiça embalada', 8.50, 85.00, 2, 'N/A', NULL, 8.5000, 't'),
(19, 1, 'Vidro e cristal', 24.00, 52.00, 1, 'N/A', NULL, 24.0000, 't'),
(20, 1, 'Máquinas industriais', 28.00, 45.00, 1, 'N/A', NULL, 28.0000, 't'),
(21, 1, 'Papel e celulose', 20.50, 72.00, 3, 'N/A', NULL, 20.5000, 't'),
(22, 1, 'Borracha', 19.80, 60.00, 2, 'N/A', NULL, 19.8000, 't'),
(23, 1, 'Cerâmica e azulejos', 26.50, 48.00, 1, 'N/A', NULL, 26.5000, 't'),
(24, 1, 'Plásticos granulados', 14.20, 75.00, 3, 'N/A', NULL, 14.2000, 't'),

-- Reefer
(4, 2, 'Carnes congeladas', 20.10, 65.00, 1, 'N/A', -25.00, 20.1000, 't'),
(5, 2, 'Fruta refrigerada', 19.40, 64.00, 2, 'N/A', 2.00, 19.4000, 't'),
(6, 2, 'Lacticínios +4 °C', 17.80, 60.00, 2, 'N/A', 4.00, 17.8000, 't'),
(25, 2, 'Peixe congelado', 21.50, 66.00, 1, 'N/A', -20.00, 21.5000, 't'),
(26, 2, 'Sorvetes', 16.00, 70.00, 1, 'N/A', -25.00, 16.0000, 't'),
(27, 2, 'Produtos farmacêuticos', 14.00, 55.00, 1, 'N/A', 5.00, 14.0000, 't'),
(28, 2, 'Flores frescas', 8.50, 80.00, 2, 'N/A', 4.00, 8.5000, 't'),
(29, 2, 'Sumos concentrados', 22.00, 58.00, 2, 'N/A', -10.00, 22.0000, 't'),

-- Carga perigosa em contentor
(7, 3, 'Solventes orgânicos', 24.00, 66.00, 1, '3', NULL, 24.0000, 't'),
(8, 3, 'Hipoclorito de sódio', 21.50, 60.00, 2, '8', NULL, 21.5000, 't'),
(9, 3, 'Aerossóis UN1950', 15.00, 50.00, 3, '2.1', NULL, 12000.0000, 'un'),
(10, 3, 'Pesticidas classe 6.1', 22.00, 62.00, 1, '6.1', NULL, 22.0000, 't'),
(30, 3, 'Peróxidos orgânicos', 18.00, 55.00, 1, '5.2', NULL, 18.0000, 't'),
(31, 3, 'Baterias de lítio', 12.50, 45.00, 2, '9', NULL, 12.5000, 't'),
(32, 3, 'Resinas inflamáveis', 23.00, 60.00, 2, '3', NULL, 23.0000, 't'),
(33, 3, 'Material radioativo', 5.00, 30.00, 1, '7', NULL, 5.0000, 't'),

-- Líquidos a granel
(11, 4, 'CPP — parcela Rotterdam A', 8500.00, 10000.00, 1, 'N/A', NULL, 10000.0000, 'm3'),
(12, 4, 'CPP — parcela Rotterdam B', 6400.00, 7500.00, 2, 'N/A', NULL, 7500.0000, 'm3'),
(13, 4, 'Nafta leve', 3200.00, 4000.00, 1, '3', NULL, 4000.0000, 'm3'),
(14, 4, 'Gasóleo marítimo MGO', 2100.00, 2500.00, 2, 'N/A', NULL, 2500.0000, 'm3'),
(15, 4, 'Óleo base lubrificante', 1800.00, 2000.00, 3, 'N/A', NULL, 2000.0000, 'm3'),
(34, 4, 'Gasolina 95', 6800.00, 8000.00, 1, '3', NULL, 8000.0000, 'm3'),
(35, 4, 'Querosene de aviação', 7500.00, 9000.00, 1, '3', NULL, 9000.0000, 'm3'),
(36, 4, 'Etanol anidro', 5600.00, 7000.00, 2, '3', NULL, 7000.0000, 'm3'),
(37, 4, 'Ácido sulfúrico', 18400.00, 10000.00, 1, '8', NULL, 10000.0000, 'm3'),
(38, 4, 'Soda cáustica', 13500.00, 8500.00, 1, '8', NULL, 8500.0000, 'm3'),

-- Granel sólido
(39, 5, 'Cereais (trigo)', 25000.00, 35000.00, 2, 'N/A', NULL, 25000.0000, 't'),
(40, 5, 'Minério de ferro', 45000.00, 25000.00, 1, 'N/A', NULL, 45000.0000, 't'),
(41, 5, 'Carvão', 35000.00, 40000.00, 2, 'N/A', NULL, 35000.0000, 't'),
(42, 5, 'Cimento', 28000.00, 22000.00, 1, 'N/A', NULL, 28000.0000, 't'),

-- Carga Ro-Ro
(43, 6, 'Tratores agrícolas', 45.00, 120.00, 1, 'N/A', NULL, 45.0000, 't'),
(44, 6, 'Contentores refrigerados em chassis', 28.00, 70.00, 2, 'N/A', -18.00, 28.0000, 't'),
(45, 6, 'Autocarros usados', 38.00, 150.00, 2, 'N/A', NULL, 38.0000, 't'),
(46, 6, 'Veículos todo-o-terreno 4x4', 8.50, 30.00, 3, 'N/A', NULL, 1700.0000, 'un'),

-- Carga de projecto
(47, 7, 'Pás eólicas', 65.00, 450.00, 1, 'N/A', NULL, 65.0000, 't'),
(48, 7, 'Gerador industrial', 120.00, 280.00, 1, 'N/A', NULL, 120.0000, 't'),
(49, 7, 'Transformador elétrico', 95.00, 180.00, 1, 'N/A', NULL, 95.0000, 't'),

-- Gás
(50, 8, 'Gás natural liquefeito (LNG)', 35000.00, 80000.00, 1, '2.1', -162.00, 80000.0000, 'm3'),
(51, 8, 'Gás de petróleo liquefeito (LPG)', 25000.00, 55000.00, 1, '2.1', NULL, 55000.0000, 'm3');

-- -----------------------------------------------------
-- CONTAINER_TYPE
-- -----------------------------------------------------
INSERT INTO container_type (id, name, length, width, height, max_weight) VALUES
(1, '40'' HC', 12.20, 2.44, 2.90, 30.48),
(2, '20'' Dry', 6.06, 2.44, 2.59, 28.00),
(3, '40'' Dry', 12.20, 2.44, 2.59, 30.48),
(4, '20'' Reefer', 5.90, 2.44, 2.59, 27.00),
(5, '40'' HC Reefer', 12.20, 2.44, 2.90, 30.00),
(6, '20'' Open Top', 6.06, 2.44, 2.59, 25.00),
(7, '40'' Flat Rack', 12.20, 2.44, 2.59, 40.00),
(8, '45'' HC Pallet Wide', 13.72, 2.50, 2.90, 32.00);

-- -----------------------------------------------------
-- SHIP (Navios)
-- -----------------------------------------------------

-- Navio 1: Porta-contentores
INSERT INTO ship (
    id, id_company, id_ship_type, id_fuel_efficiency,
    name, built_year, imo_number, gt, dwt, height, length, width, max_draft, crew_size,
    ukc_margin, max_bending_moment, max_shear_force, speed_knots, description,
    lightweight, lcg, vcg, tcg,
    gm_min_admissible, max_trim_meters, max_trim_percent_loa, max_list_angle_deg,
    default_water_density_kg_m3
) VALUES (
    1, 1, 1, 1,
    'MSC Irina', 2016, 'IMO9270001',
    25000.00, 42000.00, 24.50, 200.00, 32.20, 14.80, 24,
    1.20, 520000.00, 410000.00, 19.00,
    'Porta-contentores da Mediterranean Shipping Company.',
    11800.00, 0.0000, 8.2000, 0.0000,
    1.2000, 2.50, 1.500, 12.00,
    1025.00
);

-- Navio 2: Tanqueiro
INSERT INTO ship (
    id, id_company, id_ship_type, id_fuel_efficiency,
    name, built_year, imo_number, gt, dwt, height, length, width, max_draft, crew_size,
    ukc_margin, max_bending_moment, max_shear_force, speed_knots, description,
    lightweight, lcg, vcg, tcg,
    gm_min_admissible, max_trim_meters, max_trim_percent_loa, max_list_angle_deg,
    default_water_density_kg_m3
) VALUES (
    2, 5, 2, 2,
    'Maersk Navigator', 2014, 'IMO9270002',
    42000.00, 75000.00, 22.00, 228.00, 32.26, 15.20, 28,
    1.35, 680000.00, 520000.00, 14.50,
    'Navio tanqueiro da frota Maersk.',
    18500.00, 2.5000, 7.8000, 0.0000,
    1.0000, 3.00, 2.000, 10.00,
    1025.00
);

-- Navio 3: ConRo
INSERT INTO ship (
    id, id_company, id_ship_type, id_fuel_efficiency,
    name, built_year, imo_number, gt, dwt, height, length, width, max_draft, crew_size,
    ukc_margin, max_bending_moment, max_shear_force, speed_knots, description,
    lightweight, lcg, vcg, tcg,
    gm_min_admissible, max_trim_meters, max_trim_percent_loa, max_list_angle_deg,
    default_water_density_kg_m3
) VALUES (
    3, 3, 7, 5,
    'Portline Navigator', 2019, 'IMO9876500',
    28500.00, 38500.00, 22.50, 210.00, 30.50, 13.50, 22,
    1.00, 480000.00, 380000.00, 18.00,
    'Navio misto contentores e Ro-Ro da Portline.',
    13500.00, -2.5000, 9.2000, 0.0000,
    1.1500, 2.50, 1.400, 10.00,
    1025.00
);

-- Navio 4: Graneleiro
INSERT INTO ship (
    id, id_company, id_ship_type, id_fuel_efficiency,
    name, built_year, imo_number, gt, dwt, height, length, width, max_draft, crew_size,
    ukc_margin, max_bending_moment, max_shear_force, speed_knots, description,
    lightweight, lcg, vcg, tcg,
    gm_min_admissible, max_trim_meters, max_trim_percent_loa, max_list_angle_deg,
    default_water_density_kg_m3
) VALUES (
    4, 5, 4, 7,
    'Maersk Bulker', 2012, 'IMO9365200',
    55000.00, 92000.00, 20.00, 260.00, 38.00, 16.80, 26,
    1.40, 750000.00, 560000.00, 13.50,
    'Graneleiro para minério e cereais da Maersk.',
    23500.00, 3.2000, 8.5000, 0.0000,
    0.9500, 3.50, 1.800, 12.00,
    1025.00
);

-- Navio 5: PCTC
INSERT INTO ship (
    id, id_company, id_ship_type, id_fuel_efficiency,
    name, built_year, imo_number, gt, dwt, height, length, width, max_draft, crew_size,
    ukc_margin, max_bending_moment, max_shear_force, speed_knots, description,
    lightweight, lcg, vcg, tcg,
    gm_min_admissible, max_trim_meters, max_trim_percent_loa, max_list_angle_deg,
    default_water_density_kg_m3
) VALUES (
    5, 7, 5, 3,
    'Auto Atlantic', 2020, 'IMO9987650',
    42000.00, 28500.00, 28.50, 200.00, 32.80, 10.80, 18,
    0.80, 420000.00, 310000.00, 16.00,
    'Porta-automóveis da Atlantic RoRo Solutions.',
    17800.00, -4.8000, 12.5000, 0.0000,
    1.3000, 2.00, 1.200, 8.00,
    1025.00
);

-- Navio 6: LNG Carrier
INSERT INTO ship (
    id, id_company, id_ship_type, id_fuel_efficiency,
    name, built_year, imo_number, gt, dwt, height, length, width, max_draft, crew_size,
    ukc_margin, max_bending_moment, max_shear_force, speed_knots, description,
    lightweight, lcg, vcg, tcg,
    gm_min_admissible, max_trim_meters, max_trim_percent_loa, max_list_angle_deg,
    default_water_density_kg_m3
) VALUES (
    6, 1, 2, 2,
    'MSC LNG Abidjan', 2018, 'IMO9448200',
    112000.00, 98000.00, 26.00, 295.00, 46.00, 12.00, 32,
    1.50, 890000.00, 690000.00, 19.50,
    'Transportador de GNL da frota MSC.',
    38500.00, 1.2000, 12.8000, 0.0000,
    1.5000, 2.00, 1.000, 5.00,
    1025.00
);

-- Navio 7: Feeder contentores pequeno
INSERT INTO ship (
    id, id_company, id_ship_type, id_fuel_efficiency,
    name, built_year, imo_number, gt, dwt, height, length, width, max_draft, crew_size,
    ukc_margin, max_bending_moment, max_shear_force, speed_knots, description,
    lightweight, lcg, vcg, tcg,
    gm_min_admissible, max_trim_meters, max_trim_percent_loa, max_list_angle_deg,
    default_water_density_kg_m3
) VALUES (
    7, 4, 1, 6,
    'CMA CGM Tagus', 2015, 'IMO9214500',
    12500.00, 18500.00, 16.00, 142.00, 23.40, 9.80, 12,
    0.85, 280000.00, 210000.00, 14.00,
    'Feeder da CMA CGM para rotas europeias costeiras.',
    7200.00, -1.5000, 6.8000, 0.0000,
    1.2000, 1.80, 1.500, 10.00,
    1025.00
);

-- -----------------------------------------------------
-- TANK (Navio 1)
-- -----------------------------------------------------
INSERT INTO tank (id, id_ship, id_tank_type, name, capacity_m3, lcv, vcv, tcv) VALUES
(1, 1, 1, 'Alpha — lastro central', 2500.0000, -5.0000, 3.2000, 0.0000),
(2, 1, 2, 'Alpha — MGO', 1200.0000, 12.0000, 2.8000, 1.2000);

-- -----------------------------------------------------
-- TANK (Navio 2)
-- -----------------------------------------------------
INSERT INTO tank (id, id_ship, id_tank_type, name, capacity_m3, lcv, vcv, tcv) VALUES
(3, 2, 1, 'Beta — lastro 1', 4200.0000, -35.0000, 3.0000, 0.0000),
(4, 2, 2, 'Beta — fuelóleo', 2100.0000, 18.0000, 2.6000, 0.8000),
(5, 2, 4, 'Beta — carga líquida centro', 12000.0000, 5.0000, 4.5000, 0.0000),
(6, 2, 4, 'Beta — carga líquida popa', 9500.0000, 45.0000, 4.2000, 0.0000),
(7, 2, 4, 'Beta — carga líquida proa', 3500.0000, -28.0000, 4.0000, 0.0000);

-- -----------------------------------------------------
-- TANK (Navio 3 - ConRo)
-- -----------------------------------------------------
INSERT INTO tank (id, id_ship, id_tank_type, name, capacity_m3, lcv, vcv, tcv) VALUES
(8, 3, 1, 'Atlantic — lastro central', 2800.0000, -8.0000, 3.5000, 0.0000),
(9, 3, 1, 'Atlantic — lastro lateral E', 1800.0000, -3.0000, 3.5000, -8.0000),
(10, 3, 1, 'Atlantic — lastro lateral W', 1800.0000, -3.0000, 3.5000, 8.0000),
(11, 3, 2, 'Atlantic — MGO', 950.0000, 15.0000, 2.5000, 2.5000),
(12, 3, 3, 'Atlantic — água doce', 250.0000, -5.0000, 6.2000, 0.0000);

-- -----------------------------------------------------
-- TANK (Navio 4 - Graneleiro)
-- -----------------------------------------------------
INSERT INTO tank (id, id_ship, id_tank_type, name, capacity_m3, lcv, vcv, tcv) VALUES
(13, 4, 1, 'Bulk — lastro fundo central', 6500.0000, -15.5000, 2.8000, 0.0000),
(14, 4, 1, 'Bulk — lastro lateral E1', 2200.0000, -8.0000, 3.2000, -9.5000),
(15, 4, 1, 'Bulk — lastro lateral W1', 2200.0000, -8.0000, 3.2000, 9.5000),
(16, 4, 1, 'Bulk — lastro lateral E2', 1800.0000, 22.0000, 3.2000, -9.5000),
(17, 4, 1, 'Bulk — lastro lateral W2', 1800.0000, 22.0000, 3.2000, 9.5000),
(18, 4, 2, 'Bulk — fuelóleo', 1850.0000, 28.5000, 2.2000, 3.2000),
(19, 4, 3, 'Bulk — água doce', 450.0000, -8.0000, 7.8000, 0.0000);

-- -----------------------------------------------------
-- TANK (Navio 5 - PCTC)
-- -----------------------------------------------------
INSERT INTO tank (id, id_ship, id_tank_type, name, capacity_m3, lcv, vcv, tcv) VALUES
(20, 5, 1, 'Auto — lastro duplo fundo', 4500.0000, -12.0000, 2.5000, 0.0000),
(21, 5, 2, 'Auto — MGO', 1200.0000, 10.5000, 3.8000, 4.0000),
(22, 5, 3, 'Auto — água doce', 320.0000, -6.0000, 9.2000, 0.0000);

-- -----------------------------------------------------
-- TANK (Navio 6 - LNG)
-- -----------------------------------------------------
INSERT INTO tank (id, id_ship, id_tank_type, name, capacity_m3, lcv, vcv, tcv) VALUES
(23, 6, 1, 'LNG — lastro central', 12000.0000, -45.0000, 5.2000, 0.0000),
(24, 6, 1, 'LNG — lastro lateral E', 5800.0000, -20.0000, 5.2000, -12.0000),
(25, 6, 1, 'LNG — lastro lateral W', 5800.0000, -20.0000, 5.2000, 12.0000),
(26, 6, 2, 'LNG — fuelóleo', 3200.0000, 25.0000, 4.8000, 0.0000),
(27, 6, 4, 'LNG — tanque cargo 1', 40000.0000, -35.0000, 10.5000, 0.0000),
(28, 6, 4, 'LNG — tanque cargo 2', 40000.0000, 15.0000, 10.5000, 0.0000);

-- -----------------------------------------------------
-- TANK (Navio 7 - Feeder)
-- -----------------------------------------------------
INSERT INTO tank (id, id_ship, id_tank_type, name, capacity_m3, lcv, vcv, tcv) VALUES
(29, 7, 1, 'Feeder — lastro duplo fundo', 2200.0000, -6.5000, 2.2000, 0.0000),
(30, 7, 2, 'Feeder — MGO', 450.0000, 8.0000, 2.5000, 1.2000),
(31, 7, 3, 'Feeder — água doce', 120.0000, -3.0000, 5.5000, 0.0000);

-- -----------------------------------------------------
-- TANK_FILL_CURVE
-- -----------------------------------------------------
INSERT INTO tank_fill_curve (id, id_tank, level_m, volume_m3) VALUES
-- Navio 1
(1, 1, 0.0000, 0.000), (2, 1, 2.5000, 800.000), (3, 1, 5.0000, 1800.000), (4, 1, 7.8000, 2500.000),
(5, 2, 0.0000, 0.000), (6, 2, 1.2000, 400.000), (7, 2, 2.4000, 1200.000),

-- Navio 2
(8, 3, 0.0000, 0.000), (9, 3, 4.0000, 2000.000), (10, 3, 8.5000, 4200.000),
(11, 4, 0.0000, 0.000), (12, 4, 2.0000, 1050.000), (13, 4, 4.0000, 2100.000),
(14, 5, 0.0000, 0.000), (15, 5, 5.0000, 5000.000), (16, 5, 10.0000, 12000.000),
(17, 6, 0.0000, 0.000), (18, 6, 4.0000, 4500.000), (19, 6, 8.1000, 9500.000),
(32, 7, 0.0000, 0.000), (33, 7, 3.0000, 1500.000), (34, 7, 6.2000, 3500.000),

-- Navio 3
(100, 8, 0, 0), (101, 8, 3.5, 1400), (102, 8, 7.0, 2800),
(103, 9, 0, 0), (104, 9, 3.0, 900), (105, 9, 6.0, 1800),
(106, 10, 0, 0), (107, 10, 3.0, 900), (108, 10, 6.0, 1800),
(109, 11, 0, 0), (110, 11, 2.5, 475), (111, 11, 5.0, 950),
(112, 12, 0, 0), (113, 12, 1.5, 125), (114, 12, 3.0, 250),

-- Navio 4
(115, 13, 0, 0), (116, 13, 4.0, 3250), (117, 13, 8.0, 6500),
(118, 14, 0, 0), (119, 14, 3.0, 1100), (120, 14, 6.0, 2200),
(121, 15, 0, 0), (122, 15, 3.0, 1100), (123, 15, 6.0, 2200),
(124, 16, 0, 0), (125, 16, 2.5, 900), (126, 16, 5.0, 1800),
(127, 17, 0, 0), (128, 17, 2.5, 900), (129, 17, 5.0, 1800),
(130, 18, 0, 0), (131, 18, 2.5, 925), (132, 18, 5.0, 1850),
(133, 19, 0, 0), (134, 19, 1.8, 225), (135, 19, 3.6, 450),

-- Navio 5
(136, 20, 0, 0), (137, 20, 3.0, 2250), (138, 20, 6.0, 4500),
(139, 21, 0, 0), (140, 21, 2.0, 600), (141, 21, 4.0, 1200),
(142, 22, 0, 0), (143, 22, 1.5, 160), (144, 22, 3.0, 320),

-- Navio 6
(145, 23, 0, 0), (146, 23, 4.0, 6000), (147, 23, 8.0, 12000),
(148, 24, 0, 0), (149, 24, 3.5, 2900), (150, 24, 7.0, 5800),
(151, 25, 0, 0), (152, 25, 3.5, 2900), (153, 25, 7.0, 5800),
(154, 26, 0, 0), (155, 26, 2.5, 1600), (156, 26, 5.0, 3200),
(157, 27, 0, 0), (158, 27, 8.0, 20000), (159, 27, 16.0, 40000),
(160, 28, 0, 0), (161, 28, 8.0, 20000), (162, 28, 16.0, 40000),

-- Navio 7
(163, 29, 0, 0), (164, 29, 2.5, 1100), (165, 29, 5.0, 2200),
(166, 30, 0, 0), (167, 30, 1.8, 225), (168, 30, 3.6, 450),
(169, 31, 0, 0), (170, 31, 1.0, 60), (171, 31, 2.0, 120);

-- -----------------------------------------------------
-- TANK_STABILITY_CURVE
-- -----------------------------------------------------
INSERT INTO tank_stability_curve (id, id_tank, volume_m3, liquid_lcg, liquid_vcg, liquid_tcg, fsm_t_m) VALUES
-- Navio 1
(1, 1, 0.000, NULL, NULL, NULL, 0.000000),
(2, 1, 1250.000, -5.0000, 3.1500, 0.0000, 850.000000),
(3, 1, 2500.000, NULL, NULL, NULL, 0.000000),
(4, 2, 0.000, NULL, NULL, NULL, 0.000000),
(5, 2, 600.000, 12.0000, 2.8200, 1.2000, 120.000000),
(6, 2, 1200.000, NULL, NULL, NULL, 0.000000),

-- Navio 2
(20, 3, 0.000, NULL, NULL, NULL, 0.000000),
(21, 3, 2100.000, -35.0000, 2.9500, 0.0000, 1100.000000),
(22, 3, 4200.000, NULL, NULL, NULL, 0.000000),
(23, 4, 0.000, NULL, NULL, NULL, 0.000000),
(24, 4, 1050.000, 18.0000, 2.5800, 0.8000, 95.000000),
(25, 4, 2100.000, NULL, NULL, NULL, 0.000000),
(26, 5, 0.000, NULL, NULL, NULL, 0.000000),
(27, 5, 6000.000, 5.0000, 4.4800, 0.0000, 4200.000000),
(28, 5, 12000.000, NULL, NULL, NULL, 0.000000),
(29, 6, 0.000, NULL, NULL, NULL, 0.000000),
(30, 6, 4750.000, 45.0000, 4.1800, 0.0000, 3100.000000),
(31, 6, 9500.000, NULL, NULL, NULL, 0.000000),
(35, 7, 0.000, NULL, NULL, NULL, 0.000000),
(36, 7, 1750.000, -28.0000, 3.9800, 0.0000, 280.000000),
(37, 7, 3500.000, NULL, NULL, NULL, 0.000000),

-- Navio 3
(200, 8, 0, NULL, NULL, NULL, 0),
(201, 8, 1400, -8.0000, 3.4000, 0.0000, 1200),
(202, 8, 2800, NULL, NULL, NULL, 0),
(203, 9, 0, NULL, NULL, NULL, 0),
(204, 9, 900, -3.0000, 3.3000, -8.0000, 850),
(205, 9, 1800, NULL, NULL, NULL, 0),
(206, 10, 0, NULL, NULL, NULL, 0),
(207, 10, 900, -3.0000, 3.3000, 8.0000, 850),
(208, 10, 1800, NULL, NULL, NULL, 0),
(209, 11, 0, NULL, NULL, NULL, 0),
(210, 11, 475, 15.0000, 2.4500, 2.5000, 180),
(211, 11, 950, NULL, NULL, NULL, 0),
(212, 12, 0, NULL, NULL, NULL, 0),
(213, 12, 125, -5.0000, 6.1000, 0.0000, 45),
(214, 12, 250, NULL, NULL, NULL, 0),

-- Navio 5
(215, 20, 0, NULL, NULL, NULL, 0),
(216, 20, 2250, -12.0000, 2.4500, 0.0000, 950),
(217, 20, 4500, NULL, NULL, NULL, 0),
(218, 21, 0, NULL, NULL, NULL, 0),
(219, 21, 600, 10.5000, 3.7500, 4.0000, 140),
(220, 21, 1200, NULL, NULL, NULL, 0),
(221, 22, 0, NULL, NULL, NULL, 0),
(222, 22, 160, -6.0000, 9.1500, 0.0000, 50),
(223, 22, 320, NULL, NULL, NULL, 0),

-- Navio 6
(224, 27, 0, NULL, NULL, NULL, 0),
(225, 27, 20000, -35.0000, 10.2000, 0.0000, 18500),
(226, 27, 40000, NULL, NULL, NULL, 0),
(227, 28, 0, NULL, NULL, NULL, 0),
(228, 28, 20000, 15.0000, 10.2000, 0.0000, 18500),
(229, 28, 40000, NULL, NULL, NULL, 0);

-- -----------------------------------------------------
-- CONTAINER
-- -----------------------------------------------------
INSERT INTO container (registration, id_container_type, tare_weight, gross_weight, cg_offset_v_m) VALUES
-- Navio Alpha
('MSCU1111111', 1, 3.90, 22.50, 0.0000),
('MSCU2222222', 1, 3.90, 18.20, 0.0000),
('MSCU3333333', 1, 4.10, 20.10, 0.0200),
('MSCU4444444', 1, 3.85, 24.00, 0.0500),
('MSCU5555555', 1, 3.88, 22.00, 0.0000),
('MSCU6666666', 1, 3.92, 21.50, 0.0300),
('MSCU7777777', 1, 3.80, 15.00, 0.0100),

-- Contentores adicionais
('MAEU1234567', 2, 2.20, 18.50, 0.0000),
('MAEU1234568', 2, 2.20, 22.00, 0.0000),
('MAEU1234569', 3, 3.70, 26.50, 0.0100),
('MAEU1234570', 1, 3.90, 28.00, 0.0200),
('MAEU1234571', 4, 2.40, 21.50, 0.0000),
('MAEU1234572', 5, 4.10, 25.00, 0.0300),
('MAEU1234573', 5, 4.10, 22.00, 0.0000),

('SCXU9876543', 1, 3.85, 24.50, 0.0100),
('SCXU9876544', 1, 3.90, 20.00, 0.0000),
('SCXU9876545', 2, 2.15, 16.80, 0.0000),
('SCXU9876546', 3, 3.75, 27.00, 0.0200),
('SCXU9876547', 1, 3.88, 23.50, 0.0000),

('ONEU4444111', 1, 3.92, 25.00, 0.0100),
('ONEU4444112', 5, 4.20, 28.00, 0.0400),
('ONEU4444113', 2, 2.18, 19.50, 0.0000),
('ONEU4444114', 1, 3.87, 26.00, 0.0000),
('ONEU4444115', 3, 3.72, 24.00, 0.0100),
('ONEU4444116', 4, 2.35, 23.00, 0.0000),

('HLCU8888881', 1, 3.95, 27.50, 0.0200),
('HLCU8888882', 1, 3.88, 21.50, 0.0000),
('HLCU8888883', 2, 2.22, 17.50, 0.0000),
('HLCU8888884', 5, 4.15, 24.00, 0.0300),

('COSU5555111', 1, 3.90, 22.00, 0.0000),
('COSU5555112', 1, 3.85, 19.80, 0.0100),
('COSU5555113', 2, 2.20, 18.00, 0.0000),
('COSU5555114', 3, 3.80, 25.50, 0.0000),

('APLU9999991', 1, 3.92, 24.00, 0.0100),
('APLU9999992', 4, 2.38, 22.00, 0.0000),
('APLU9999993', 5, 4.08, 26.00, 0.0200),
('APLU9999994', 1, 3.86, 23.00, 0.0000);

-- -----------------------------------------------------
-- CONTAINER_SLOT
-- -----------------------------------------------------
-- Navio 1 (Alpha)
INSERT INTO container_slot (id, id_ship, bay, row, tier, max_weight, slot_lcg, slot_vcg, slot_tcg) VALUES
(1, 1, 12, 2, 4, 32.00, 15.5000, 18.2000, -2.4000),
(2, 1, 12, 2, 3, 32.00, 15.5000, 15.3000, -2.4000),
(3, 1, 14, 1, 2, 32.00, 22.0000, 12.1000, 0.0000),
(4, 1, 14, 1, 3, 32.00, 22.0000, 15.2000, 0.0000),
(5, 1, 14, 2, 2, 32.00, 22.0000, 12.1000, 2.4000),
(6, 1, 16, 1, 2, 32.00, 28.0000, 12.1000, 0.0000),
(7, 1, 16, 1, 3, 32.00, 28.0000, 15.2000, 0.0000),
(8, 1, 12, 1, 2, 32.00, 15.5000, 12.1000, 0.0000),
(9, 1, 12, 3, 2, 32.00, 15.5000, 12.1000, 4.8000),
(10, 1, 14, 2, 3, 32.00, 22.0000, 15.2000, 2.4000),
(11, 1, 16, 2, 2, 32.00, 28.0000, 12.1000, 2.4000),
(12, 1, 16, 2, 3, 32.00, 28.0000, 15.2000, 2.4000),
(13, 1, 18, 1, 2, 32.00, 34.0000, 12.1000, 0.0000),
(14, 1, 18, 1, 3, 32.00, 34.0000, 15.2000, 0.0000),
(15, 1, 18, 2, 2, 32.00, 34.0000, 12.1000, 2.4000);

-- Navio 7 (Feeder)
INSERT INTO container_slot (id, id_ship, bay, row, tier, max_weight, slot_lcg, slot_vcg, slot_tcg) VALUES
(16, 7, 5, 1, 2, 28.00, -18.0000, 6.8000, 0.0000),
(17, 7, 5, 2, 2, 28.00, -18.0000, 6.8000, -1.5000),
(18, 7, 5, 3, 2, 28.00, -18.0000, 6.8000, 1.5000),
(19, 7, 8, 1, 2, 28.00, -5.0000, 6.8000, 0.0000),
(20, 7, 8, 2, 2, 28.00, -5.0000, 6.8000, -1.5000),
(21, 7, 8, 3, 2, 28.00, -5.0000, 6.8000, 1.5000),
(22, 7, 11, 1, 2, 28.00, 8.0000, 6.8000, 0.0000),
(23, 7, 11, 2, 2, 28.00, 8.0000, 6.8000, -1.5000),
(24, 7, 11, 3, 2, 28.00, 8.0000, 6.8000, 1.5000);

-- -----------------------------------------------------
-- SAILING
-- -----------------------------------------------------
INSERT INTO sailing (id, id_ship, id_route, id_weather_condition, fuel_price_per_ton, estimated_arrival_time, water_density_kg_m3) VALUES
(1, 1, 1, 1, 685.00, '2026-05-15 08:00:00', 1025.00),
(2, 2, 2, 2, 672.00, '2026-06-10 06:00:00', 1025.00),
(3, 1, 3, 1, 688.00, '2026-07-22 14:00:00', 1025.00),
(4, 2, 2, 2, 670.00, '2026-08-01 06:00:00', 1025.00),
(5, 1, 4, 3, 680.00, '2026-01-15 10:00:00', 1025.00),
(6, 1, 6, 1, 690.00, '2026-02-20 14:30:00', 1025.00),
(7, 1, 1, 1, 685.00, '2026-03-10 08:00:00', 1025.00),
(8, 1, 3, 1, 688.00, '2026-04-05 16:00:00', 1025.00),
(9, 2, 5, 2, 675.00, '2026-01-25 09:00:00', 1025.00),
(10, 2, 8, 1, 690.00, '2026-03-15 07:00:00', 1025.00),
(11, 2, 2, 2, 672.00, '2026-04-20 11:00:00', 1025.00),
(12, 3, 4, 3, 650.00, '2026-02-05 08:30:00', 1025.00),
(13, 3, 6, 1, 660.00, '2026-03-18 15:00:00', 1025.00),
(14, 3, 12, 2, 645.00, '2026-05-02 09:00:00', 1025.00),
(15, 3, 4, 1, 655.00, '2026-06-12 17:00:00', 1025.00),
(16, 4, 5, 1, 660.00, '2026-01-30 07:00:00', 1025.00),
(17, 4, 10, 2, 670.00, '2026-03-22 14:00:00', 1025.00),
(18, 4, 8, 1, 680.00, '2026-05-10 08:00:00', 1025.00),
(19, 5, 12, 2, 630.00, '2026-02-12 10:00:00', 1025.00),
(20, 5, 7, 2, 620.00, '2026-03-25 13:00:00', 1025.00),
(21, 5, 4, 1, 640.00, '2026-05-18 09:30:00', 1025.00),
(22, 6, 5, 3, 690.00, '2026-03-05 06:00:00', 1025.00),
(23, 6, 8, 2, 695.00, '2026-06-20 11:00:00', 1025.00),
(24, 7, 7, 2, 610.00, '2026-01-18 14:00:00', 1025.00),
(25, 7, 4, 1, 615.00, '2026-02-28 09:00:00', 1025.00),
(26, 7, 7, 2, 608.00, '2026-03-30 16:00:00', 1025.00),
(27, 7, 12, 2, 612.00, '2026-04-25 10:30:00', 1025.00),
(28, 7, 7, 1, 614.00, '2026-06-05 08:00:00', 1025.00);

-- -----------------------------------------------------
-- SHIPMENT
-- -----------------------------------------------------
INSERT INTO shipment (id, id_sailing, id_cargo) VALUES
(1, 1, 1), (2, 1, 2), (3, 1, 4), (4, 1, 7), (5, 1, 10),
(6, 3, 8), (7, 3, 9),
(8, 2, 11), (9, 2, 12), (10, 4, 13), (11, 4, 14), (12, 4, 15),
(13, 5, 16), (14, 5, 17), (15, 5, 5),
(16, 6, 18), (17, 6, 19), (18, 6, 20),
(19, 7, 21), (20, 7, 22), (21, 7, 23),
(22, 8, 24), (23, 8, 25), (24, 8, 26), (25, 8, 27),
(26, 9, 34), (27, 9, 35),
(28, 10, 36), (29, 10, 37),
(30, 11, 38), (31, 11, 15),
(32, 12, 43), (33, 12, 44), (34, 12, 16),
(35, 13, 45), (36, 13, 2), (37, 13, 5),
(38, 14, 46), (39, 14, 47),
(40, 15, 48), (41, 15, 49),
(42, 16, 39), (43, 16, 40),
(44, 17, 41), (45, 17, 42),
(46, 18, 41), (47, 18, 39),
(48, 19, 46), (49, 19, 43),
(50, 20, 46), (51, 20, 45),
(52, 21, 44), (53, 21, 46),
(54, 22, 50),
(55, 23, 51),
(56, 24, 1), (57, 24, 2), (58, 24, 4),
(59, 25, 7), (60, 25, 8), (61, 25, 30),
(62, 26, 16), (63, 26, 17), (64, 26, 18),
(65, 27, 3), (66, 27, 19), (67, 27, 20),
(68, 28, 21), (69, 28, 22), (70, 28, 23), (71, 28, 26);

-- -----------------------------------------------------
-- CONTAINER_STORAGE
-- -----------------------------------------------------
INSERT INTO container_storage (id, id_container_slot, container_registration, id_shipment) VALUES
(1, 1, 'MSCU1111111', 1),
(2, 2, 'MSCU2222222', 2),
(3, 3, 'MSCU3333333', 3),
(4, 4, 'MSCU4444444', 4),
(5, 5, 'MSCU5555555', 5),
(6, 6, 'MSCU6666666', 6),
(7, 7, 'MSCU7777777', 7),
(8, 8, 'MAEU1234567', 13),
(9, 9, 'MAEU1234568', 14),
(10, 10, 'MAEU1234569', 15),
(11, 11, 'MAEU1234570', 16),
(12, 12, 'MAEU1234571', 17),
(13, 13, 'MAEU1234572', 18),
(14, 14, 'MAEU1234573', 19),
(15, 15, 'SCXU9876543', 20),
(16, 16, 'SCXU9876544', 56),
(17, 17, 'SCXU9876545', 57),
(18, 18, 'SCXU9876546', 58),
(19, 19, 'SCXU9876547', 59),
(20, 20, 'ONEU4444111', 60),
(21, 21, 'ONEU4444112', 61),
(22, 22, 'ONEU4444113', 62),
(23, 23, 'ONEU4444114', 63),
(24, 24, 'ONEU4444115', 64);

-- -----------------------------------------------------
-- LIQUID_STORAGE
-- -----------------------------------------------------
INSERT INTO liquid_storage (id, id_shipment, id_tank, volume_m3, cargo_density_kg_m3) VALUES
(1, 8, 5, 10000.000, 850.0000),
(2, 9, 6, 7500.000, 853.3333),
(3, 10, 5, 4000.000, 800.0000),
(4, 11, 6, 2500.000, 840.0000),
(5, 12, 7, 2000.000, 900.0000),
(6, 26, 5, 8000.000, 850.0000),
(7, 27, 6, 9000.000, 833.3333),
(8, 28, 5, 7000.000, 800.0000),
(9, 29, 6, 2200.000, 840.0000),
(10, 30, 7, 1500.000, 900.0000),
(11, 31, 5, 2500.000, 800.0000),
(12, 54, 27, 38000.000, 425.0000),
(13, 55, 28, 52000.000, 510.0000);

-- -----------------------------------------------------
-- SHIP_HYDROSTATIC_CURVE
-- -----------------------------------------------------
INSERT INTO ship_hydrostatic_curve (id, id_ship, displacement, draft, KM, KB, LCB, TPC, MCTC) VALUES
-- Navio 1
(1, 1, 15000.00, 8.50, 12.80, 4.60, 0.50, 42.00, 850.00),
(2, 1, 25000.00, 11.20, 11.50, 5.80, 1.20, 48.00, 920.00),
(3, 1, 35000.00, 13.80, 10.40, 6.90, 1.80, 52.00, 980.00),
(4, 1, 45000.00, 14.70, 9.90, 7.40, 2.10, 54.00, 1000.00),

-- Navio 2
(5, 2, 28000.00, 9.20, 11.20, 5.10, 1.00, 55.00, 1050.00),
(6, 2, 45000.00, 11.50, 10.10, 6.20, 1.60, 62.00, 1180.00),
(7, 2, 62000.00, 13.40, 9.40, 7.00, 2.00, 66.00, 1250.00),
(8, 2, 78000.00, 14.80, 8.90, 7.60, 2.30, 68.00, 1280.00),

-- Navio 3
(9, 3, 15000.00, 6.50, 11.20, 4.20, -2.50, 38.00, 720.00),
(10, 3, 25000.00, 8.80, 10.40, 5.10, -1.80, 44.00, 810.00),
(11, 3, 35000.00, 11.00, 9.70, 5.90, -1.00, 48.00, 880.00),
(12, 3, 42000.00, 12.50, 9.20, 6.40, -0.50, 50.00, 920.00),

-- Navio 4
(13, 4, 35000.00, 8.20, 12.50, 4.80, 2.20, 65.00, 1250.00),
(14, 4, 55000.00, 10.50, 11.20, 5.70, 2.80, 72.00, 1380.00),
(15, 4, 75000.00, 13.00, 10.40, 6.50, 3.20, 78.00, 1460.00),
(16, 4, 95000.00, 15.50, 9.80, 7.20, 3.60, 82.00, 1520.00),

-- Navio 5
(17, 5, 15000.00, 5.50, 14.20, 3.80, -4.50, 42.00, 880.00),
(18, 5, 22000.00, 7.20, 13.80, 4.60, -4.00, 46.00, 950.00),
(19, 5, 29000.00, 9.00, 13.40, 5.20, -3.60, 49.00, 1010.00),

-- Navio 6
(20, 6, 45000.00, 7.00, 15.50, 4.20, 1.20, 98.00, 2450.00),
(21, 6, 65000.00, 8.80, 14.80, 5.10, 1.50, 105.00, 2620.00),
(22, 6, 85000.00, 10.20, 14.20, 5.80, 1.80, 110.00, 2750.00),
(23, 6, 105000.00, 11.50, 13.70, 6.40, 2.00, 114.00, 2850.00),

-- Navio 7
(24, 7, 8000.00, 5.50, 8.20, 3.20, -1.50, 22.00, 340.00),
(25, 7, 12000.00, 7.00, 7.60, 4.00, -1.00, 25.00, 380.00),
(26, 7, 16000.00, 8.20, 7.10, 4.60, -0.60, 27.00, 410.00),
(27, 7, 19500.00, 9.20, 6.70, 5.10, -0.20, 28.50, 435.00);

-- -----------------------------------------------------
-- SHIP_PHOTO
-- -----------------------------------------------------
INSERT INTO ship_photo (id, id_ship, url) VALUES
(1, 1, 'imgs/msc_irina.png'),
(2, 2, 'imgs/maersk_navigator.png'),
(3, 3, 'imgs/portline_navigator.jpg'),
(4, 4, 'imgs/maersk_bulker.jpg'),
(5, 5, 'imgs/auto_atlantic.jpg'),
(6, 6, 'imgs/msc_lng_abidjan.jpg'),
(7, 7, 'imgs/cma_cgm_tagus.jpg');
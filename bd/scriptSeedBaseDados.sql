/* Seed alinhado com scriptBaseDados.sql — executar sobre esquema vazio após CREATE. */

/* ---------- Entidades base ---------- */
INSERT INTO company (id, name) VALUES (1, 'Empresa de Navegação Teste, LDA');

INSERT INTO ship_type (id, name) VALUES
    (1, 'Porta-contentores'),
    (2, 'Químico / produtos líquidos a granel');

INSERT INTO fuel_efficiency (id, name, fuel_consumption_t_per_day) VALUES
    (1, 'Consumo médio — linha contentores', 42.50),
    (2, 'Consumo médio — tanqueiro', 38.00);

INSERT INTO weather_condition (id, name) VALUES
    (1, 'Mar moderado'),
    (2, 'Bonança');

INSERT INTO tank_type (id, code, name) VALUES
    (1, 'BALLAST', 'Lastro'),
    (2, 'FUEL', 'Combustível'),
    (3, 'FW', 'Água doce'),
    (4, 'LIQUID_CARGO', 'Carga líquida');

INSERT INTO route (id, name, distance_nm, frequency_days) VALUES
    (1, 'Rotterdam — Leixões', 950.00, 15),
    (2, 'Sines — Rotterdam', 1100.00, 7),
    (3, 'Rotterdam — Sines', 2650.00, 21);

INSERT INTO port (id, name, country, latitude, longitude, max_draft, max_ship_length, tidal_restrictions, description) VALUES
    (1, 'Rotterdam', 'Países Baixos', 51.9225000, 4.4791700, 20.00, 400.00, 1, 'Porto de teste — origem'),
    (2, 'Leixões', 'Portugal', 41.1833333, -8.7000000, 16.00, 350.00, 0, 'Porto de teste — destino'),
    (3, 'Sines', 'Portugal', 37.9500000, -8.8666667, 21.00, 400.00, 0, 'Terminal de líquidos — exemplo tanqueiro'),
    (4, 'Hamburgo', 'Alemanha', 53.5419444, 9.9961111, 16.50, 400.00, 0, 'Hub Norte da Europa'),
    (5, 'Antuérpia', 'Bélgica', 51.2300000, 4.4000000, 17.50, 430.00, 0, 'Maior porto de contentores da Europa');

INSERT INTO cargo_type (id, code, name, need_container) VALUES
    (1, 'DRY_CONTAINER', 'Seca em contentor', 1),
    (2, 'REEFER', 'Reefer (temperatura controlada)', 1),
    (3, 'DANGEROUS_CONTAINER', 'ADR / IMDG em contentor', 1),
    (4, 'LIQUID_BULK', 'Líquido a granel (tanques)', 0);

INSERT INTO cargo (id, id_cargo_type, cargo_name, weight, volume, priority, imdg_class, temperature_required, quantity, unit) VALUES
    (1, 1, 'Peças automóveis — lote A', 22.50, 68.00, 1, 'N/A', NULL, 22.5000, 't'),
    (2, 1, 'Têxteis embalados', 18.20, 55.00, 2, 'N/A', NULL, 18.2000, 't'),
    (3, 1, 'Mobiliário flat-pack', 16.00, 62.00, 3, 'N/A', NULL, 800.0000, 'm3'),
    (4, 2, 'Carnes congeladas', 20.10, 65.00, 1, 'N/A', -25.00, 20.1000, 't'),
    (5, 2, 'Fruta refrigerada', 19.40, 64.00, 2, 'N/A', 2.00, 19.4000, 't'),
    (6, 2, 'Lacticínios +4 °C', 17.80, 60.00, 2, 'N/A', 4.00, 17.8000, 't'),
    (7, 3, 'Solventes orgânicos', 24.00, 66.00, 1, '3', NULL, 24.0000, 't'),
    (8, 3, 'Hipoclorito de sódio', 21.50, 60.00, 2, '8', NULL, 21.5000, 't'),
    (9, 3, 'Aerossóis UN1950', 15.00, 50.00, 3, '2.1', NULL, 12000.0000, 'un'),
    (10, 3, 'Pesticidas classe 6.1', 22.00, 62.00, 1, '6.1', NULL, 22.0000, 't'),
    (11, 4, 'CPP — parcela Rotterdam A', 8500.00, 10000.00, 1, 'N/A', NULL, 10000.0000, 'm3'),
    (12, 4, 'CPP — parcela Rotterdam B', 6400.00, 7500.00, 2, 'N/A', NULL, 7500.0000, 'm3'),
    (13, 4, 'Nafta leve', 3200.00, 4000.00, 1, '3', NULL, 4000.0000, 'm3'),
    (14, 4, 'Gasóleo marítimo MGO', 2100.00, 2500.00, 2, 'N/A', NULL, 2500.0000, 'm3'),
    (15, 4, 'Óleo base lubrificante', 1800.00, 2000.00, 3, 'N/A', NULL, 2000.0000, 'm3');

INSERT INTO route_port (id, id_route, id_port, port_order) VALUES
    (1, 1, 1, 1),
    (2, 1, 2, 2),
    (3, 2, 3, 1),
    (4, 2, 1, 2),
    (5, 3, 1, 1),
    (6, 3, 4, 2),
    (7, 3, 5, 3),
    (8, 3, 2, 4),
    (9, 3, 3, 5);

INSERT INTO port_fees (id, id_port, name, price) VALUES
    (1, 1, 'Taxa atracação', 12500.00),
    (2, 2, 'Taxa atracação', 9800.00),
    (3, 3, 'Taxa terminal líquidos', 15200.00),
    (4, 4, 'Taxa atracação', 14200.00),
    (5, 5, 'Taxa atracação', 16800.00);

INSERT INTO container_type (id, name, length, width, height, max_weight) VALUES
    (1, '40'' HC', 12.20, 2.44, 2.90, 30.48);

/* ---------- Navio 1: porta-contentores ---------- */
INSERT INTO ship (
    id, id_company, id_ship_type, id_fuel_efficiency,
    name, built_year, imo_number, gt, dwt, height, length, width, max_draft, crew_size,
    ukc_margin, max_bending_moment, max_shear_force, speed_knots, description,
    lightweight, lcg, vcg, tcg,
    gm_min_admissible, max_trim_meters, max_trim_percent_loa, max_list_angle_deg,
    default_water_density_kg_m3
) VALUES (
    1, 1, 1, 1,
    'MV Alpha Test', 2016, 'IMO9270001',
    25000.00, 42000.00, 24.50, 200.00, 32.20, 14.80, 24,
    1.20, 520000.00, 410000.00, 19.00,
    'Exemplo porta-contentores — estivagem em contentores.',
    11800.00, 0.0000, 8.2000, 0.0000,
    1.2000, 2.50, 1.500, 12.00,
    1025.00
);

INSERT INTO tank (id, id_ship, id_tank_type, name, capacity_m3, lcv, vcv, tcv) VALUES
    (1, 1, 1, 'Alpha — lastro central', 2500.0000, -5.0000, 3.2000, 0.0000),
    (2, 1, 2, 'Alpha — MGO', 1200.0000, 12.0000, 2.8000, 1.2000);

INSERT INTO tank_fill_curve (id, id_tank, level_m, volume_m3) VALUES
    (1, 1, 0.0000, 0.000), (2, 1, 2.5000, 800.000), (3, 1, 5.0000, 1800.000), (4, 1, 7.8000, 2500.000),
    (5, 2, 0.0000, 0.000), (6, 2, 1.2000, 400.000), (7, 2, 2.4000, 1200.000);

INSERT INTO tank_stability_curve (id, id_tank, volume_m3, liquid_lcg, liquid_vcg, liquid_tcg, fsm_t_m) VALUES
    (1, 1, 0.000, NULL, NULL, NULL, 0.000000),
    (2, 1, 1250.000, -5.0000, 3.1500, 0.0000, 850.000000),
    (3, 1, 2500.000, NULL, NULL, NULL, 0.000000),
    (4, 2, 0.000, NULL, NULL, NULL, 0.000000),
    (5, 2, 600.000, 12.0000, 2.8200, 1.2000, 120.000000),
    (6, 2, 1200.000, NULL, NULL, NULL, 0.000000);

INSERT INTO container (registration, id_container_type, tare_weight, gross_weight, cg_offset_v_m) VALUES
    ('MSCU1111111', 1, 3.90, 22.50, 0.0000),
    ('MSCU2222222', 1, 3.90, 18.20, 0.0000),
    ('MSCU3333333', 1, 4.10, 20.10, 0.0200),
    ('MSCU4444444', 1, 3.85, 24.00, 0.0500),
    ('MSCU5555555', 1, 3.88, 22.00, 0.0000),
    ('MSCU6666666', 1, 3.92, 21.50, 0.0300),
    ('MSCU7777777', 1, 3.80, 15.00, 0.0100);

INSERT INTO container_slot (id, id_ship, bay, row, tier, max_weight, slot_lcg, slot_vcg, slot_tcg) VALUES
    (1, 1, 12, 2, 4, 32.00, 15.5000, 18.2000, -2.4000),
    (2, 1, 12, 2, 3, 32.00, 15.5000, 15.3000, -2.4000),
    (3, 1, 14, 1, 2, 32.00, 22.0000, 12.1000, 0.0000),
    (4, 1, 14, 1, 3, 32.00, 22.0000, 15.2000, 0.0000),
    (5, 1, 14, 2, 2, 32.00, 22.0000, 12.1000, 2.4000),
    (6, 1, 16, 1, 2, 32.00, 28.0000, 12.1000, 0.0000),
    (7, 1, 16, 1, 3, 32.00, 28.0000, 15.2000, 0.0000);

INSERT INTO sailing (id, id_ship, id_route, id_weather_condition, fuel_price_per_ton, estimated_arrival_time, water_density_kg_m3) VALUES
    (1, 1, 1, 1, 685.00, '2026-05-15 08:00:00', 1025.00),
    (3, 1, 3, 1, 688.00, '2026-07-22 14:00:00', 1025.00);

INSERT INTO shipment (id, id_sailing, id_cargo) VALUES
    (1, 1, 1),
    (2, 1, 2),
    (3, 1, 4),
    (4, 1, 7),
    (5, 1, 10),
    (6, 3, 8),
    (7, 3, 9);

INSERT INTO container_storage (id, id_container_slot, container_registration, id_shipment) VALUES
    (1, 1, 'MSCU1111111', 1),
    (2, 2, 'MSCU2222222', 2),
    (3, 3, 'MSCU3333333', 3),
    (4, 4, 'MSCU4444444', 4),
    (5, 5, 'MSCU5555555', 5),
    (6, 6, 'MSCU6666666', 6),
    (7, 7, 'MSCU7777777', 7);

/* ---------- Navio 2: tanqueiro ---------- */
INSERT INTO ship (
    id, id_company, id_ship_type, id_fuel_efficiency,
    name, built_year, imo_number, gt, dwt, height, length, width, max_draft, crew_size,
    ukc_margin, max_bending_moment, max_shear_force, speed_knots, description,
    lightweight, lcg, vcg, tcg,
    gm_min_admissible, max_trim_meters, max_trim_percent_loa, max_list_angle_deg,
    default_water_density_kg_m3
) VALUES (
    2, 1, 2, 2,
    'MV Beta Tanker', 2014, 'IMO9270002',
    42000.00, 75000.00, 22.00, 228.00, 32.26, 15.20, 28,
    1.35, 680000.00, 520000.00, 14.50,
    'Exemplo tanqueiro — carga em tanques.',
    18500.00, 2.5000, 7.8000, 0.0000,
    1.0000, 3.00, 2.000, 10.00,
    1025.00
);

INSERT INTO tank (id, id_ship, id_tank_type, name, capacity_m3, lcv, vcv, tcv) VALUES
    (3, 2, 1, 'Beta — lastro 1', 4200.0000, -35.0000, 3.0000, 0.0000),
    (4, 2, 2, 'Beta — fuelóleo', 2100.0000, 18.0000, 2.6000, 0.8000),
    (5, 2, 4, 'Beta — carga líquida centro', 12000.0000, 5.0000, 4.5000, 0.0000),
    (6, 2, 4, 'Beta — carga líquida popa', 9500.0000, 45.0000, 4.2000, 0.0000),
    (7, 2, 4, 'Beta — carga líquida proa', 3500.0000, -28.0000, 4.0000, 0.0000);

INSERT INTO tank_fill_curve (id, id_tank, level_m, volume_m3) VALUES
    (8, 3, 0.0000, 0.000), (9, 3, 4.0000, 2000.000), (10, 3, 8.5000, 4200.000),
    (11, 4, 0.0000, 0.000), (12, 4, 2.0000, 1050.000), (13, 4, 4.0000, 2100.000),
    (14, 5, 0.0000, 0.000), (15, 5, 5.0000, 5000.000), (16, 5, 10.0000, 12000.000),
    (17, 6, 0.0000, 0.000), (18, 6, 4.0000, 4500.000), (19, 6, 8.1000, 9500.000),
    (32, 7, 0.0000, 0.000), (33, 7, 3.0000, 1500.000), (34, 7, 6.2000, 3500.000);

INSERT INTO tank_stability_curve (id, id_tank, volume_m3, liquid_lcg, liquid_vcg, liquid_tcg, fsm_t_m) VALUES
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
    (37, 7, 3500.000, NULL, NULL, NULL, 0.000000);

INSERT INTO sailing (id, id_ship, id_route, id_weather_condition, fuel_price_per_ton, estimated_arrival_time, water_density_kg_m3) VALUES
    (2, 2, 2, 2, 672.00, '2026-06-10 06:00:00', 1025.00),
    (4, 2, 2, 2, 670.00, '2026-08-01 06:00:00', 1025.00);

INSERT INTO shipment (id, id_sailing, id_cargo) VALUES
    (8, 2, 11),
    (9, 2, 12),
    (10, 4, 13),
    (11, 4, 14),
    (12, 4, 15);

INSERT INTO liquid_storage (id, id_shipment, id_tank, volume_m3, cargo_density_kg_m3) VALUES
    (1, 8, 5, 10000.000, 850.0000),
    (2, 9, 6, 7500.000, 853.3333),
    (3, 10, 5, 4000.000, 800.0000),
    (4, 11, 6, 2500.000, 840.0000),
    (5, 12, 7, 2000.000, 900.0000);

INSERT INTO ship_hydrostatic_curve (id, id_ship, displacement, draft, KM, KB, LCB, TPC, MCTC) VALUES
    (1, 1, 15000.00, 8.50, 12.80, 4.60, 0.50, 42.00, 850.00),
    (2, 1, 25000.00, 11.20, 11.50, 5.80, 1.20, 48.00, 920.00),
    (3, 1, 35000.00, 13.80, 10.40, 6.90, 1.80, 52.00, 980.00),
    (4, 1, 45000.00, 14.70, 9.90, 7.40, 2.10, 54.00, 1000.00),
    (5, 2, 28000.00, 9.20, 11.20, 5.10, 1.00, 55.00, 1050.00),
    (6, 2, 45000.00, 11.50, 10.10, 6.20, 1.60, 62.00, 1180.00),
    (7, 2, 62000.00, 13.40, 9.40, 7.00, 2.00, 66.00, 1250.00),
    (8, 2, 78000.00, 14.80, 8.90, 7.60, 2.30, 68.00, 1280.00);

INSERT INTO ship_photo (id, id_ship, url) VALUES
    (1, 1, 'imgs/container.jpg'),
    (2, 2, 'imgs/tank.jpg');

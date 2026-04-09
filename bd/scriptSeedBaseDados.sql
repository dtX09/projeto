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

INSERT INTO route (id, name, distance_nm, frequency_days) VALUES
    (1, 'Rotterdam — Leixões', 950.00, 15),
    (2, 'Sines — Rotterdam', 1100.00, 7),
    (3, 'Rotterdam — Sines', 2650.00, 21);

INSERT INTO port (id, name, country, latitude, longitude, max_draft, max_ship_length, tidal_restrictions, description) VALUES
    (1, 'Rotterdam', 'Países Baixos', 51.9225000, 4.4791700, 20.00, 400.00, 1, 'Porto de teste — origem'),
    (2, 'Leixões', 'Portugal', 41.1833333, -8.7000000, 16.00, 350.00, 0, 'Porto de teste — destino'),
    (3, 'Sines', 'Portugal', 37.9500000, -8.8666667, 21.00, 400.00, 0, 'Terminal de líquidos — exemplo tanqueiro'),
    (4, 'Hamburgo', 'Alemanha', 53.5419444, 9.9961111, 16.50, 400.00, 0, 'Hub Norte da Europa — exemplo rota multi-porto'),
    (5, 'Antuérpia', 'Bélgica', 51.2300000, 4.4000000, 17.50, 430.00, 0, 'Maior porto de contentores da Europa — exemplo rota multi-porto');

/* ---------- Navio 1: porta-contentores (só contentores na condição de teste) ---------- */
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
    'Exemplo porta-contentores — condição de teste sem carga líquida operacional em tanques.',
    11800.00, 0.0000, 8.2000, 0.0000,
    1.2000, 2.50, 1.500, 12.00,
    1025.00
);

/* Tanques operacionais do Alpha (lastro + combustível); não há liquid_cargo_stowage neste exemplo */
INSERT INTO tanks (id, id_ship, id_tank_type, name, capacity_m3, lcv, vcv, tcv) VALUES
    (1, 1, 1, 'Alpha — lastro central', 2500.000, -5.0000, 3.2000, 0.0000),
    (2, 1, 2, 'Alpha — MGO', 1200.000, 12.0000, 2.8000, 1.2000);

INSERT INTO tank_fill_curve (id_tank, level_m, volume_m3) VALUES
    (1, 0.0000, 0.000), (1, 2.5000, 800.000), (1, 5.0000, 1800.000), (1, 7.8000, 2500.000),
    (2, 0.0000, 0.000), (2, 1.2000, 400.000), (2, 2.4000, 1200.000);

INSERT INTO tank_stability_curve (id_tank, volume_m3, liquid_lcg, liquid_vcg, liquid_tcg, fsm_t_m) VALUES
    (1, 0.000, NULL, NULL, NULL, 0.000000),
    (1, 1250.000, -5.0000, 3.1500, 0.0000, 850.000000),
    (1, 2500.000, NULL, NULL, NULL, 0.000000),
    (2, 0.000, NULL, NULL, NULL, 0.000000),
    (2, 600.000, 12.0000, 2.8200, 1.2000, 120.000000),
    (2, 1200.000, NULL, NULL, NULL, 0.000000);

INSERT INTO container_type (id, name, length, width, height, max_weight) VALUES
    (1, '40'' HC', 12.20, 2.44, 2.90, 30.48);

INSERT INTO container (id, id_container_type, container_number, cargo_name, volume, priority, imdg_class, temperature_required, tare_weight, gross_weight, owner, status, cg_offset_v_m) VALUES
    (1, 1, 'MSCU1234567', 'Peças automóveis', 68.00, 1, 'N/A', NULL, 3.90, 22.50, 'Shipper Teste SA', 'LOADED', 0.0000),
    (2, 1, 'MSCU7654321', 'Produtos químicos embalados', 66.00, 2, '3', 18.00, 3.85, 26.20, NULL, 'LOADED', 0.0500);

INSERT INTO container_slot (id, id_ship, bay, row, tier, max_weight, slot_lcg, slot_vcg, slot_tcg) VALUES
    (1, 1, 12, 2, 4, 32.00, 15.5000, 18.2000, -2.4000),
    (2, 1, 12, 2, 3, 32.00, 15.5000, 15.3000, -2.4000),
    (3, 1, 14, 1, 2, 32.00, 22.0000, 12.1000, 0.0000);

INSERT INTO sailing (id, id_ship, id_route, id_weather_condition, fuel_price_per_ton, estimated_arrival_time) VALUES
    (1, 1, 1, 1, 685.00, '2026-05-15 08:00:00'),
    (3, 1, 3, 1, 688.00, '2026-07-22 14:00:00');

INSERT INTO cargo_shipment (id, id_sailing, id_discharge_port, cargo_name, weight, volume, priority, imdg_class, temperature_required, need_container) VALUES
    (1, 1, 2, 'Peças automóveis', 22.50, 68.00, 1, 'N/A', NULL, 1),
    (2, 1, 2, 'Químicos embalados', 26.20, 66.00, 2, '3', 18.00, 1);

INSERT INTO loading_condition (id, id_sailing, name, description, water_density_kg_m3) VALUES
    (1, 1, 'Alpha — partida (contentores)', 'Apenas estivagem em contentores; sem registos em liquid_cargo_stowage.', 1025.00);

INSERT INTO shipment_container (id_cargo_shipment, id_container) VALUES
    (1, 1),
    (2, 2);

INSERT INTO container_stowage (id_loading_condition, id_container_slot, id_container) VALUES
    (1, 1, 1),
    (1, 2, 2);

/* ---------- Navio 2: tanque (só carga em tanques; sem contentores) ---------- */
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
    'Exemplo tanqueiro — carga apenas em tanques; sem slots nem contentores.',
    18500.00, 2.5000, 7.8000, 0.0000,
    1.0000, 3.00, 2.000, 10.00,
    1025.00
);

/* tank_type: 1 BALLAST, 2 FUEL, 4 LIQUID_CARGO */
INSERT INTO tanks (id, id_ship, id_tank_type, name, capacity_m3, lcv, vcv, tcv) VALUES
    (3, 2, 1, 'Beta — lastro 1', 4200.000, -35.0000, 3.0000, 0.0000),
    (4, 2, 2, 'Beta — fuelóleo', 2100.000, 18.0000, 2.6000, 0.8000),
    (5, 2, 4, 'Beta — carga líquida centro', 12000.000, 5.0000, 4.5000, 0.0000),
    (6, 2, 4, 'Beta — carga líquida popa', 9500.000, 45.0000, 4.2000, 0.0000);

INSERT INTO tank_fill_curve (id_tank, level_m, volume_m3) VALUES
    (3, 0.0000, 0.000), (3, 4.0000, 2000.000), (3, 8.5000, 4200.000),
    (4, 0.0000, 0.000), (4, 2.0000, 1050.000), (4, 4.0000, 2100.000),
    (5, 0.0000, 0.000), (5, 5.0000, 5000.000), (5, 10.0000, 12000.000),
    (6, 0.0000, 0.000), (6, 4.0000, 4500.000), (6, 8.1000, 9500.000);

INSERT INTO tank_stability_curve (id_tank, volume_m3, liquid_lcg, liquid_vcg, liquid_tcg, fsm_t_m) VALUES
    (3, 0.000, NULL, NULL, NULL, 0.000000),
    (3, 2100.000, -35.0000, 2.9500, 0.0000, 1100.000000),
    (3, 4200.000, NULL, NULL, NULL, 0.000000),
    (4, 0.000, NULL, NULL, NULL, 0.000000),
    (4, 1050.000, 18.0000, 2.5800, 0.8000, 95.000000),
    (4, 2100.000, NULL, NULL, NULL, 0.000000),
    (5, 0.000, NULL, NULL, NULL, 0.000000),
    (5, 6000.000, 5.0000, 4.4800, 0.0000, 4200.000000),
    (5, 12000.000, NULL, NULL, NULL, 0.000000),
    (6, 0.000, NULL, NULL, NULL, 0.000000),
    (6, 4750.000, 45.0000, 4.1800, 0.0000, 3100.000000),
    (6, 9500.000, NULL, NULL, NULL, 0.000000);

INSERT INTO sailing (id, id_ship, id_route, id_weather_condition, fuel_price_per_ton, estimated_arrival_time) VALUES
    (2, 2, 2, 2, 672.00, '2026-06-10 06:00:00');

INSERT INTO cargo_shipment (id, id_sailing, id_discharge_port, cargo_name, weight, volume, priority, imdg_class, temperature_required, need_container) VALUES
    (3, 2, 1, 'CPP — crude parcela A', 8500.00, 10000.00, 1, 'N/A', NULL, 0),
    (4, 2, 1, 'CPP — crude parcela B', 6400.00, 7500.00, 2, 'N/A', NULL, 0);

INSERT INTO loading_condition (id, id_sailing, name, description, water_density_kg_m3) VALUES
    (2, 2, 'Beta — plena carga (tanques)', 'Apenas liquid_cargo_stowage; navio sem grelha de contentores.', 1025.00);

INSERT INTO liquid_cargo_stowage (id_loading_condition, id_tank, volume_m3, cargo_density_kg_m3) VALUES
    (2, 3, 2800.000, 1025.0000),
    (2, 5, 10000.000, 850.0000),
    (2, 6, 7500.000, 853.3333);

INSERT INTO route_port (id_route, id_port, port_order) VALUES
    (1, 1, 1),
    (1, 2, 2),
    (2, 3, 1),
    (2, 1, 2),
    (3, 1, 1),
    (3, 4, 2),
    (3, 5, 3),
    (3, 2, 4),
    (3, 3, 5);

INSERT INTO port_fees (id_port, name, price) VALUES
    (1, 'Taxa atracação', 12500.00),
    (2, 'Taxa atracação', 9800.00),
    (3, 'Taxa terminal líquidos', 15200.00),
    (4, 'Taxa atracação', 14200.00),
    (5, 'Taxa atracação', 16800.00);

INSERT INTO exercise_plan (id, name, description) VALUES
    (1, 'Plano A — Distribuição de contentores', 'Exercício pedagógico: equilibrar peso por baía (sem ligar a sailings).');

INSERT INTO exercise_plan_cargo (id_exercise_plan, cargo_name, weight, volume, priority, imdg_class, temperature_required) VALUES
    (1, 'Carga genérica A', 100.00, 120.00, 1, 'N/A', NULL),
    (1, 'Carga genérica B', 85.00, 95.00, 2, 'N/A', NULL);

INSERT INTO exercise_plan_port (id_exercise_plan, id_port, port_order) VALUES
    (1, 1, 1),
    (1, 2, 2);

INSERT INTO ship_hydrostatic_curve (id_ship, displacement, draft, KM, KB, LCB, TPC, MCTC) VALUES
    (1, 15000.00, 8.50, 12.80, 4.60, 0.50, 42.00, 850.00),
    (1, 25000.00, 11.20, 11.50, 5.80, 1.20, 48.00, 920.00),
    (1, 35000.00, 13.80, 10.40, 6.90, 1.80, 52.00, 980.00),
    (1, 45000.00, 14.70, 9.90, 7.40, 2.10, 54.00, 1000.00),
    (2, 28000.00, 9.20, 11.20, 5.10, 1.00, 55.00, 1050.00),
    (2, 45000.00, 11.50, 10.10, 6.20, 1.60, 62.00, 1180.00),
    (2, 62000.00, 13.40, 9.40, 7.00, 2.00, 66.00, 1250.00),
    (2, 78000.00, 14.80, 8.90, 7.60, 2.30, 68.00, 1280.00);

INSERT INTO ship_photo (id_ship, url) VALUES
    (1, 'imgs/container.jpg'),
    (2, 'imgs/tank.jpg');


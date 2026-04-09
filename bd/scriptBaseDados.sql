CREATE TABLE company (
    id BIGINT AUTO_INCREMENT PRIMARY KEY NOT NULL,
    name VARCHAR(80)
);

CREATE TABLE ship_type (
    id BIGINT AUTO_INCREMENT PRIMARY KEY NOT NULL,
    name VARCHAR(80) NOT NULL
) ;

CREATE TABLE fuel_efficiency (
    id BIGINT AUTO_INCREMENT PRIMARY KEY NOT NULL,
    name VARCHAR(80) NOT NULL,
    fuel_consumption_t_per_day DECIMAL(10,2) NOT NULL
) ;

CREATE TABLE weather_condition (
    id BIGINT AUTO_INCREMENT PRIMARY KEY NOT NULL,
    name VARCHAR(80) NOT NULL
) ;

CREATE TABLE route (
    id BIGINT AUTO_INCREMENT PRIMARY KEY NOT NULL,
    name VARCHAR(80) NOT NULL,
    distance_nm DECIMAL(10,2) NOT NULL,
    frequency_days INT NOT NULL
) ;

CREATE TABLE port (
    id BIGINT AUTO_INCREMENT PRIMARY KEY NOT NULL,
    name VARCHAR(80) NOT NULL,
    country VARCHAR(80) NOT NULL,
    latitude DECIMAL(10,7) NOT NULL,
    longitude DECIMAL(10,7) NOT NULL,
    max_draft DECIMAL(8,2) NOT NULL,
    max_ship_length DECIMAL(8,2) NOT NULL,
    tidal_restrictions BOOLEAN NOT NULL,
    description TEXT
) ;

CREATE TABLE ship (
    id BIGINT AUTO_INCREMENT PRIMARY KEY NOT NULL,
    id_company BIGINT NOT NULL,
    id_ship_type BIGINT NOT NULL,
    id_fuel_efficiency BIGINT NOT NULL,
    name VARCHAR(80) NOT NULL,
    built_year INT NOT NULL,
    imo_number VARCHAR(40) NOT NULL,
    gt DECIMAL(8,2) NOT NULL,
    dwt DECIMAL(8,2) NOT NULL,
    height DECIMAL(8,2) NOT NULL,
    length DECIMAL(8,2) NOT NULL,
    width DECIMAL(8,2) NOT NULL,
    max_draft DECIMAL(8,2) NOT NULL,
    crew_size INT,
    ukc_margin DECIMAL(8,2) NOT NULL,
    max_bending_moment DECIMAL(10,2) NOT NULL,
    max_shear_force DECIMAL(10,2) NOT NULL,
    speed_knots DECIMAL(6,2) NOT NULL,
    description VARCHAR(300),
    /* Lightweight (displacement) e centro de gravidade do navio vazio — estabilidade / distribuição de carga */
    lightweight DECIMAL(12,2) NOT NULL,
    lcg DECIMAL(10,4) NOT NULL,
    vcg DECIMAL(10,4) NOT NULL,
    tcg DECIMAL(10,4) NOT NULL,
    /* Limites operacionais */
    gm_min_admissible DECIMAL(8,4) NOT NULL,
    max_trim_meters DECIMAL(8,4),
    max_trim_percent_loa DECIMAL(6,3),
    max_list_angle_deg DECIMAL(6,2) NOT NULL,
    /* Densidade média da água do mar para conversões deslocamento ↔ calado (pode sobrepor-se por condição de carregamento) */
    default_water_density_kg_m3 DECIMAL(8,2) NOT NULL DEFAULT 1025.00,
    UNIQUE (imo_number),
    FOREIGN KEY (id_company) REFERENCES company(id),
    FOREIGN KEY (id_ship_type) REFERENCES ship_type(id),
    FOREIGN KEY (id_fuel_efficiency) REFERENCES fuel_efficiency(id)
) ;

CREATE TABLE sailing (
    id BIGINT AUTO_INCREMENT PRIMARY KEY NOT NULL,
    id_ship BIGINT NOT NULL,
    id_route BIGINT NOT NULL,
    id_weather_condition BIGINT NOT NULL,
    fuel_price_per_ton DECIMAL(8,2) NOT NULL,
    estimated_arrival_time DATETIME NOT NULL,
    FOREIGN KEY (id_ship) REFERENCES ship(id),
    FOREIGN KEY (id_route) REFERENCES route(id),
    FOREIGN KEY (id_weather_condition) REFERENCES weather_condition(id)
) ;

CREATE TABLE tank_type (
    id BIGINT AUTO_INCREMENT PRIMARY KEY NOT NULL,
    code VARCHAR(40) NOT NULL,
    name VARCHAR(80) NOT NULL,
    UNIQUE (code)
) ;

CREATE TABLE tanks (
    id BIGINT AUTO_INCREMENT PRIMARY KEY NOT NULL,
    id_ship BIGINT NOT NULL,
    id_tank_type BIGINT NOT NULL,
    name VARCHAR(80) NOT NULL,
    capacity_m3 DECIMAL(12,3) NOT NULL,
    /* Centro de volume (LCG/VCG/TCG do tanque) — referência habitual: midship / quilha / linha de água ou convencão do navio */
    lcv DECIMAL(10,4) NOT NULL,
    vcv DECIMAL(10,4) NOT NULL,
    tcv DECIMAL(10,4) NOT NULL,
    FOREIGN KEY (id_ship) REFERENCES ship(id) ON DELETE CASCADE,
    FOREIGN KEY (id_tank_type) REFERENCES tank_type(id)
) ;

/* Curva de enchimento: relação nível (sondagens) ↔ volume */
CREATE TABLE tank_fill_curve (
    id BIGINT AUTO_INCREMENT PRIMARY KEY NOT NULL,
    id_tank BIGINT NOT NULL,
    level_m DECIMAL(10,4) NOT NULL,
    volume_m3 DECIMAL(12,3) NOT NULL,
    FOREIGN KEY (id_tank) REFERENCES tanks(id) ON DELETE CASCADE
) ;

/*
 * Por volume de líquido no tanque: CG da massa líquida (parcialmente cheio ≠ centro geométrico do tanque)
 * e momento de superfície livre FSM (t·m) para GM corrigido. Se liquid_* NULL, usar tanks.lcv/vcv/tcv.
 */
CREATE TABLE tank_stability_curve (
    id BIGINT AUTO_INCREMENT PRIMARY KEY NOT NULL,
    id_tank BIGINT NOT NULL,
    volume_m3 DECIMAL(12,3) NOT NULL,
    liquid_lcg DECIMAL(10,4),
    liquid_vcg DECIMAL(10,4),
    liquid_tcg DECIMAL(10,4),
    fsm_t_m DECIMAL(14,6) NOT NULL DEFAULT 0,
    UNIQUE (id_tank, volume_m3),
    FOREIGN KEY (id_tank) REFERENCES tanks(id) ON DELETE CASCADE
) ;

CREATE TABLE container_type (
    id BIGINT AUTO_INCREMENT PRIMARY KEY NOT NULL,
    name VARCHAR(80) NOT NULL,
    length DECIMAL(8,2) NOT NULL,
    width DECIMAL(8,2) NOT NULL,
    height DECIMAL(8,2) NOT NULL,
    max_weight DECIMAL(8,2) NOT NULL
) ;

CREATE TABLE container (
    id BIGINT AUTO_INCREMENT PRIMARY KEY NOT NULL,
    id_container_type BIGINT NOT NULL,
    container_number VARCHAR(80),
    cargo_name VARCHAR(150) NOT NULL,
    volume DECIMAL(10,2) NOT NULL,
    priority INT NOT NULL,
    imdg_class VARCHAR(30) NOT NULL,
    temperature_required DECIMAL(6,2),
    tare_weight DECIMAL(10,2) NOT NULL,
    gross_weight DECIMAL(10,2) NOT NULL,
    owner VARCHAR(120),
    status VARCHAR(40) NOT NULL,
    /* Desvio vertical do CG da carga+contentor em relação ao CG geométrico do slot (+ para cima) */
    cg_offset_v_m DECIMAL(8,4) NOT NULL DEFAULT 0,
    UNIQUE (container_number),
    FOREIGN KEY (id_container_type) REFERENCES container_type(id),
    CONSTRAINT chk_container_gross_ge_tare CHECK (gross_weight >= tare_weight)
) ;

CREATE TABLE container_slot (
    id BIGINT AUTO_INCREMENT PRIMARY KEY NOT NULL,
    id_ship BIGINT NOT NULL,
    bay INT NOT NULL,
    row INT NOT NULL,
    tier INT NOT NULL,
    max_weight DECIMAL(8,2) NOT NULL,
    /* Centro geométrico do slot no referencial do navio (mesma convenção que ship.lcg/vcg/tcg) — para momentos e KG */
    slot_lcg DECIMAL(10,4) NOT NULL,
    slot_vcg DECIMAL(10,4) NOT NULL,
    slot_tcg DECIMAL(10,4) NOT NULL,
    FOREIGN KEY (id_ship) REFERENCES ship(id)
) ;

CREATE TABLE cargo_shipment (
    id BIGINT AUTO_INCREMENT PRIMARY KEY NOT NULL,
    id_sailing BIGINT NOT NULL,
    id_discharge_port BIGINT NOT NULL,
    cargo_name VARCHAR(150) NOT NULL,
    weight DECIMAL(8,2) NOT NULL,
    volume DECIMAL(8,2) NOT NULL,
    priority INT NOT NULL,
    imdg_class VARCHAR(30) NOT NULL,
    temperature_required DECIMAL(6,2),
    need_container BOOLEAN NOT NULL,
    FOREIGN KEY (id_sailing) REFERENCES sailing(id),
    FOREIGN KEY (id_discharge_port) REFERENCES port(id)
) ;

CREATE TABLE route_port (
    id BIGINT AUTO_INCREMENT PRIMARY KEY NOT NULL,
    id_route BIGINT NOT NULL,
    id_port BIGINT NOT NULL,
    port_order INT NOT NULL,
    UNIQUE (id_route, port_order),
    FOREIGN KEY (id_route) REFERENCES route(id),
    FOREIGN KEY (id_port) REFERENCES port(id)
) ;

CREATE TABLE port_fees (
    id BIGINT AUTO_INCREMENT PRIMARY KEY NOT NULL,
    id_port BIGINT NOT NULL,
    name VARCHAR(80) NOT NULL,
    price DECIMAL(7,2) NOT NULL,
    FOREIGN KEY (id_port) REFERENCES port(id)
) ;

CREATE TABLE exercise_plan (
    id BIGINT AUTO_INCREMENT PRIMARY KEY NOT NULL,
    name VARCHAR(255),
    description TEXT
) ;

CREATE TABLE exercise_plan_cargo (
    id BIGINT AUTO_INCREMENT PRIMARY KEY NOT NULL,
    id_exercise_plan BIGINT NOT NULL,
    cargo_name VARCHAR(150) NOT NULL,
    weight DECIMAL(8,2) NOT NULL,
    volume DECIMAL(8,2) NOT NULL,
    priority INT NOT NULL,
    imdg_class VARCHAR(30) NOT NULL,
    temperature_required DECIMAL(6,2),
    FOREIGN KEY (id_exercise_plan) REFERENCES exercise_plan(id)
) ;

CREATE TABLE exercise_plan_port (
    id BIGINT AUTO_INCREMENT PRIMARY KEY NOT NULL,
    id_exercise_plan BIGINT NOT NULL,
    id_port BIGINT NOT NULL,
    port_order INT NOT NULL,
    UNIQUE (id_port, port_order, id_exercise_plan),
    FOREIGN KEY (id_exercise_plan) REFERENCES exercise_plan(id),
    FOREIGN KEY (id_port) REFERENCES port(id)
) ;

/* Condição de carregamento: estivagem real ligada à viagem (sailing). exercise_plan é só uso pedagógico, sem FK para aqui. */
CREATE TABLE loading_condition (
    id BIGINT AUTO_INCREMENT PRIMARY KEY NOT NULL,
    id_sailing BIGINT NOT NULL,
    name VARCHAR(120) NOT NULL,
    description VARCHAR(500),
    /* Massa específica da água exterior para hidrostática nesta condição (água salgada típ. 1025 kg/m³) */
    water_density_kg_m3 DECIMAL(8,2) NOT NULL DEFAULT 1025.00,
    FOREIGN KEY (id_sailing) REFERENCES sailing(id) ON DELETE CASCADE
) ;

CREATE TABLE shipment_container (
    id BIGINT AUTO_INCREMENT PRIMARY KEY NOT NULL,
    id_cargo_shipment BIGINT NOT NULL,
    id_container BIGINT NOT NULL,
    UNIQUE (id_container, id_cargo_shipment),
    FOREIGN KEY (id_cargo_shipment) REFERENCES cargo_shipment(id),
    FOREIGN KEY (id_container) REFERENCES container(id)
) ;

/* Ocupação de um slot por um contentor numa condição de carregamento */
CREATE TABLE container_stowage (
    id BIGINT AUTO_INCREMENT PRIMARY KEY NOT NULL,
    id_loading_condition BIGINT NOT NULL,
    id_container_slot BIGINT NOT NULL,
    id_container BIGINT NOT NULL,
    UNIQUE (id_loading_condition, id_container_slot),
    UNIQUE (id_loading_condition, id_container),
    FOREIGN KEY (id_loading_condition) REFERENCES loading_condition(id) ON DELETE CASCADE,
    FOREIGN KEY (id_container_slot) REFERENCES container_slot(id),
    FOREIGN KEY (id_container) REFERENCES container(id)
) ;

/* Ligação tanque ↔ condição de carregamento (carga líquida a bordo) */
CREATE TABLE liquid_cargo_stowage (
    id BIGINT AUTO_INCREMENT PRIMARY KEY NOT NULL,
    id_loading_condition BIGINT NOT NULL,
    id_tank BIGINT NOT NULL,
    volume_m3 DECIMAL(12,3) NOT NULL,
    /* Massa = volume_m3 * cargo_density_kg_m3 / 1000 (toneladas métricas) */
    cargo_density_kg_m3 DECIMAL(10,4) NOT NULL,
    UNIQUE (id_loading_condition, id_tank),
    FOREIGN KEY (id_loading_condition) REFERENCES loading_condition(id) ON DELETE CASCADE,
    FOREIGN KEY (id_tank) REFERENCES tanks(id) ON DELETE CASCADE
) ;

CREATE TABLE ship_hydrostatic_curve (
    id BIGINT AUTO_INCREMENT PRIMARY KEY NOT NULL,
    id_ship BIGINT NOT NULL,
    displacement DECIMAL(10,2) NOT NULL,
    draft DECIMAL(10,2) NOT NULL,
    KM DECIMAL(10,2) NOT NULL,
    KB DECIMAL(10,2) NOT NULL,
    LCB DECIMAL(10,2) NOT NULL,
    TPC DECIMAL(10,2) NOT NULL,
    MCTC DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (id_ship) REFERENCES ship(id)
) ;

CREATE TABLE ship_photo (
    id BIGINT AUTO_INCREMENT PRIMARY KEY NOT NULL,
    id_ship BIGINT NOT NULL,
    url TEXT NOT NULL,
    FOREIGN KEY (id_ship) REFERENCES ship(id)
) ;

/* Dados iniciais para tank_type */
INSERT INTO tank_type (code, name) VALUES
    ('BALLAST', 'Lastro'),
    ('FUEL', 'Combustível'),
    ('FRESH_WATER', 'Água doce'),
    ('LIQUID_CARGO', 'Carga líquida'),
    ('LUB_OIL', 'Óleo lubrificante'),
    ('WASTE', 'Resíduos / águas sujas');

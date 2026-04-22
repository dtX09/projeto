CREATE TABLE cargo (
    id BIGINT NOT NULL,
    cargo_name VARCHAR(150) NOT NULL,
    weight DECIMAL(8,2) NOT NULL,
    volume DECIMAL(8,2) NOT NULL,
    priority INT NOT NULL,
    imdg_class VARCHAR(30) NOT NULL,
    temperature_required DECIMAL(6,2),
    quantity DECIMAL(10,4) NOT NULL,
    unit VARCHAR(40) NOT NULL,
    need_container BOOLEAN NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE company (
    id BIGINT NOT NULL,
    name VARCHAR(80),
    PRIMARY KEY (id)
);

CREATE TABLE container_type (
    id BIGINT NOT NULL,
    name VARCHAR(80) NOT NULL,
    length DECIMAL(8,2) NOT NULL,
    width DECIMAL(8,2) NOT NULL,
    height DECIMAL(8,2) NOT NULL,
    max_weight DECIMAL(8,2) NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE container (
    registration VARCHAR(250) NOT NULL,
    id_container_type BIGINT NOT NULL,
    tare_weight DECIMAL(10,2) NOT NULL,
    gross_weight DECIMAL(10,2) NOT NULL,
    /* Desvio vertical do CG da carga+contentor face ao CG geométrico do slot (+ para cima) */
    cg_offset_v_m DECIMAL(8,4) NOT NULL DEFAULT 0,
    PRIMARY KEY (registration),
    FOREIGN KEY (id_container_type) REFERENCES container_type(id),
    CONSTRAINT chk_container_gross_ge_tare CHECK (gross_weight >= tare_weight)
);

CREATE TABLE ship_type (
    id BIGINT NOT NULL,
    name VARCHAR(80) NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE fuel_efficiency (
    id BIGINT NOT NULL,
    name VARCHAR(80) NOT NULL,
    fuel_consumption_t_per_day DECIMAL(10,2) NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE ship (
    id BIGINT NOT NULL,
    id_company BIGINT NOT NULL,
    id_ship_type BIGINT NOT NULL,
    id_fuel_efficiency BIGINT NOT NULL,
    name VARCHAR(80) NOT NULL,
    built_year INT NOT NULL,
    imo_number VARCHAR(40) NOT NULL UNIQUE,
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
    /* Navio leve e CG — base para KG / momentos */
    lightweight DECIMAL(12,2) NOT NULL,
    lcg DECIMAL(10,4) NOT NULL,
    vcg DECIMAL(10,4) NOT NULL,
    tcg DECIMAL(10,4) NOT NULL,
    gm_min_admissible DECIMAL(8,4) NOT NULL,
    max_trim_meters DECIMAL(8,4),
    max_trim_percent_loa DECIMAL(6,3),
    max_list_angle_deg DECIMAL(6,2) NOT NULL,
    default_water_density_kg_m3 DECIMAL(8,2) NOT NULL DEFAULT 1025.00,
    PRIMARY KEY (id),
    FOREIGN KEY (id_company) REFERENCES company(id),
    FOREIGN KEY (id_ship_type) REFERENCES ship_type(id),
    FOREIGN KEY (id_fuel_efficiency) REFERENCES fuel_efficiency(id)
);

CREATE TABLE container_slot (
    id BIGINT NOT NULL,
    id_ship BIGINT NOT NULL,
    bay INT NOT NULL,
    row INT NOT NULL,
    tier INT NOT NULL,
    max_weight DECIMAL(28,2) NOT NULL,
    slot_lcg DECIMAL(10,4) NOT NULL,
    slot_vcg DECIMAL(10,4) NOT NULL,
    slot_tcg DECIMAL(10,4) NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (id_ship) REFERENCES ship(id)
);

CREATE TABLE route (
    id BIGINT NOT NULL,
    name VARCHAR(80) NOT NULL,
    distance_nm DECIMAL(10,2) NOT NULL,
    frequency_days INT,
    PRIMARY KEY (id)
);

CREATE TABLE weather_condition (
    id BIGINT NOT NULL,
    name VARCHAR(80) NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE sailing (
    id BIGINT NOT NULL,
    id_ship BIGINT NOT NULL,
    id_route BIGINT NOT NULL,
    id_weather_condition BIGINT NOT NULL,
    fuel_price_per_ton DECIMAL(8,2) NOT NULL,
    estimated_arrival_time DATETIME NOT NULL,
    /* Água exterior para hidrostática nesta viagem (sobrepor default do navio na aplicação, se quiseres) */
    water_density_kg_m3 DECIMAL(8,2) NOT NULL DEFAULT 1025.00,
    PRIMARY KEY (id),
    FOREIGN KEY (id_ship) REFERENCES ship(id),
    FOREIGN KEY (id_route) REFERENCES route(id),
    FOREIGN KEY (id_weather_condition) REFERENCES weather_condition(id)
);

CREATE TABLE shipment (
    id BIGINT NOT NULL,
    id_sailing BIGINT NOT NULL,
    id_cargo BIGINT NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (id_sailing) REFERENCES sailing(id),
    FOREIGN KEY (id_cargo) REFERENCES cargo(id)
);

CREATE TABLE container_storage (
    id BIGINT NOT NULL,
    id_container_slot BIGINT NOT NULL,
    container_registration VARCHAR(250) NOT NULL,
    id_shipment BIGINT NOT NULL,
    PRIMARY KEY (id),
    UNIQUE (id_shipment, id_container_slot),
    UNIQUE (id_shipment, container_registration),
    FOREIGN KEY (id_container_slot) REFERENCES container_slot(id),
    FOREIGN KEY (container_registration) REFERENCES container(registration),
    FOREIGN KEY (id_shipment) REFERENCES shipment(id)
);

CREATE TABLE port (
    id BIGINT NOT NULL,
    name VARCHAR(80) NOT NULL,
    country VARCHAR(80) NOT NULL,
    latitude DECIMAL(10,7) NOT NULL,
    longitude DECIMAL(10,7) NOT NULL,
    max_draft DECIMAL(8,2) NOT NULL,
    max_ship_length DECIMAL(8,2) NOT NULL,
    tidal_restrictions BOOLEAN NOT NULL,
    description TEXT,
    PRIMARY KEY (id)
);

CREATE TABLE route_port (
    id BIGINT NOT NULL,
    id_route BIGINT NOT NULL,
    id_port BIGINT NOT NULL,
    port_order INT NOT NULL,
    PRIMARY KEY (id),
    UNIQUE (id_route, port_order),
    FOREIGN KEY (id_route) REFERENCES route(id),
    FOREIGN KEY (id_port) REFERENCES port(id)
);

CREATE TABLE port_fees (
    id BIGINT NOT NULL,
    id_port BIGINT NOT NULL,
    name VARCHAR(80) NOT NULL,
    price DECIMAL(7,2) NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (id_port) REFERENCES port(id)
);

CREATE TABLE tank_type (
    id BIGINT NOT NULL,
    code VARCHAR(80) NOT NULL UNIQUE,
    name VARCHAR(100) NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE tank (
    id BIGINT NOT NULL,
    id_ship BIGINT NOT NULL,
    id_tank_type BIGINT NOT NULL,
    name VARCHAR(150) NOT NULL,
    capacity_m3 DECIMAL(10,4) NOT NULL,
    lcv DECIMAL(10,4) NOT NULL,
    vcv DECIMAL(10,4) NOT NULL,
    tcv DECIMAL(10,4) NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (id_ship) REFERENCES ship(id) ON DELETE CASCADE,
    FOREIGN KEY (id_tank_type) REFERENCES tank_type(id)
);

/* Curva nível (sondagens) ↔ volume */
CREATE TABLE tank_fill_curve (
    id BIGINT NOT NULL,
    id_tank BIGINT NOT NULL,
    level_m DECIMAL(10,4) NOT NULL,
    volume_m3 DECIMAL(12,3) NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (id_tank) REFERENCES tank(id) ON DELETE CASCADE
);

/*
 * Por volume no tanque: CG da massa líquida e FSM (t·m) para GM corrigido.
 * Se liquid_* NULL, usar tank.lcv/vcv/tcv na aplicação.
 */
CREATE TABLE tank_stability_curve (
    id BIGINT NOT NULL,
    id_tank BIGINT NOT NULL,
    volume_m3 DECIMAL(12,3) NOT NULL,
    liquid_lcg DECIMAL(10,4),
    liquid_vcg DECIMAL(10,4),
    liquid_tcg DECIMAL(10,4),
    fsm_t_m DECIMAL(14,6) NOT NULL DEFAULT 0,
    PRIMARY KEY (id),
    UNIQUE (id_tank, volume_m3),
    FOREIGN KEY (id_tank) REFERENCES tank(id) ON DELETE CASCADE
);

CREATE TABLE liquid_storage (
    id BIGINT NOT NULL,
    id_shipment BIGINT NOT NULL,
    id_tank BIGINT NOT NULL,
    volume_m3 DECIMAL(12,3) NOT NULL,
    /* Massa (t) = volume_m3 * cargo_density_kg_m3 / 1000 */
    cargo_density_kg_m3 DECIMAL(10,4) NOT NULL,
    PRIMARY KEY (id),
    UNIQUE (id_shipment, id_tank),
    FOREIGN KEY (id_shipment) REFERENCES shipment(id),
    FOREIGN KEY (id_tank) REFERENCES tank(id)
);

CREATE TABLE ship_hydrostatic_curve (
    id BIGINT NOT NULL,
    id_ship BIGINT NOT NULL,
    displacement DECIMAL(10,2) NOT NULL,
    draft DECIMAL(10,2) NOT NULL,
    KM DECIMAL(10,2) NOT NULL,
    KB DECIMAL(10,2) NOT NULL,
    LCB DECIMAL(10,2) NOT NULL,
    TPC DECIMAL(10,2) NOT NULL,
    MCTC DECIMAL(10,2) NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (id_ship) REFERENCES ship(id)
);

CREATE TABLE ship_photo (
    id BIGINT NOT NULL,
    id_ship BIGINT NOT NULL,
    url TEXT NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (id_ship) REFERENCES ship(id)
);
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
    distance_nm DECIMAL(10,2) NOT NULL
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

CREATE TABLE ballast_tanks (
    id BIGINT AUTO_INCREMENT PRIMARY KEY NOT NULL,
    id_ship BIGINT NOT NULL,
    name VARCHAR(40) NOT NULL,
    capacity DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (id_ship) REFERENCES ship(id) ON DELETE CASCADE
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
    registration VARCHAR(250) NOT NULL,
    id_container_type BIGINT NOT NULL,
    PRIMARY KEY (registration),
    FOREIGN KEY (id_container_type) REFERENCES container_type(id)
) ;

CREATE TABLE container_slot (
    id BIGINT AUTO_INCREMENT PRIMARY KEY NOT NULL,
    id_ship BIGINT NOT NULL,
    bay INT NOT NULL,
    row INT NOT NULL,
    tier INT NOT NULL,
    max_weight DECIMAL(8,2) NOT NULL,
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

CREATE TABLE shipment_container (
    id BIGINT AUTO_INCREMENT PRIMARY KEY NOT NULL,
    id_cargo_shipment BIGINT NOT NULL,
    container_registration VARCHAR(250) NOT NULL,
    UNIQUE (container_registration, id_cargo_shipment),
    FOREIGN KEY (id_cargo_shipment) REFERENCES cargo_shipment(id),
    FOREIGN KEY (container_registration) REFERENCES container(registration)
) ;

CREATE TABLE container_storage (
    id BIGINT AUTO_INCREMENT PRIMARY KEY NOT NULL,
    id_shipment_container BIGINT NOT NULL,
    id_container_slot BIGINT NOT NULL,
    FOREIGN KEY (id_shipment_container) REFERENCES shipment_container(id),
    FOREIGN KEY (id_container_slot) REFERENCES container_slot(id)
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
-- Таблица корпоративных подписок
CREATE TABLE IF NOT EXISTS corporate_subscriptions (
    subscription_id SERIAL PRIMARY KEY,
    payment_timestamp TIMESTAMP,
    renewal_timestamp TIMESTAMP,
    subscription_cost DECIMAL(10,2),
    private_key TEXT
);

-- Таблица компаний
CREATE TABLE IF NOT EXISTS companies (
    company_id SERIAL PRIMARY KEY,
    subscription_id INT REFERENCES corporate_subscriptions(subscription_id),
    company_name VARCHAR(255),
    is_active BOOLEAN
);

-- Таблица связки компании с корпоративными доменами почты
CREATE TABLE IF NOT EXISTS company_email_domains (
    record_id SERIAL PRIMARY KEY,
    company_id INT REFERENCES companies(company_id),
    email_domain VARCHAR(255),
    is_active BOOLEAN
);

-- Таблица ролей
CREATE TABLE IF NOT EXISTS roles (
    role_id SERIAL PRIMARY KEY,
    role_name VARCHAR(255),
    role_level INT
);

-- Таблица пользователей
CREATE TABLE IF NOT EXISTS users (
    user_id SERIAL PRIMARY KEY,
    role_id INT REFERENCES roles(role_id),
    country_iso_code CHAR(2),
    encrypted_password TEXT,
    created_timestamp TIMESTAMP,
    email VARCHAR(255) UNIQUE,
    is_active BOOLEAN,
    phone_number VARCHAR(20)
);

-- Таблица персональных тарифов
CREATE TABLE IF NOT EXISTS personal_tariffs (
    tariff_id SERIAL PRIMARY KEY,
    max_requests INT,
    tariff_rate DECIMAL(10,2)
);

-- Таблица типов пользователей (корпоративные и индивидуальные)
CREATE TABLE IF NOT EXISTS corporate_users (
    user_id INT PRIMARY KEY REFERENCES users(user_id),
    company_id INT REFERENCES companies(company_id)
);

CREATE TABLE IF NOT EXISTS individual_users (
    user_id INT PRIMARY KEY REFERENCES users(user_id),
    tariff_id INT REFERENCES personal_tariffs(tariff_id)
);

-- Таблица регионов
CREATE TABLE IF NOT EXISTS regions (
    country_iso_code CHAR(2) PRIMARY KEY,
    access_status BOOLEAN
);



-- Таблица контекста запросов
CREATE TABLE IF NOT EXISTS contexts (
    context_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(user_id),
    start_timestamp TIMESTAMP,
    end_timestamp TIMESTAMP
);


-- Таблица запросов к ИИ
CREATE TABLE IF NOT EXISTS ai_requests (
    request_id SERIAL PRIMARY KEY,
    context_id INT REFERENCES contexts(context_id),
    request_text TEXT,
    request_timestamp TIMESTAMP
);


-- Таблица моделей ИИ
CREATE TABLE IF NOT EXISTS ai_models (
    model_id SERIAL PRIMARY KEY,
    api_address VARCHAR(255)
);


-- Таблица ответов ИИ
CREATE TABLE IF NOT EXISTS ai_responses (
    response_id SERIAL PRIMARY KEY,
    request_id INT REFERENCES ai_requests(request_id),
    model_id INT REFERENCES ai_models(model_id),
    response_text TEXT,
    response_timestamp TIMESTAMP
);


-- Таблица связки тарифов и моделей ИИ
CREATE TABLE IF NOT EXISTS tariff_model_mapping (
    mapping_id SERIAL PRIMARY KEY,
    tariff_id INT REFERENCES personal_tariffs(tariff_id),
    model_id INT REFERENCES ai_models(model_id),
    token_price DECIMAL(10,5)
);

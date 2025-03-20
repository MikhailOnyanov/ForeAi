-- Наполнение тестовыми данными

-- Роли
INSERT INTO roles (role_name, role_level) VALUES ('Администратор', 1), ('Пользователь', 2);

-- Пользователи
INSERT INTO users (role_id, country_iso_code, encrypted_password, created_timestamp, email, is_active, phone_number)
VALUES (1, 'RU', 'password123', NOW(), 'admin@example.com', TRUE, '+79999999999'),
       (2, 'US', 'password456', NOW(), 'user@example.com', TRUE, '+18888888888');

-- Компании
INSERT INTO companies (subscription_id, company_name, is_active) VALUES (NULL, 'Tech Corp', TRUE), (NULL, 'Innovate Ltd', TRUE);

-- Корпоративные пользователи
INSERT INTO corporate_users (user_id, company_id) VALUES (1, 1);

-- Персональные тарифы
INSERT INTO personal_tariffs (max_requests, tariff_rate) VALUES (1000, 9.99), (5000, 49.99);

-- Индивидуальные пользователи
INSERT INTO individual_users (user_id, tariff_id) VALUES (2, 1);

-- Регион
INSERT INTO regions (country_iso_code, access_status) VALUES ('RU', TRUE), ('US', TRUE);

-- Модели ИИ
INSERT INTO ai_models (api_address) VALUES ('https://api.model1.com'), ('https://api.model2.com');

-- Контексты
INSERT INTO contexts (user_id, start_timestamp, end_timestamp) VALUES (1, NOW(), NOW() + INTERVAL '1 hour');

-- Запросы к ИИ
INSERT INTO ai_requests (context_id, request_text, request_timestamp) VALUES (1, 'Как погода?', NOW());

-- Ответы ИИ
INSERT INTO ai_responses (request_id, model_id, response_text, response_timestamp) VALUES (1, 1, 'Сегодня солнечно.', NOW());

-- Связка тарифов и моделей
INSERT INTO tariff_model_mapping (tariff_id, model_id, token_price) VALUES (1, 1, 0.01), (2, 2, 0.005);

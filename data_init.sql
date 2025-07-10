INSERT INTO public.role(
	id, name, description, created_at, updated_at)
	VALUES (9999, 'ADMIN', 'ALL Permission', NOW(), NOW());

INSERT INTO public."user"(
	id, username, password, email_text, first_name, last_name, created_at, updated_at)
	VALUES (9999, 'testAdmin101', '123', 'Testadmin@test.com', 'TEST', 'Admin', NOW(), NOW());

INSERT INTO public.user_role(
	user_id, role_id, created_at, updated_at)
	VALUES (9999, 9999, NOW(),NOW());

INSERT INTO public.hardware(
	id, name, type, manufacturer, model, location, status, purchase_date, created_at, updated_at)
	VALUES
	(9999, 'Linux','Server', 'Linux', 'ABC123', 'UK', 'Valid' , '2022-05-01 00:00:00', NOW(), NOW()),
	(9998, 'Window','Server', 'Microsoft', 'Win123', 'HK', 'Valid' , '2022-10-01 00:00:00', NOW(), NOW());

INSERT INTO public.software(
	id, name, version, vendor, hardware_id, status, installation_date, licence_expiry_date, created_at, updated_at)
	VALUES
	(9999, 'Solarwinds', '1.0.1', 'Solarwinds', 9999, 'Active', '2022-05-01 00:00:00', '2026-05-01 00:00:00',  NOW(), NOW()),
	(9998, 'Pycharm', '2024.1.1', 'JetBrains', 9999, 'Active', '2022-05-01 00:00:00', '2025-06-28 00:00:00',  NOW(), NOW());

INSERT INTO public.vulnerability(
	cve_id, published_date, last_modified_date, description, severity, cvss_score, vendor, product, version)
	VALUES ('A_2025_19', NOW(), NOW(), 'Example created', 'CRITICAL', 1.01, 'JetBrains', 'Pycharm', '2024.1.1');
-- name: cars
-- 1. Список автомобилей (SELECT, ORDER BY).
SELECT id, name FROM cars ORDER BY name, id;

-- name: fuels
-- 2. Список видов топлива (SELECT, ORDER BY).
SELECT id, name FROM fuels ORDER BY name, id;

-- name: car_detail
-- 3. Автомобиль и его необязательный расход (WHERE, LEFT JOIN).
SELECT c.id, c.name, x.liters_per_100km
FROM cars AS c
LEFT JOIN consumptions AS x ON x.car_id = c.id
WHERE c.id = ?;

-- name: refuelings
-- 4. Заправки с названиями автомобиля и топлива (JOIN).
SELECT r.*, c.name AS car_name, f.name AS fuel_name,
       r.fuel_liters * r.price_per_liter AS cost
FROM refuelings AS r
JOIN cars AS c ON c.id = r.car_id
JOIN fuels AS f ON f.id = r.fuel_id
ORDER BY r.id DESC;

-- name: refueling_detail
-- 5. Полная информация о выбранной заправке (JOIN, WHERE).
SELECT r.*, c.name AS car_name, f.name AS fuel_name,
       r.fuel_liters * r.price_per_liter AS cost
FROM refuelings AS r
JOIN cars AS c ON c.id = r.car_id
JOIN fuels AS f ON f.id = r.fuel_id
WHERE r.id = ?;

-- name: search
-- 6. Поиск по автомобилю, топливу и минимальному объёму (WHERE, AND).
-- Параметры: car_id дважды, fuel_id дважды, min_liters.
SELECT r.*, c.name AS car_name, f.name AS fuel_name,
       r.fuel_liters * r.price_per_liter AS cost
FROM refuelings AS r
JOIN cars AS c ON c.id = r.car_id
JOIN fuels AS f ON f.id = r.fuel_id
WHERE (? IS NULL OR r.car_id = ?)
  AND (? IS NULL OR r.fuel_id = ?)
  AND r.fuel_liters >= ?
ORDER BY cost DESC, r.id;

-- name: without_refuelings
-- 7. Автомобили без заправок (NOT EXISTS).
SELECT c.id, c.name FROM cars AS c
WHERE NOT EXISTS (SELECT 1 FROM refuelings AS r WHERE r.car_id = c.id)
ORDER BY c.name, c.id;

-- name: totals
-- 8. Количество, сумма, средняя, минимальная и максимальная стоимость.
SELECT COUNT(*) AS count,
       COALESCE(SUM(fuel_liters * price_per_liter), 0) AS total_cost,
       COALESCE(SUM(fuel_liters), 0) AS total_liters,
       AVG(fuel_liters * price_per_liter) AS average_cost,
       MIN(fuel_liters * price_per_liter) AS min_cost,
       MAX(fuel_liters * price_per_liter) AS max_cost
FROM refuelings;

-- name: consumption_totals
-- 9. Количество автомобилей с нормой расхода и средний расход.
SELECT COUNT(*) AS count, AVG(liters_per_100km) AS average_consumption
FROM consumptions;

-- name: by_car
-- 10. Статистика по всем автомобилям, включая автомобили без заправок.
SELECT c.id, c.name, COUNT(r.id) AS count,
       COALESCE(SUM(r.fuel_liters * r.price_per_liter), 0) AS total_cost
FROM cars AS c
LEFT JOIN refuelings AS r ON r.car_id = c.id
GROUP BY c.id, c.name
ORDER BY total_cost DESC, c.id;

-- name: by_fuel
-- 11. Статистика по видам топлива (GROUP BY).
SELECT f.id, f.name, COUNT(r.id) AS count,
       COALESCE(SUM(r.fuel_liters), 0) AS total_liters
FROM fuels AS f
LEFT JOIN refuelings AS r ON r.fuel_id = f.id
GROUP BY f.id, f.name
ORDER BY total_liters DESC, f.id;

-- name: frequent_cars
-- 12. Автомобили с количеством заправок больше порога (HAVING).
SELECT c.id, c.name, COUNT(r.id) AS count
FROM cars AS c
JOIN refuelings AS r ON r.car_id = c.id
GROUP BY c.id, c.name
HAVING COUNT(r.id) > ?
ORDER BY count DESC, c.id;

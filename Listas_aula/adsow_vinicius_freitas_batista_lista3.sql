USE sakila;

-- 1. Clientes com locações em aberto
SELECT DISTINCT c.first_name, c.last_name, c.email
FROM customer c
JOIN rental r ON c.customer_id = r.customer_id
WHERE r.return_date IS NULL;

-- 2. Cliente e quantidade de filmes alugados
SELECT c.first_name, c.last_name, COUNT(r.rental_id) AS qtd_locacoes
FROM customer c
JOIN rental r ON c.customer_id = r.customer_id
GROUP BY c.customer_id
ORDER BY qtd_locacoes DESC;

-- 3. Cliente e valor total gasto
SELECT c.first_name, c.last_name, SUM(p.amount) AS total_gasto
FROM customer c
JOIN payment p ON c.customer_id = p.customer_id
GROUP BY c.customer_id
ORDER BY total_gasto DESC;

-- 4. Quantidade de filmes (itens) por loja
SELECT s.store_id, COUNT(i.inventory_id) AS total_itens
FROM store s
JOIN inventory i ON s.store_id = i.store_id
GROUP BY s.store_id;

-- 5. Valor recebido por loja
SELECT s.store_id, SUM(p.amount) AS receita_total
FROM payment p
JOIN staff st ON p.staff_id = st.staff_id
JOIN store s ON st.store_id = s.store_id
GROUP BY s.store_id;

-- 6. Quantidade de clientes ativos por loja
SELECT store_id, COUNT(customer_id) AS clientes_ativos
FROM customer
WHERE active = 1
GROUP BY store_id;

-- 7. Filmes fora de catálogo
SELECT title FROM film 
WHERE film_id NOT IN (SELECT DISTINCT film_id FROM inventory);

-- 8. Filme e quantidade de vezes alugado
SELECT f.title, COUNT(r.rental_id) AS vezes_alugado
FROM film f
JOIN inventory i ON f.film_id = i.film_id
JOIN rental r ON i.inventory_id = r.inventory_id
GROUP BY f.film_id
ORDER BY vezes_alugado DESC;

-- 9. Filme e valor total arrecadado
SELECT f.title, SUM(p.amount) AS total_arrecadado
FROM film f
JOIN inventory i ON f.film_id = i.film_id
JOIN rental r ON i.inventory_id = r.inventory_id
JOIN payment p ON r.rental_id = p.rental_id
GROUP BY f.film_id
ORDER BY total_arrecadado DESC;

-- 10. Ator e quantidade de filmes
SELECT a.first_name, a.last_name, COUNT(fa.film_id) AS qtd_filmes
FROM actor a
JOIN film_actor fa ON a.actor_id = fa.actor_id
GROUP BY a.actor_id
ORDER BY qtd_filmes DESC;

-- 11. Filmes que nunca foram alugados
SELECT f.title
FROM film f
LEFT JOIN inventory i ON f.film_id = i.film_id
LEFT JOIN rental r ON i.inventory_id = r.inventory_id
WHERE r.rental_id IS NULL;

-- 12. Clientes e filmes com locação em aberto
SELECT c.first_name, f.title, r.rental_date
FROM rental r
JOIN customer c ON r.customer_id = c.customer_id
JOIN inventory i ON r.inventory_id = i.inventory_id
JOIN film f ON i.film_id = f.film_id
WHERE r.return_date IS NULL;

-- 13. Multa para locações em aberto (R$ 0.10/dia de atraso)
SELECT 
    c.first_name, f.title, r.rental_date,
    DATEDIFF(CURRENT_DATE(), r.rental_date) AS dias_com_filme,
    IF(DATEDIFF(CURRENT_DATE(), r.rental_date) > f.rental_duration, 
       (DATEDIFF(CURRENT_DATE(), r.rental_date) - f.rental_duration) * 0.10, 
       0) AS multa_estimada
FROM rental r
JOIN inventory i ON r.inventory_id = i.inventory_id
JOIN film f ON i.film_id = f.film_id
JOIN customer c ON r.customer_id = c.customer_id
WHERE r.return_date IS NULL;

-- 14. Top 10 filmes mais alugados
SELECT f.title, COUNT(r.rental_id) AS total
FROM film f
JOIN inventory i ON f.film_id = i.film_id
JOIN rental r ON i.inventory_id = r.inventory_id
GROUP BY f.film_id
ORDER BY total DESC
LIMIT 10;

-- 15. Sazonalidade: mês, dia da semana e quantidade de aluguéis
SELECT MONTH(rental_date) mes, DAYNAME(rental_date) dia, COUNT(*) qtd
FROM rental
GROUP BY MONTH(rental_date), DAYNAME(rental_date)
ORDER BY mes, qtd DESC;

-- 16. Dashboard da loja (total, abertos, receita, pendente)
SELECT 
    s.store_id,
    COUNT(r.rental_id) AS total_locacoes,
    SUM(IF(r.return_date IS NULL, 1, 0)) AS locacoes_aberto,
    SUM(p.amount) AS receita_realizada,
    SUM(IF(r.return_date IS NULL AND DATEDIFF(CURRENT_DATE(), r.rental_date) > f.rental_duration, 
           (DATEDIFF(CURRENT_DATE(), r.rental_date) - f.rental_duration) * 0.10, 0)) AS receita_pendente_multa
FROM store s
JOIN inventory i ON s.store_id = i.store_id
JOIN film f ON i.film_id = f.film_id
LEFT JOIN rental r ON i.inventory_id = r.inventory_id
LEFT JOIN payment p ON r.rental_id = p.rental_id
GROUP BY s.store_id;

-- 17. Histórico do cliente
SELECT c.first_name, f.title, s.store_id, p.amount
FROM rental r
JOIN customer c ON r.customer_id = c.customer_id
JOIN inventory i ON r.inventory_id = i.inventory_id
JOIN film f ON i.film_id = f.film_id
JOIN store s ON i.store_id = s.store_id
LEFT JOIN payment p ON r.rental_id = p.rental_id
ORDER BY c.customer_id, r.rental_date DESC;

-- 18. Dias totais que cada cópia ficou alugada
SELECT f.title, i.inventory_id, SUM(DATEDIFF(r.return_date, r.rental_date)) AS dias_alugado
FROM rental r
JOIN inventory i ON r.inventory_id = i.inventory_id
JOIN film f ON i.film_id = f.film_id
WHERE r.return_date IS NOT NULL
GROUP BY i.inventory_id, f.title;

-- 19. Quantidade de aluguéis por mês/ano
SELECT YEAR(rental_date) ano, MONTH(rental_date) mes, COUNT(*) total
FROM rental
GROUP BY YEAR(rental_date), MONTH(rental_date);

-- 20. Faturamento por mês/ano
SELECT YEAR(payment_date) ano, MONTH(payment_date) mes, SUM(amount) total
FROM payment
GROUP BY YEAR(payment_date), MONTH(payment_date);

-- 21. Quantidade de locações de cada filme por mês
SELECT YEAR(r.rental_date) ano, MONTH(r.rental_date) mes, f.title, COUNT(*) qtd
FROM rental r
JOIN inventory i ON r.inventory_id = i.inventory_id
JOIN film f ON i.film_id = f.film_id
GROUP BY YEAR(r.rental_date), MONTH(r.rental_date), f.title
ORDER BY ano, mes, qtd DESC;

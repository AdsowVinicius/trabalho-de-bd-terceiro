-- 1
SELECT name, lifeexpectancy FROM country WHERE lifeexpectancy > 70;

-- 2
SELECT language, countrycode FROM countrylanguage;

-- 3
SELECT country.name, countrylanguage.language
FROM country
INNER JOIN countrylanguage ON country.code = countrylanguage.countrycode
WHERE countrylanguage.isofficial = 'T';

-- 4
SELECT name, surfacearea FROM country ORDER BY surfacearea DESC;

-- 5
SELECT name, governmentform FROM country WHERE governmentform LIKE '%monarchy%';

-- 6
SELECT name, indepyear FROM country WHERE indepyear IS NULL;

-- 7
SELECT region, name, population FROM country WHERE population < 200000;

-- 8
SELECT name, district, population FROM city WHERE population > 10000000;

-- 9
SELECT name, continent FROM country WHERE indepyear IS NOT NULL;

-- 10
SELECT CASE WHEN continent LIKE '%America%' THEN 'America' ELSE continent END AS continente
FROM country
GROUP BY continente;

-- 11
SELECT region, COUNT(*) AS qtd_paises FROM country GROUP BY region;

-- 12
SELECT country.continent, COUNT(city.id) AS qtd_cidades
FROM country
INNER JOIN city ON country.code = city.countrycode
GROUP BY country.continent;

-- 13
SELECT continent, AVG(lifeexpectancy) AS media_expectativa FROM country GROUP BY continent;

-- 14
SELECT country.name, countrylanguage.language,
    ROUND(country.population * (countrylanguage.percentage / 100)) AS total_falantes
FROM country
INNER JOIN countrylanguage ON country.code = countrylanguage.countrycode;

-- 15
SELECT region, AVG(gnp) AS media_gnp FROM country GROUP BY region;

-- 16
SELECT language, COUNT(*) AS num_paises
FROM countrylanguage
WHERE language = 'Spanish' AND isofficial = 'T'
GROUP BY language;

-- 17
SELECT country.continent, countrylanguage.language,
    SUM(country.population * (countrylanguage.percentage / 100)) AS falantes
FROM country
INNER JOIN countrylanguage ON country.code = countrylanguage.countrycode
WHERE countrylanguage.language = 'Portuguese'
GROUP BY country.continent, countrylanguage.language;

-- 18
SELECT country.governmentform, COUNT(city.id) AS qtd_cidades
FROM country
INNER JOIN city ON country.code = city.countrycode
WHERE country.governmentform LIKE '%monarchy%'
GROUP BY country.governmentform;

-- 19
SELECT country.name, COUNT(DISTINCT city.district) AS num_distritos
FROM country
INNER JOIN city ON country.code = city.countrycode
GROUP BY country.name;

-- 20
SELECT continente, name, population
FROM (
  SELECT CASE WHEN continent LIKE '%America%' THEN 'America' ELSE continent END AS continente, name, population
  FROM country
  WHERE continent LIKE '%America%'
  ORDER BY population DESC
  LIMIT 1
) AS t;

-- 21
SELECT country.name, countrylanguage.language,
    ROUND(country.population * (countrylanguage.percentage / 100)) AS falantes
FROM country
INNER JOIN countrylanguage ON country.code = countrylanguage.countrycode;

-- 22
SELECT country.name, COUNT(city.id) AS qtd_cidades
FROM country
INNER JOIN city ON country.code = city.countrycode
GROUP BY country.name;

-- 23
SELECT region, AVG(population) AS media_populacao FROM country GROUP BY region;

-- 24
SELECT language, COUNT(*) AS num_paises
FROM countrylanguage
WHERE language = 'Portuguese' AND isofficial = 'T'
GROUP BY language;

-- 25
SELECT country.name, COUNT(countrylanguage.language) AS qtd_idiomas
FROM country
INNER JOIN countrylanguage ON country.code = countrylanguage.countrycode
GROUP BY country.name;

-- 26
SELECT country.name, COUNT(DISTINCT city.district) AS qtd_distritos
FROM country
INNER JOIN city ON country.code = city.countrycode
GROUP BY country.name;

-- 27
SELECT continent, COUNT(*) AS qtd_nao_independentes
FROM country
WHERE indepyear IS NULL
GROUP BY continent;

-- 28
SELECT region, COUNT(*) AS qtd_monarquias
FROM country
WHERE governmentform LIKE '%monarchy%'
GROUP BY region;

-- 29
SELECT continent, SUM(population) AS pop_monarquia
FROM country
WHERE governmentform LIKE '%monarchy%'
GROUP BY continent;

-- 30
SELECT name, surfacearea FROM country ORDER BY surfacearea DESC LIMIT 1;

-- 31
SELECT name, surfacearea FROM country ORDER BY surfacearea ASC LIMIT 1;

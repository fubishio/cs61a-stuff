-- CS 61A Fall 2014
-- Name: Johnathan Chow
-- Login: AKH

drop table parents;
drop table dogs;

create table parents as
  select "abraham" as parent, "barack" as child union
  select "abraham"          , "clinton"         union
  select "delano"           , "herbert"         union
  select "fillmore"         , "abraham"         union
  select "fillmore"         , "delano"          union
  select "fillmore"         , "grover"          union
  select "eisenhower"       , "fillmore"        union
  select "delano"           , "jackson";

create table dogs as
  select "abraham" as name, "long" as fur, 26 as height union
  select "barack"         , "short"      , 52           union
  select "clinton"        , "long"       , 47           union
  select "delano"         , "long"       , 46           union
  select "eisenhower"     , "short"      , 35           union
  select "fillmore"       , "curly"      , 32           union
  select "grover"         , "short"      , 28           union
  select "herbert"        , "curly"      , 31           union
  select "jackson"        , "long"       , 43;

-- All triples of dogs with the same fur that have increasing heights

select a.name, b.name, c.name from dogs as a, dogs as b, dogs as c 
where a.name != b.name and 
b.name != c.name and
a.name != c.name and
a.fur = b.fur and 
b.fur = c.fur and 
a.height < b.height and 
b.height < c.height;

-- Expected output:
--   abraham|delano|clinton
--   abraham|jackson|clinton
--   abraham|jackson|delano
--   grover|eisenhower|barack
--   jackson|delano|clinton

-- The sum of the heights of at least 3 dogs with the same fur, ordered by sum


with 
sums(currentfur, total, n, max) as (
      select fur, height, 1, height from dogs union
      select fur, total+height, n+1, height from dogs, sums
      where n<4 and fur=currentfur and max<height
)
select currentfur, total from sums where n>=3 order by total


-- Expected output:
--   long|115
--   short|115
--   long|116
--   long|119
--   long|136
--   long|162

-- The terms of g(n) where g(n) = g(n-1) + 2*g(n-2) + 3*g(n-3) and g(n) = n if n <= 3

with g(one, two, three) as 
	(select 1, 2, 3 union 
	 select two, three, three+2*two+3*one 
	 from g where one < 4000000)
   		select one from g;
 

-- Expected output:
--   1
--   2
--   3
--   10
--   22
--   51
--   125
--   293
--   696
--   1657
--   ...
--   9426875

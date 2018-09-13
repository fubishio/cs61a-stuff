-- CS 61A Fall 2014
-- Name: Johnathan Chow
-- Login: AKH

create table parents as
  select "abraham" as parent, "barack" as child union
  select "abraham"          , "clinton"         union
  select "delano"           , "herbert"         union
  select "fillmore"         , "abraham"         union
  select "fillmore"         , "delano"          union
  select "fillmore"         , "grover"          union
  select "eisenhower"       , "fillmore";

create table dogs as
  select "abraham" as name, "long" as fur, 26 as height union
  select "barack"         , "short"      , 52           union
  select "clinton"        , "long"       , 47           union
  select "delano"         , "long"       , 46           union
  select "eisenhower"     , "short"      , 35           union
  select "fillmore"       , "curly"      , 32           union
  select "grover"         , "short"      , 28           union
  select "herbert"        , "curly"      , 31;

create table sizes as
  select "toy" as size, 24 as min, 28 as max union
  select "mini",        28,        35        union
  select "medium",      35,        45        union
  select "standard",    45,        60;

-------------------------------------------------------------
-- PLEASE DO NOT CHANGE ANY SQL STATEMENTS ABOVE THIS LINE --
-------------------------------------------------------------
create table dogsize as
  select name, size from dogs as d, sizes as s where d.height <= max and d.height > min;

-- The names of all "toy" and "mini" dogs
select name from dogsize where size = "toy" or size = "mini";
-- Expected output:
--   abraham
--   eisenhower
--   fillmore
--   grover
--   herbert

-- All dogs with parents ordered by decreasing height of their parent
select child from parents, dogs where parent = name order by -height;
-- Expected output:
--   herbert
--   fillmore
--   abraham
--   delano
--   grover
--   barack
--   clinton

-- Sentences about siblings that are the same size
select "REPLACE THIS LINE WITH YOUR SOLUTION";
-- Expected output:
--   barack and clinton are standard siblings
--   abraham and grover are toy siblings

-- Ways to stack 4 dogs to a height of at least 170, ordered by total height
select a.name||", "||b.name||", "||c.name||", "||d.name||"|"||(a.height + b.height + c.height + d.height) from dogs as a, dogs as b, dogs as c, dogs as d 
where 

a.height < b.height and
b.height < c.height and 
c.height < d.height and
(a.height + b.height + c.height + d.height) >= 170
order by (a.height + b.height + c.height + d.height);
-- Expected output:
--   abraham, delano, clinton, barack|171
--   grover, delano, clinton, barack|173
--   herbert, delano, clinton, barack|176
--   fillmore, delano, clinton, barack|177
--   eisenhower, delano, clinton, barack|180

-- All non-parent relations ordered by height difference
select "REPLACE THIS LINE WITH YOUR SOLUTION";
-- Expected output:
--   fillmore|barack
--   eisenhower|barack
--   fillmore|clinton
--   eisenhower|clinton
--   eisenhower|delano
--   abraham|eisenhower
--   grover|eisenhower
--   herbert|eisenhower
--   herbert|fillmore
--   fillmore|herbert
--   eisenhower|herbert
--   eisenhower|grover
--   eisenhower|abraham
--   delano|eisenhower
--   clinton|eisenhower
--   clinton|fillmore
--   barack|eisenhower
--   barack|fillmore



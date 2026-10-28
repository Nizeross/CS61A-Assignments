CREATE TABLE parents AS
  SELECT "ace" AS parent, "bella" AS child UNION
  SELECT "ace"          , "charlie"        UNION
  SELECT "daisy"        , "hank"           UNION
  SELECT "finn"         , "ace"            UNION
  SELECT "finn"         , "daisy"          UNION
  SELECT "finn"         , "ginger"         UNION
  SELECT "ellie"        , "finn";

CREATE TABLE dogs AS
  SELECT "ace" AS name, "long" AS fur, 26 AS height UNION
  SELECT "bella"      , "short"      , 52           UNION
  SELECT "charlie"    , "long"       , 47           UNION
  SELECT "daisy"      , "long"       , 46           UNION
  SELECT "ellie"      , "short"      , 35           UNION
  SELECT "finn"       , "curly"      , 32           UNION
  SELECT "ginger"     , "short"      , 28           UNION
  SELECT "hank"       , "curly"      , 31;

CREATE TABLE sizes AS
  SELECT "toy" AS size, 24 AS min, 28 AS max UNION
  SELECT "mini"       , 28       , 35        UNION
  SELECT "medium"     , 35       , 45        UNION
  SELECT "standard"   , 45       , 60;


-- 所有有父母记录的狗，按其父母的身高降序排列
CREATE TABLE by_parent_height AS
  SELECT "REPLACE THIS LINE WITH YOUR SOLUTION";


-- 每只狗的体型分类
CREATE TABLE size_of_dogs AS
  SELECT "REPLACE THIS LINE WITH YOUR SOLUTION";


-- 【可选】建议填写此辅助表
CREATE TABLE siblings AS
  SELECT "REPLACE THIS LINE WITH YOUR SOLUTION";

-- 描述体型相同的兄弟姐妹的句子
CREATE TABLE sentences AS
  SELECT "REPLACE THIS LINE WITH YOUR SOLUTION";


-- 对于所有身高与平均身高的偏差均不超过 30% 的毛发类型，求其身高范围
CREATE TABLE low_variance AS
  SELECT "REPLACE THIS LINE WITH YOUR SOLUTION";


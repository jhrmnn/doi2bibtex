alter table abbrvs add column type integer check (type in (0, 1, 2, 3));
update abbrvs set type = 0 where full not like "%-" and full not like "-%";
update abbrvs set type = 1, full = rtrim(full, "-") || "%", abbr = rtrim(abbr, "-")
    where full like "%-" and full not like "-%";
update abbrvs set type = 2, full = "%" || ltrim(full, "-"), abbr = ltrim(abbr, "-")
    where full not like "%-" and full like "-%";
update abbrvs set type = 3, full = "%" || trim(full, "-") || "%", abbr = trim(abbr, "-")
    where full like "-%-";
vacuum;

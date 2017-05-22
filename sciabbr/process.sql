/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */
alter table abbrvs add column type integer check (type in (0, 1, 2, 3));
update abbrvs set type = 0 where full not like "%-" and full not like "-%";
update abbrvs set type = 1, full = rtrim(full, "-") || "%", abbr = rtrim(abbr, "-")
    where full like "%-" and full not like "-%";
update abbrvs set type = 2, full = "%" || ltrim(full, "-"), abbr = ltrim(abbr, "-")
    where full not like "%-" and full like "-%";
update abbrvs set type = 3, full = "%" || trim(full, "-") || "%", abbr = trim(abbr, "-")
    where full like "-%-";
vacuum;

Data described in

Seierstad, C., & Opsahl, T. (2011). For the few not the many? The effects of affirmative action on presence, prominence, and social capital of women directors in Norway. Scandinavian journal of management, 27(1), 44-54.


downloaded from http://www.boardsandgender.com/data.php on 29 June 2020


data-companies.txt and data_people.txt simply downloaded with wget,
but the 224 net?m_*.txt files were downloaded with:

for i in `grep -o "data/net[12]m/net[12]m_20[0-9][0-9]-[0-9][0-9]-[0-9][0-9][.]txt" view-source_www.boardsandgender.com_data.php.html`; do wget http://www.boardsandgender.com/${i}; done

(could not use recursive wget as forbidden, so parsed URLs out of page and used wget one by one).

ADS
Mon, Jun 29, 2020 11:34:13 AM

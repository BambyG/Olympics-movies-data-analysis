# Olympics-movies-data-analysis


The analysis below is based on the [IMDB 5000 Movie Dataset](https://www.kaggle.com/deepmatrix/imdb-5000-movie-dataset)
and the [ Olympics Sports and Medals from 1896 to 2014](https://www.kaggle.com/the-guardian/olympic-games"). 

I have used Python programming language, Pygal for data visualization and SQLite as a database engine. 

Please note that more than 35000 medals have been won since the beginning of the games. The Olympics Games dataset has a row per athlete, when a team wins a medal this dataset will count 4 medals (rows) for the 4x100 meter relay gold medal winner.

To have figures closed to what we find online I created a unique medals table grouping my initial table by medal, category_id, event, country_code and gender.

The final page is available here: https://bambyg-sql.herokuapp.com/


## 数据文件：

数据来自于网站 grouplens 中公开的数据，网站链接为 [https://grouplens.org/datasets/movielens/](https://grouplens.org/datasets/movielens/)

在网站中选取 MovieLens 20M数据集，此数据集包含2000万个评分，46.5万个标签，13.8万用户，2.7万部电影


## ratings.csv

等级评定文件。每一行表示一个用户对一个电影的评级，共4个字段，分别为：

- userId：用户 id 
- movieId：电影 id
- rating：评级范围，以半星为单位(0.5星- 5.0星)
- timestamp ：时间戳


## tags.csv

标签数据文件。每一行表示一个用户对一个电影的标签，共4个字段，分别为：

- userId：用户 id 
- movieId：电影 id
- tag：单词或短语
- timestamp ：时间戳

## movies.csv

电影数据文件。每一行都表示一部电影的信息，共3个字段，分别为：

- movieId：电影ID
- title：标题，括号内为发行年份
- genres：流派，从以下选择，以管道分隔符分开

`（Action，Adventure，Animation，Children's，Comedy，Crime，Documentary，Drama，Fantasy，Film-Noir，Horror，Musical，Mystery，Romance，Sci-Fi，Thriller，War，Western，(no genres listed)）`


## links.csv

链接数据文件。每一行都代表一部电影，共3个字段，分别为：

- movieId： 电影推荐系统MovieLens  https://movielens.org/movies/1
- imdbId：互联网电影资料库  http://www.imdb.com/title/tt0114709/
- tmdbId： 电影数据库  https://www.themoviedb.org/movie/862


## 字段概览

```
ratings.csv
userId,movieId,rating,timestamp

tags.csv
userId,movieId,tag,timestamp

movies.csv
movieId,title,genres

links.csv
movieId,imdbId,tmdbId
```
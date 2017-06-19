from flask import Flask
from datetime import datetime
from flask import render_template
import matplotlib.pyplot as plt
from pygal.style import BlueStyle
import pygal
from pygal.style import Style
import sqlite3
from pygal.maps.world import World
from pygal.style import Style




app = Flask(__name__, static_url_path='/static')

#import sys
#sys.path.append(''/usr/local/Cellar/python/2.7.13/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages'')

@app.route('/')
def hello(name=None):
	conn = sqlite3.connect('/Users/ograndberry/Documents/FrauenLoop/SQL/databases/Project_frauenloop2017')

	c = conn.cursor()

#first graph
	
	movie_title =[]
	revenue= []
	budget=[]
	profit = []


	for row in c.execute("Select movie_title, gross, budget,(gross-budget) as profit from movies where gross!='' and budget!='' order by profit desc limit 10;"):
		movie_title.append(row[0])
		revenue.append(float(row[1]))
		budget.append(float(row[2]))
		profit.append(float(row[3]))

		
	box= pygal.Bar(x_label_rotation=30)
	box.title = ' What are the most profitable movies?'
	box.x_labels = movie_title
	box.add('Revenue', revenue)
	box.add('Budget', budget)
	box.add('Profit', profit)

	box.value_formatter = lambda y: "${:,}".format(y)
	box.render_to_file('static/profitability.svg')



#second graph
	year, score_c, score_b= [],[],[]
	for row in c.execute("Select colorvsScoreBlack.year, colorvsScoreBlack.color, colorvsScoreBlack.Score_b, colorvsScoreColor.Color, colorvsScoreColor.Score_c from colorvsScoreBlack left join colorvsScoreColor on colorvsScoreBlack.Year=colorvsScoreColor.Year where colorvsScoreColor.Color is not null order by colorvsscoreblack.year desc limit 20;"):
		year.append(float(row[0]))
		score_c.append(float(row[4]))
		score_b.append(float(row[2]))

	lines = pygal.Line(x_label_rotation=70)
	lines.title = "Does the color of a movie impact its Imdb score?"
	lines.x_labels = year
	lines.add('Color',score_c) 
	lines.add('Black and White',score_b)

	lines.render_to_file('static/colorandscoreimpact.svg', format="svg")

#third graph

	x_values = []
	y_values = []


	for row in c.execute('Select duration, movie_facebook_likes from movies where duration !="";'):
	    print(row)
	    x_values.append(float(row[0]))
	    y_values.append(float(row[1]))

	both=list(zip(x_values,y_values))


	xy_chart = pygal.XY(stroke=False,x_title='Duration in minutes', y_title='Facebook Likes')
	xy_chart.title = 'What the impact of the Imdb score on the movie facebook likes?'
	xy_chart.add('Movies', both)
	xy_chart.render_to_file('static/facebookanddur.svg', format="svg")


#fourth graph


	actor_name =[]
	revenue= []


	for row in c.execute("Select distinct actor_name, sum(gross) from actors left join movies on actors.movie_id=movies.id group by actor_name order by sum(gross) desc limit 10 ;"):
		actor_name.append(row[0])
		revenue.append(float(row[1]))

	deux = list (zip(actor_name,revenue))
		
	line = pygal.HorizontalBar(x_label_rotation=30)
	line.title = 'What are the actors playing in movies with the higest revenue?'

	for r in deux:
		line.add(r[0], r[1])

	line.value_formatter = lambda y: "${:,}".format(y)

	line.render_to_file('static/actorsandrevenuefrommovies.svg')


#5 graph

	ge= []
	revenue=[]



	for row in c.execute("Select distinct movies_2.genres, sum(movies.gross)as mm from movies_2 left join movies on movies.id = movies_2.id group by movies_2.genres order by mm desc limit 10;"):
		ge.append(row[0])
		revenue.append(float(row[1]))

	both=list(zip(ge,revenue))

	total_revenue = sum(revenue)

	pie_chart = pygal.Pie()
	pie_chart.title = 'What are the genres generating the highest revenues?'

	for r in both: 
		pie_chart.add(r[0], [{'value': round(((r[1]/total_revenue)*100)), 'label': str(r[1])}])

	pie_chart.value_formatter = lambda x:  '%s%%' % x 


	
	pie_chart.render_to_file('static/genresandrevenuefrommovie.svg')




#6

	gen= []
	im=[]

	for row in c.execute("Select distinct movies_2.genres, avg(movies.imdb_score) from movies_2 left join movies on movies.id = movies_2.id group by movies_2.genres order by avg(movies.imdb_score) desc limit 10;"):
		gen.append(row[0])
		im.append(float(row[1]))

	bol=list(zip(gen,im))

	pibb = pygal.HorizontalBar()
	pibb.title = 'What are the genres generating the highest imdb score?'

	for r in bol:
		pibb.add(r[0], [{'value': r[1], 'label': r[0]}])


	pibb.render_to_file('static/genresandscorefrommovie.svg')





#7
	year= []
	medals_men = []
	medals_women = []

	for row in c.execute("Select t1.yearmen, t1.Medals_men, t2.Medals_female from (Select distinct games.year as yearmen, count(medal) as Medals_men from unique_medals left join categories on categories.id= unique_medals.category_id left join games on games.id = categories.games_id left join countries on countries.id = games.countries_id left join athletes on unique_medals.athlete_id= athletes.id where athletes.gender='Men' group by games.year) t1  left join (Select distinct games.year as yearwomen, count(medal) as Medals_female from unique_medals left join categories on categories.id= unique_medals.category_id left join games on games.id = categories.games_id left join countries on countries.id = games.countries_id left join athletes on unique_medals.athlete_id= athletes.id where athletes.gender='Women' group by games.year) t2 on t1.yearmen = t2.yearwomen  order by yearmen;"):
		year.append(row[0])
		medals_men.append(row[1])
		medals_women.append(row[2])


	line_chart = pygal.Bar(x_label_rotation=30)
	line_chart.title = "How did the victory by gender evolve with time? "
	line_chart.x_labels = year
	line_chart.add('Men', medals_men)
	line_chart.add('Women', medals_women)

	line_chart.render_to_file('static/yearandgenrechange.svg')  




#8 graph 
	medals_summer_men = []
	medals_winter_men = []
	medals_summer_women = []
	medals_winter_women = []



	for row in c.execute("Select distinct count(medal), unique_medals.gender, type from unique_medals left join athletes on athletes.id= unique_medals.athlete_id left join Categories on categories.ID = unique_medals.category_id left join games on games.ID = categories.games_id where country_code!= '' group by unique_medals.Gender, type order by count(medal)desc;"):
		
		if row[1] == "Men" and row[2]=='summer':
			medals_summer_men.append(float(row[0]))

		elif row[1] == "Men" and row[2]=='winter':
			medals_winter_men.append(float(row[0]))
		elif row[1] == "Women" and row[2]=='summer':
			medals_summer_women.append(float(row[0]))
		else:
			medals_winter_women.append(float(row[0]))


	total_summer = sum(medals_summer_women+medals_summer_men)
	total_winter = sum(medals_winter_women+ medals_winter_men)


	gauge = pygal.SolidGauge(inner_radius=0.70)
	percent_formatter = lambda x: '{:.10g}%'.format(x)
	dollar_formatter = lambda x: '{:.10g}$'.format(x)
	gauge.value_formatter = percent_formatter

	men_win_summer = round(((medals_summer_men[0]/total_summer)*100))
	women_win_summer = round(((medals_summer_women[0]/total_summer)*100))

	men_win_winter = round(((medals_winter_men[0]/total_winter)*100))
	women_win_winter = round(((medals_winter_women[0]/total_winter)*100))

	gauge.add('Women summer', [{'value': women_win_summer, 'max_value': 100}])
	gauge.add('Men summer', [{'value': men_win_summer, 'max_value': 100}])
	gauge.title = "What is the Gender split by type of game?"

	gauge.add('Women winter', [{'value': women_win_winter, 'max_value': 100}])
	gauge.add('Men winter', [{'value': men_win_winter, 'max_value': 100}])

	gauge.render_to_file("static/worldglobalgendersplit.svg")

#9

	medals= []
	sport=[]
	athlete = []
	country = []

	for row in c.execute("Select athlete_id, category_id, medals,sport,cc, athlete from (Select athlete_id, medals,sport,athlete,cc, category_id, max(medals) as maximum from (Select athlete_id,count(medal) as medals, category_id, Sport, athletes.athlete,sumandwin.Country_code as cc from sumandwin left join athletes on sumandwin.athlete_id=athletes.id group by athletes.id, sport) group by sport) where medals = maximum order by medals desc limit 10 ;"):
		medals.append(float(row[2]))
		sport.append(row[3])
		athlete.append(row[5])
		country.append(row[4])


	bol=list(zip(sport,medals,athlete,country))

	record = pygal.HorizontalBar()
	record.title = 'What are the best athletes by Sport?'

	for r in bol:
		record.add(r[0], [{'value': r[1], 'label': r[2]}])


	record.render_to_file('static/bestplayyersbysport.svg')

#10

#Create empty lists 


	sport =[]
	country_name =[]
	country_code =[]
	medals = []
	Taekwondo=[]
	Sailing=[]
	Athletics=[]
	Tennis=[]
	Wrestling=[]
	Skiing=[]
	Skating=[]
	Boxing=[]
	Volleyball=[]
	Weightlifting=[]
	Aquatics=[]
	Curling=[]
	Football=[]
	Rowing=[]
	Cycling=[]
	Equestrian=[]
	Handball=[]
	Shooting=[]
	Luge=[]
	Hockey=[]
	Canoe=[]
	Table_Tennis=[]
	Biathlon=[]
	Kayak=[]
	Fencing= []

	#Append each sport least with the adequate countries from the database

	for row in c.execute("select medals,sport,country,alpha_2 from (Select  medals,sport,alpha_2,country, max(medals) as maximum  from  (Select count(medal) as medals,unique_medals.Sport, athletes.alpha_2, countries.country from unique_medals left join athletes on unique_medals.Athlete_id=athletes.id left join countries on countries.Code = athletes.Country_code group by alpha_2, sport) group by alpha_2) where medals = maximum and alpha_2 !=''  and country!='' ;"):
		pays=row[3].lower()
		medailles = float(row[0])
		listo= (pays,medailles)

		if row[1]== 'Taekwondo':
			Taekwondo.append(listo)	
		elif row[1]== 'Athletics':
			Athletics.append(listo)
		elif row[1]== 'Tennis':
			Tennis.append(listo)
		elif row[1]== 'Wrestling':
			Wrestling.append(listo)
		elif row[1]== 'Skiing':
			Skiing.append(listo)
		elif row[1]== 'Skating':
			Skating.append(listo)
		elif row[1]== 'Volleyball':
			Volleyball.append(listo)
		elif row[1]== 'Weightlifting':
			Weightlifting.append(listo)
		elif row[1]== 'Aquatics':
			Aquatics.append(listo)
		elif row[1]== 'Curling':
			Curling.append(listo)
		elif row[1]== 'Football':
			Football.append(listo)
		elif row[1]== 'Rowing':
			Rowing.append(listo)
		elif row[1]== 'Cycling':
			Cycling.append(listo)
		elif row[1]== 'Equestrian':
			Equestrian.append(listo)
		elif row[1]== 'Handball':
			Handball.append(listo)
		elif row[1]== 'Shooting':
			Shooting.append(listo)
		elif row[1]== 'Luge':
			Luge.append(listo)
		elif row[1]== 'Hockey':
			Hockey.append(listo)
		elif row[1]== 'Canoe':
			Canoe.append(listo)
		elif row[1]== 'Table Tennis':
			Table_Tennis.append(listo)
		elif row[1]== 'Biathlon':
			Biathlon.append(listo)
		elif row[1]== 'Kayak':
			Kayak.append(listo)
		elif row[1]== 'Fencing':
			Fencing.append(listo)
		elif row[1]== 'Sailing':
			Sailing.append(listo)
		elif row[1]== 'Wrestling':
			Wrestling.append(listo)
		else:
			sport.append(row[1])
			medals.append(float(row[0]))
			country_code.append(row[3])



	#Create a dictionnary with the countries as values and sports as keys.

	keys= ['Taekwondo', 'Sailing', 'Athletics', 'Tennis', 'Wrestling', 'Skiing', 'Skating', 'Boxing', 'Volleyball', 'Weightlifting', 'Aquatics', 'Curling'
	,'Football', 'Rowing', 'Cycling', 'Equestrian', 'Handball', 'Shooting', 'Luge', 'Hockey', 'Canoe', 'Table Tennis', 'Biathlon', 'Kayak','Fencing']

	values= [Taekwondo, Sailing, Athletics, Tennis, Wrestling, Skiing, Skating, Boxing, Volleyball, Weightlifting, Aquatics, Curling,
	Football, Rowing, Cycling, Equestrian, Handball, Shooting, Luge, Hockey, Canoe, Table_Tennis, Biathlon, Kayak, Fencing]

	dictionnary= dict(zip(keys,values))
	#create the map 

	custom_style = Style(
		colors = ("#001f3f",'#FFDBE5', "#7A4900", "#0000A6", "#63FFAC", "#B79762", "#004D43", "#8FB0FF", "#997D87",
	"#5A0007", "#809693", "#111111", "#1B4400", "#4FC601", "#3B5DFF", "#4A3B53", "#FF2F80",
	"#61615A", "#BA0900", "#6B7900", "#F012BE", "#FFAA92", "#FF90C9", "#B903AA", "#D16100"))

	worldmap_chart = pygal.maps.world.World(style= custom_style)
	worldmap_chart.title = 'In which sport each country is better at?'

	for key, values in dictionnary.items():
		worldmap_chart.add(key,values)
		

	worldmap_chart.render_to_file('static/best_country_game.svg')

#11 

	Country= []
	avg_abroad = []
	avg_home = []

	for row in c.execute("Select t1.country_code, (t2.Medals_abroad/t3.games_abroad) as avg_medals_abroad,(t1.medals_all-t2.medals_abroad)/t4.games_home as avg_medals_home from(Select distinct country_code, count(medal) as Medals_all from unique_medals left join athletes on athletes.id= unique_medals.athlete_id  left join categories on categories.id= unique_medals.category_id left join games on games.ID=categories.games_id left join countries on countries.id = games.countries_id group by country_Code) t1 left join (Select distinct country_code, count(medal) as Medals_abroad from unique_medals left join athletes on athletes.id= unique_medals.athlete_id left join categories on categories.id= unique_medals.category_id left join games on games.ID=categories.games_id left join countries on countries.id = games.countries_id where athletes.Country_code != countries.Code  group by country_Code) t2 on t1.country_code = t2.country_code left join(Select distinct Country_code, count(distinct games_ID )as Games_abroad from sumandwin left join countries on countries.country = sumandwin.country where code!=country_code group by country_code ) t3 on t2.country_code = t3.country_code left join(Select distinct Country_code, count(distinct games_ID)as Games_home from sumandwin left join countries on countries.country = sumandwin.country where code=country_code group by country_code) t4 on t3.country_code = t4.country_code where avg_medals_home is not null order by avg_medals_home desc limit 17;"):
	    Country.append(row[0])
	    avg_abroad.append(row[1])
	    avg_home.append(row[2])



	line_chart = pygal.StackedBar(x_title='Countries', y_title='Average Medals')
	line_chart.title = "Is the fact to host the games impacts a country general performance?"
	line_chart.x_labels = Country
	line_chart.add('Away Games', avg_abroad)
	line_chart.add('Home Games', avg_home)


	line_chart.render_to_file('static/hostingornot.svg')  

#12

	country =[]
	men = []
	women = []

	for row in c.execute("select t1.country_code, t1.Medals_men, t2.Medals_women from (Select distinct country_code, count(medal) as Medals_men from unique_medals left join athletes on athletes.id= unique_medals.athlete_id where  athletes.gender = 'Men' group by country_Code order by medals_men desc) t1 left join (Select distinct country_code, count(medal) as Medals_women from unique_medals left join athletes on athletes.id= unique_medals.athlete_id  where  athletes.gender = 'Women' group by country_Code order by medals_women desc) t2 on t1.country_code = t2.country_code limit 30;"):
		country.append(row[0])
		men.append(row[1])
		women.append(row[2])



	radar_chart = pygal.Radar()
	radar_chart.title = 'What is the Men and Women victory split during the games?'
	radar_chart.x_labels = country
	radar_chart.add('Medals Men', men)
	radar_chart.add('Medals Women', women)

	radar_chart.render_to_file('static/sexeandvictory.svg')
#13
 
	Country= []
	Medals_90 = []
	Movies_90 = []
	Medals_00 = []
	Movies_00 = []

	for row in c.execute("select  t1.country_code, t1.Medals, t2.Mo, t3.country_code, t3.medals,t4.movies from (Select distinct country_Code , count(medal) as Medals from unique_medals left join categories on categories.id= unique_medals.category_id left join games on games.id = categories.games_id left join countries on countries.id = games.countries_id left join athletes on unique_medals.athlete_id= athletes.id where games.year between 1990 and 1999 group by country_code) t1  left join (Select distinct code, count(movies.id) as Mo from movies left join countries on countries.country=movies.country where title_year between 1990 and 1999 group by code) t2 on t1.country_code = t2.code left join (Select distinct country_Code , count(medal) as Medals from unique_medals left join categories on categories.id= unique_medals.category_id left join games on games.id = categories.games_id left join countries on countries.id = games.countries_id left join athletes on unique_medals.athlete_id= athletes.id where games.year between 2000 and 2009 group by athletes.country_code) t3 on t2.code = t3.country_code left join (Select distinct code, count(movies.id) as Movies from movies left join countries on countries.country=movies.country where title_year between 2000 and 2009 group by code) t4 on t3.country_code = t4.code where mo is not null and movies is not null;"):
	    Country.append(row[0])
	    Medals_90.append(row[1])
	    Movies_90.append(row[2])
	    Medals_00.append(row[4])
	    Movies_00.append(row[5])


	dot_chart = pygal.Box()
	dot_chart.title = 'How the 90s and 00s are different in terms of medals and movies?'
	dot_chart.add('Medals in 90s',  Medals_90)
	dot_chart.add('Movies in 90s', Movies_90)
	dot_chart.add('Medals in 00s', Medals_00)
	dot_chart.add('Movies in 00s', Movies_00)

	dot_chart.render_to_file('static/00contre90.svg')  



	return render_template('hello.html', name=name)

if __name__ == "__main__":
    app.run()
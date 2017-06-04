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
	box.title = ' Top 10 most profitable movies'
	box.x_labels = movie_title
	box.add('Revenue', revenue)
	box.add('Budget', budget)
	box.add('Profit', profit)

	box.value_formatter = lambda y: "${:,}".format(y)
	box.render_to_file('static/budgetvsrevenue1.svg')



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

	lines.render_to_file('static/colorORblack7.svg', format="svg")

#third graph

	x_values = []
	y_values = []


	for row in c.execute('Select duration, movie_facebook_likes from movies where duration !="";'):
	    print(row)
	    x_values.append(float(row[0]))
	    y_values.append(float(row[1]))

	both=list(zip(x_values,y_values))


	xy_chart = pygal.XY(stroke=False,x_title='Duration in minutes', y_title='Facebook Likes')
	xy_chart.title = 'Duration vs Facebook Likes'
	xy_chart.add('Movies', both)
	xy_chart.render_to_file('static/facebook_duration5.svg', format="svg")


#fourth graph


	actor_name =[]
	revenue= []


	for row in c.execute("Select distinct actor_name, sum(gross) from actors left join movies on actors.movie_id=movies.id group by actor_name order by sum(gross) desc limit 10 ;"):
		actor_name.append(row[0])
		revenue.append(float(row[1]))

	deux = list (zip(actor_name,revenue))
		
	line = pygal.HorizontalBar(x_label_rotation=30)
	line.title = 'Top 10 actors playing in movies with the higest revenue'

	for r in deux:
		line.add(r[0], r[1])

	line.value_formatter = lambda y: "${:,}".format(y)

	line.render_to_file('static/top10actors1.svg')


#5 graph

	ge= []
	revenue=[]



	for row in c.execute("Select distinct movies_2.genres, sum(movies.gross) from movies_2 left join movies on movies.id = movies_2.id group by movies_2.genres order by movies_2.genres desc LIMIT 10;"):
		ge.append(row[0])
		revenue.append(float(row[1]))

	both=list(zip(ge,revenue))

	total_revenue = sum(revenue)

	pie_chart = pygal.Pie()
	pie_chart.title = 'Genres by Revenue'

	for r in both: 
		pie_chart.add(r[0], [{'value': round(((r[1]/total_revenue)*100)), 'label': str(r[1])}])

	pie_chart.value_formatter = lambda x:  '%s%%' % x 


	
	pie_chart.render_to_file('static/geandre2.svg')




#6

	gen= []
	im=[]

	for row in c.execute("Select distinct movies_2.genres, avg(movies.imdb_score)  from movies_2 left join movies on movies.id = movies_2.id group by movies_2.genres order by movies_2.genres desc LIMIT 10;"):
		gen.append(row[0])
		im.append(float(row[1]))

	bol=list(zip(gen,im))

	pibb = pygal.HorizontalBar()
	pibb.title = 'Genres by Imdb Score'

	for r in bol:
		pibb.add(r[0], [{'value': r[1], 'label': r[0]}])


	pibb.render_to_file('static/genresVSimdbscore1.svg')





#7
	year= []
	medals_men = []
	medals_women = []

	for row in c.execute("Select t1.yearmen, t1.Medals_men, t2.Medals_female from (Select distinct games.year as yearmen, count(medal) as Medals_men from unique_medals left join categories on categories.id= unique_medals.category_id left join games on games.id = categories.games_id left join countries on countries.id = games.countries_id left join athletes on unique_medals.athlete_id= athletes.id where athletes.gender='Men' group by games.year) t1  left join (Select distinct games.year as yearwomen, count(medal) as Medals_female from unique_medals left join categories on categories.id= unique_medals.category_id left join games on games.id = categories.games_id left join countries on countries.id = games.countries_id left join athletes on unique_medals.athlete_id= athletes.id where athletes.gender='Women' group by games.year) t2 on t1.yearmen = t2.yearwomen  order by yearmen;"):
		year.append(row[0])
		medals_men.append(row[1])
		medals_women.append(row[2])



	line_chart = pygal.Bar()
	line_chart.title = "Medals won per gender over time"
	line_chart.x_labels = year
	line_chart.add('Men', medals_men)
	line_chart.add('Women', medals_women)

	line_chart.render_to_file('static/year_gender.svg')  




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
	gauge.title = "Gender split in the World"

	gauge.add('Women winter', [{'value': women_win_winter, 'max_value': 100}])
	gauge.add('Men winter', [{'value': men_win_winter, 'max_value': 100}])

	gauge.render_to_file("static/world_winter_summer999.svg")

#9

	medals= []
	sport=[]
	athlete = []
	country = []

	for row in c.execute("select athelete_ID, category_id, medals,sport,country_code, athlete from (Select athelete_ID, medals,sport,athlete,Country_code, category_id, max(medals) as maximum from  (Select athelete_ID,count(medal) as medals, category_id, Sport, athletes.athlete,Country_code from reward left join athletes on reward.Athelete_id=athletes.id group by athelete_ID, sport) group by sport) where medals = maximum order by medals desc limit 10 ;"):
		medals.append(float(row[2]))
		sport.append(row[3])
		athlete.append(row[5])
		country.append(row[4])


	bol=list(zip(sport,medals,athlete,country))

	record = pygal.HorizontalBar()
	record.title = 'Top 10 Athletes by Sport '

	for r in bol:
		record.add(r[0], [{'value': r[1], 'label': r[2]}])


	record.render_to_file('static/recordbysport.svg')

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
		

	worldmap_chart.render_to_file('static/world_best22.svg')

#11 

	country =[]
	men = []
	women = []

	for row in c.execute("select t1.country_code, t1.Medals_men, t2.Medals_women from (Select distinct country_code, count(medal) as Medals_men from unique_medals left join athletes on athletes.id= unique_medals.athlete_id where athletes.Gender = 'Men' group by country_Code order by medals_men desc) t1 left join (Select distinct country_code, count(medal) as Medals_women from unique_medals left join athletes on athletes.id= unique_medals.athlete_id where  athletes.gender = 'Women' group by country_Code order by medals_women desc) t2 on t1.country_code = t2.country_code limit 30;"):
		country.append(row[0])
		men.append(row[1])
		women.append(row[2])



	radar_chart = pygal.Radar()
	radar_chart.title = 'Men vs Women victory split'
	radar_chart.x_labels = country
	radar_chart.add('Medals Men', men)
	radar_chart.add('Medals Women', women)

	radar_chart.render_to_file('static/radar11.svg')

#12

	country =[]
	med = []
	mov = []

	for row in c.execute("select t1.country_code, t1.Medals_2012, t2.Movies_2012 from (Select distinct country_Code, count(medal) as Medals_2012 from unique_medals left join categories on categories.id= unique_medals.category_id left join games on games.id = categories.games_id left join countries on countries.id = games.countries_id left join athletes on unique_medals.athlete_id= athletes.id where games.year = 2012 group by country_Code) t1 Inner join (Select distinct Code, count(movies.id) as Movies_2012 from movies left join countries on countries.country=movies.country where title_year = 2012 group by code ) t2 on t1.country_Code = t2.code order by medals_2012 desc LIMIT 10 ;"):
		country.append(row[0])
		med.append(row[1])
		mov.append(row[2])


	dot_chart = pygal.Dot(x_label_rotation=30)
	dot_chart.title = 'Number of movies and medals in 2012'
	dot_chart.x_labels = country
	dot_chart.add('Medals', med)
	dot_chart.add('Movies', mov)


	dot_chart.render_to_file('static/combine.svg')
	return render_template('hello.html', name=name)

if __name__ == "__main__":
    app.run()
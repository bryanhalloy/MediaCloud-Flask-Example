import ConfigParser, logging, datetime, os

from flask import Flask, render_template, request

import mediacloud

CONFIG_FILE = 'settings.config'
basedir = os.path.dirname(os.path.realpath(__file__))

# load the settings file
config = ConfigParser.ConfigParser()
config.read(os.path.join(basedir, 'settings.config'))

# set up logging
log_file_path = os.path.join(basedir,'logs','mcserver.log')
logging.basicConfig(filename=log_file_path,level=logging.DEBUG)
logging.info("Starting the MediaCloud example Flask app!")

# clean a mediacloud api client
mc = mediacloud.api.MediaCloud( config.get('mediacloud','api_key') )



app = Flask(__name__)

@app.route("/")
def home():
    return render_template("search-form.html")

@app.route("/search",methods=['POST'])
def search_results():
    keywords = request.form['keywords']
    
    #user inputs start and end dates
    year_start = request.form['year_start']
    year_start = int(year_start)
    month_start = request.form['month_start']
    month_start = int(month_start)
    day_start = request.form['day_start']
    day_start = int(day_start)
    
    year_end = request.form['year_end']
    year_end = int(year_end)
    month_end = request.form['month_end']
    month_end = int(month_end)
    day_end = request.form['day_end']
    day_end = int(day_end)    
    
    date_start = datetime.date( year_start, month_start, day_start)
    date_end = datetime.date( year_end, month_end, day_end)   

   #fetch results
    results_split = mc.sentenceCount(keywords,
        solr_filter=[mc.publish_date_query( date_start, date_end ),
                     'media_sets_id:1' ], split = 1)
    results_split = results_split.items()
    
    
    results= mc.sentenceCount(keywords,
        solr_filter=[mc.publish_date_query( date_start, date_end ),
                     'media_sets_id:1' ])    
    return render_template("search-results.html", 
        keywords=keywords, sentenceCount=results['count'] )

if __name__ == "__main__":
    app.debug = True
    app.run()

from flask import Flask, render_template, request
from flask_mail import Mail, Message
import pickle
import nexmo

app = Flask(__name__)
mail = Mail(app)

#Mail Confugirations
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'shikhar.17.srivastava@st.niituniversity.in'
app.config['MAIL_PASSWORD'] = '*****************'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)


#Message Confugirations
app.config['SECRET_KEY'] = '*****************'

#Nexmo Message confugirations
client = nexmo.Client(key='88dd777b', secret='*****************')

# open a file, where one has stored the pickled data
file = open('model.pkl', 'rb')
clf = pickle.load(file)
file.close()

@app.route('/', methods = ["GET","POST"])

def hello_world():    
    if request.method == 'POST':
        myDict = request.form  

        fullname = myDict['fullname']
        email = myDict['email']
        contact = myDict['contact']
        fever = int(myDict['fever'])
        age = int(myDict['age'])
        pain = int(myDict['pain'])
        noseRunning = int(myDict['noseRunning'])
        breatingDifficulty = int(myDict['breatingDifficulty'])
        
        print(myDict)

        #inference code
        sampleInput = [fever, pain, age, noseRunning, breatingDifficulty]

        OutputPrediction = clf.predict([sampleInput]) #to get the prediction
        print (OutputPrediction)
 
        OutputProbability = clf.predict_proba([sampleInput])[0][1] #to get the probability
        print (OutputProbability)

        #Send Mail
        msg = Message('COVID-19 Predictor!', sender = 'shikhar.17.srivastava@st.niituniversity.in', recipients = [email])
        msg.body = "Thank You for using COVID-19 Predictor! Please visit us again:)"
        #msg.subject = "COVID-19 Predictor!"
        #msg.html = "\n\n<h4><u>Your Prediction percentage of COVID-19 is 45%</u></h4>\n <p>The details that was entered is as follows:</p>\n <p>Age : 20</p>\n <p>Body Temperature : 93 °F</p>\n <p>Body Pain: Yes</p>\n <p>Running Nose: Yes</p>\n <p>Breathing Difficulty: Yes</p>"
        mail.send(msg)

        
        #Send Text Message
        client.send_message({
            'from': 'Vonage APIs',
            'to': '+91 **** *** ***',
            'text': 'Hello! This Message from COVID-19 Predictor App by Shikhar:)',
        })
        
        return render_template('output.html', inf= round(OutputProbability*100)), "Mail Sent", "Text Message Sent" 
    return render_template('index.html')
    #return 'Hello Sangam!' + str(sampleOutputProbability1) + str(sampleOutputPrediction1)

if __name__ == "__main__":
    app.run(debug=True)

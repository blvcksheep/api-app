from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''@localhost/crudapi'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    address = db.Column(db.String(80))
    gender = db.Column(db.String(20))
    sms_logs = db.relationship('Sms_log', backref='client')

    def __init__(self, name, address, gender, sms_logs=[]):
        self.name = name
        self.address = address
        self.gender = gender
        self.sms_logs = sms_logs

    def __repr__(self):
        return f"{self.name} - {self.address} - {self.gender}"


class Sms_log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(20))
    message = db.Column(db.Text)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'))

    def __init__(self, number, message, client_id):
        self.number = number
        self.message = message
        self.client_id = client_id

    def __repr__(self):
        return f"{self.number} - {self.message}"


@app.route('/')
def index():
    return "TESTTTTTTTTTTTTTTTTTT"

# DISPLAY ALL CLIENT
@app.route('/clients')
def get_clients():
    clients = Client.query.all()

    output = []
    for clit in clients:
        client_data = {'Name': clit.name,
                       "Address": clit.address,
                       "Gender": clit.gender}

        output.append(client_data)

    return {"Clients": output}


# DISPLAY SPECIFIC CLIENT AND IT'S SMS
@app.route('/clients/<int:client_id>')
def get_client(client_id):
    clit = Client.query.get_or_404(client_id)

    client = {"Name": clit.name,
              "Address": clit.address, "Gender": clit.gender}

    output = []
    for sms in clit.sms_logs:
        sms_log = {"Number": sms.id,
                   "Number": sms.number, "Message": sms.message}
        output.append(sms_log)

    return {"Client": client, "Sms log": output}

# ADD CLIENT
@app.route('/clients', methods=['POST'])
def add_client():
    client = Client(name=request.json['name'],
                    address=request.json['address'],
                    gender=request.json['gender'])
    db.session.add(client)
    db.session.commit()
    return {'id': client.id}

# DELETE CLIENT
@app.route('/clients/<id>', methods=['DELETE'])
def delete_client(id):
    client = Client.query.get_or_404(id)
    if client is None:
        return {id: " is not found"}
    db.session.delete(client)
    db.session.commit()
    return {id: "is already delete"}

# DISPLAY ALL CLIENTS AND SMS_LOG
@app.route('/clients/sms_logs')
def get_clients_sms():
    clients = Client.query.order_by(Client.id.desc()).all()
    sms_logs = Sms_log.query.order_by(Sms_log.client_id.desc()).all()

    client_output = []
    for clit in clients:
        client_data = {'Name': clit.name,
                       "Address": clit.address,
                       "Gender": clit.gender}

        client_output.append(client_data)

        sms_output = []
        for smsl in sms_logs:
            sms_data = {'number': smsl.number,
                        "Address": smsl.message}

            sms_output.append(sms_data)

    return {"Clients": client_output, "Sms Logs": sms_output}


# ------------------FUNCTIONS FOR SMS LOGS----------------------------

# DISPLAY SMS LOGS
@app.route('/sms_logs')
def get_smslogs():
    sms_logs = Sms_log.query.order_by(Sms_log.id.desc()).all()

    output = []
    for smsl in sms_logs:
        sms_data = {'number': smsl.number,
                    "Address": smsl.message}

        output.append(sms_data)

    return {"Clients": output}

# ADD SMS
@app.route('/clients/sms', methods=['POST'])
def add_sms():

    sms = Sms_log(number=request.json['number'],
                  message=request.json['message'],
                  client_id=request.json['client_id'])

    db.session.add(sms)
    db.session.commit()

    return {'id': sms.id}

# DELETE SMS
@app.route('/clients/sms/<id>', methods=['DELETE'])
def delete_sms(id):
    sms = Sms_log.query.get_or_404(id)
    if sms is None:
        return {id: " is not found"}
    db.session.delete(sms)
    db.session.commit()
    return {id: "is already delete"}

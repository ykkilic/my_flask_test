from flask import Flask,render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String
from sqlalchemy.exc import SQLAlchemyError


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:20022007@localhost:5432/flasktest'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'data'
    id = Column(Integer, primary_key = True,index=True)
    name = Column(String)

def create_tables():
    db.create_all()

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/data/',methods=['POST'])
def fetch_data():
    try:
        data =request.get_json()
        Name = data.get('name')
        ID = data.get('id')
        
        if not Name or ID is None:
            return jsonify({'message' : 'failed'})
        
        new_user = User(id=int(ID),name=Name)
        db.session.add(new_user)
        db.session.commit()
        
        return jsonify({'message' : 'succes'})
    except SQLAlchemyError as e:
        return jsonify({'message' : 'ERROR', 'ERROR' : str(e)})
    except Exception as e:
        return jsonify({'message' : 'ERROR', 'ERROR' : str(e)})

if __name__ == '__main__':
    app.run(debug=True)
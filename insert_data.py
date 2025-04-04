from application import app, db, University
import datetime

def insert_data():
    # Create Table
    with app.app_context():
        db.create_all()

        # Insert Test Data
        universities = [
                University(name="National University of Singapore", country="Singapore", webpages="https://www.nus.edu.sg"),
                University(name="Nanyang Technological University", country="Singapore", webpages="https://www.ntu.edu.sg"),
                University(name="Singapore Management University", country="Singapore", webpages="https://www.smu.edu.sg"),
                University(name="Singapore University of Technology and Design", country="Singapore", webpages="https://www.sutd.edu.sg"),
                University(name="Yale-NUS College", country="Singapore", webpages="https://www.yale-nus.edu.sg"),
                University(name="Singapore Institute of Technology", country="Singapore", webpages="https://www.singaporetech.edu.sg"),
                University(name="Singapore University of Social Sciences", country="Singapore", webpages="https://www.suss.edu.sg"),
                University(name="Singapore Institute of Management", country="Singapore", webpages="https://www.sim.edu.sg/"),
                University(name="University of Wollongong", country="Australia", webpages="https://www.uow.edu.au/"),
                University(name="Harvard University", country="USA", webpages="https://www.harvard.edu")
            ]

        db.session.bulk_save_objects(universities)
        db.session.commit()

if __name__ == "__main__":
    insert_data()


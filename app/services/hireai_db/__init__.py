import psycopg2
from app.services.hireai_db.applicant import ApplicantContext
from app.services.hireai_db.interview_invitation import InterviewInvitationContext

class HireAIDB:
    def __init__(self, db_config: dict):
        try:
            conn = psycopg2.connect(
                dbname=db_config['dbname'],
                user=db_config['user'],
                password=db_config['password'],
                host=db_config['host'],
            )
            # run some ping to test the connection
            self.connection_string = f"postgresql+psycopg2://{db_config['user']}:{db_config['password']}@{db_config['host']}/{db_config['dbname']}"
            with conn.cursor() as cursor:
                cursor.execute("SELECT 1")
            self.applicant = ApplicantContext(conn=conn)
            self.interview_invitation = InterviewInvitationContext(conn=conn)
        except psycopg2.Error as e:
            print(f"Error connecting to the database: {e}")
            raise e

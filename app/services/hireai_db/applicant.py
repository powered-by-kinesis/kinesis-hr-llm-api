import psycopg2
import json

class ApplicantContext:
    def __init__(self, conn: psycopg2.extensions.connection):
        self.conn = conn

    def get(self, applicant_id: int) -> dict:
        try:
            cursor = self.conn.cursor()
            query = "SELECT * FROM applicants WHERE id = %s"
            cursor.execute(query, (applicant_id,))
            result = cursor.fetchone()
            if result:
                columns = [desc[0] for desc in cursor.description]
                return dict(zip(columns, result))
            else:
                print(f"No applicant found with id {applicant_id}")
                return {}
        except psycopg2.Error as e:
            print(f"Error fetching applicant {applicant_id}: {e}")
            raise e
        finally:
            cursor.close()

    def to_db_safe(self, value):
            if isinstance(value, (dict, list)):
                return json.dumps(value)
            return value

    def update(self, applicant_id: int, data: dict) -> dict:
        try:
            cursor = self.conn.cursor()
            set_clause = ', '.join([f"{key} = %s" for key in data.keys()])

            processed_data = {k: self.to_db_safe(v) for k, v in data.items()}

            values = list(processed_data.values())
            values.append(applicant_id)

            query = f"UPDATE applicants SET {set_clause} WHERE id = %s"

            cursor.execute(query, values)
            cursor.connection.commit()
            return self.get(applicant_id)  
        except psycopg2.Error as e:
            print(f"Error updating applicant {applicant_id}: {e}")
            raise e
        finally:
            cursor.close()

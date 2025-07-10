import psycopg2

class InterviewInvitationContext:
    def __init__(self, conn: psycopg2.extensions.connection):
        self.conn = conn
    
    def get(self, id: int) -> dict:
        try:
            cursor = self.conn.cursor()
            query = "SELECT * FROM interview_invitations WHERE id = %s"
            cursor.execute(query, (id,))
            result = cursor.fetchone()
            if result:
                columns = [desc[0] for desc in cursor.description]
                return dict(zip(columns, result))
            else:
                print(f"No interview invitation found with id {id}")
                return {}
        except psycopg2.Error as e:
            print(f"Error fetching interview invitation {id}: {e}")
            raise e
        finally:
            cursor.close()

    def update(self, id: int, data: dict) -> dict:
        try:
            cursor = self.conn.cursor()
            set_clause = ', '.join([f'"{key}" = %s' for key in data.keys()])
            values = list(data.values())
            values.append(id)

            query = f"UPDATE interview_invitations SET {set_clause} WHERE id = %s"
            cursor.execute(query, values)
            cursor.connection.commit()
            print(f"Interview invitation {id} updated successfully")
            # return updated data as a dictionary
            return self.get(id)
        except psycopg2.Error as e:
            print(f"Error updating interview invitation {id}: {e}")
            raise e
        finally:
            cursor.close()
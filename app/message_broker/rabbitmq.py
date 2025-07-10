from aio_pika import connect_robust, abc, Message
from app.api.dependencies import build_services
from app.domain.cv import SimpleCVModelExtract
import json

class RabbitMQ:
    def __init__(self, connection_string: str):
        self.connection_string = connection_string
        self.services = build_services()
    
    async def connect(self):
        self.connection = await connect_robust(self.connection_string)
        self.channel = await self.connection.channel()
        self.queue = await self.channel.declare_queue("test_change", durable=True)
        await self.queue.consume(self.on_message, no_ack=False)

    async def on_message(self, message: abc.AbstractIncomingMessage):
        try:
            body = message.body.decode()
            json_body = json.loads(body)
            if (json_body['event'] == 'update-applicant-from-embedded'):
                data = json_body['data']
                print(f"Processing message: {data}")
                applicant_id = data['applicant_id']

                metadata_filters = [
                    {"key": "applicant_id", "value": applicant_id}
                ]
                st_output = await self.services.chat_engine_service.get_structured_output(
                    model_class=SimpleCVModelExtract,
                    query="Get the summary(generate if not present), education, work history, location, and international languages(generate from where they live if not present)",
                    metadata_filters=metadata_filters
                )
                st_output_dict = st_output.model_dump(exclude_none=True)
                print(f"Structured output: {st_output_dict}")
                self.services.hireai_db.applicant.update(applicant_id, {
                    "summary": st_output_dict['summary'] if 'summary' in st_output_dict else "",
                    "education": st_output_dict['educations'] if 'educations' in st_output_dict else [],
                    "experience": st_output_dict['experiences'] if 'experiences' in st_output_dict else [],
                    "location": st_output_dict['location'] if 'location' in st_output_dict else [],
                    "languages": st_output_dict['languages'] if 'languages' in st_output_dict else []
                })
                await message.ack()
                
            elif (json_body['event'] == 'store-pdf'):
                data = json_body['data']
                print(f"Processing message: {data}")
                file_urls = data['file_urls']
                applicant_id = data['applicant_id']

                await self.services.vector_store_index_service.add(files=file_urls, metadata={"applicant_id": applicant_id})
                await self.send_message(json.dumps({
                    "event": "update-applicant-from-embedded",
                    "data": {
                        "applicant_id": applicant_id
                    }
                }))
                await message.ack()
            else:
                print(f"Unknown event type: {json_body['event']}")
                await message.ack()
        except Exception as e:
            print(f"Error processing message: {e}")

    async def send_message(self, message: str):
        if not hasattr(self, 'channel'):
            raise RuntimeError("RabbitMQ connection is not established.")
        await self.channel.default_exchange.publish(
            Message(body=message.encode()),
            routing_key=self.queue.name
        )
        print(f"Sent message: {message}")

    async def close(self):
        if hasattr(self, 'connection'):
            await self.connection.close()
            print("RabbitMQ connection closed.")
        else:
            print("No RabbitMQ connection to close.")

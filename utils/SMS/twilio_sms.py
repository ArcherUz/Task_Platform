from twilio.rest import Client
import os

account_sid = os.getenv('TWILIO_ACCOUNT_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')
client = Client(account_sid, auth_token)


def send_sms(target, code):
  #code = random.randrange(1000, 9999)
  try:
    message = client.messages.create(
      from_=os.getenv('TWILIO_NUMBER'),
      body='test msg'+str(code),
      to=target
    )
  except Exception as e:
    message = 'Phone type error'
  return message
  #print(message.sid)
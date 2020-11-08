from twilio.rest import Client
# 8454673498
def send_text_notification(number, body):
	if "+1" not in number:
		number = "+1" + number
	# Your Account SID from twilio.com/console
	account_sid = "AC9ca75293b66c581d50727bfb37fa9a37"
	# Your Auth Token from twilio.com/console
	auth_token  = "ee86b4537526481f6d391f0f333062dd"

	client = Client(account_sid, auth_token)

	message = client.messages.create(
	    to=number, 
	    from_="+19253019701",
	    body=body)
	print(message.sid)
	print(number, body)

if __name__ == "__main__":
	number = "6313577459"
	body  = "https://zoom.us/meeting/96407527780   "
	send_text_notification(number, body)


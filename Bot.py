import datetime
import telebot
from googleapiclient.discovery import build
from google.oauth2 import service_account

date = datetime.date.today().isoformat()


apikey = 'BOT-API' #TODO: ADD THE API KEY FOR THE BOT (DIFFERENT FOR EACH BOT)
bot = telebot.TeleBot(apikey)


SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = 'CREDS' #TODO: ADD THE CREDENTIALS FILE FOR THE GOOGLE DEVELOPER CONSOLE SERVICE ACCOUNT
creds = None
creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
# The ID of spreadsheet.
SAMPLE_SPREADSHEET_ID = 'SHEETID' #TODO: ADD THE GOOGLE SHEET ID (DIFFERENT FOR EACH GOOGLE SHEET)
service = build('sheets', 'v4', credentials=creds)
# Call the Sheets API
sheet = service.spreadsheets()


@bot.message_handler(commands=['help','menu','start'])
def hello(message):
    bot.send_message(message.chat.id, "SAMPLE TEXT")    #you can use 'bot.reply_to(message, <Message>)' if you want to send a reply.

@bot.message_handler(commands=['intro'])
def intro(message):
    chatid=message.chat.id
    bot.send_message(chatid,"Format:\nName of the person entering,(-)Amount,To/From")
    bot.send_message(chatid,"--> All the columns given above should be seperated by a comma\n--> If the amount is income, you don't need to do anything. But if it is expense, you need to specify it with a '-' symbol like '-1000'\n--> Check /help for the available commands")

@bot.message_handler(func=lambda message: True)
def echo_message(message):
    val = []
    chatid=message.chat.id
    message_text = message.text
    message_text = message_text.split(",")

    if(len(message_text)!=3):
        bot.send_message(chatid,"Input error: The number of arguments must be equal to 3. Check /intro to learn more.")

    elif(message_text[0].isalpha()==False):
        bot.send_message(chatid,"Input error: The name must not contain any numbers or symbols.")

    else:
        #val = message_text+[date]
        val = [date]+message_text
        bot.send_message(chatid,"The value updated is "+str(val))
        if ('-' in message_text[1]):
            val.insert(3,"")
            request = sheet.values().append(spreadsheetId=SAMPLE_SPREADSHEET_ID, range='Sheet1!a1:e1', valueInputOption="USER_ENTERED", insertDataOption="INSERT_ROWS", body={'values':[val]}).execute()
        else:
            request = sheet.values().append(spreadsheetId=SAMPLE_SPREADSHEET_ID, range='Sheet1!a1:e1', valueInputOption="USER_ENTERED", insertDataOption="INSERT_ROWS", body={'values':[val]}).execute()



bot.polling()                                           #This is used to keep the bot listening

import os
import boto3
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackContext
import json

# Initialize Lambda client
lambda_client = boto3.client('lambda')
TELEGRAM_BOT_TOKEN = "6618622439:AAHSQRJM8sgN4ABxu1fm77QGy9UJg3ozTCY"

# Define the register_user command handler
def register_user(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat_id

    # Invoke the register_user Lambda function
    response = lambda_client.invoke(
        FunctionName='register_user_lambda_function',
        InvocationType='RequestResponse',
        Payload=json.dumps({'chat_id': chat_id})
    )

    # Parse the response and send the reply to the user
    reply = json.loads(response['Payload'].read())
    update.message.reply_text(reply)

# Define the deregister_user command handler
def deregister_user(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat_id

    # Invoke the deregister_user Lambda function
    response = lambda_client.invoke(
        FunctionName='deregister_user_lambda_function',
        InvocationType='RequestResponse',
        Payload=json.dumps({'chat_id': chat_id})
    )

    # Parse the response and send the reply to the user
    reply = json.loads(response['Payload'].read())
    update.message.reply_text(reply)

# Define the admin_options command handler
def admin_options(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat_id

    # Invoke the admin_options Lambda function
    response = lambda_client.invoke(
        FunctionName='admin_options_lambda_function',
        InvocationType='RequestResponse',
        Payload=json.dumps({'chat_id': chat_id})
    )

    # Parse the response and send the reply to the user
    reply = json.loads(response['Payload'].read())
    update.message.reply_text(reply)

# Define the main function
def main() -> None:
    # Initialize the updater and dispatcher
    updater = Updater(token=TELEGRAM_BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # Register the command handlers
    dispatcher.add_handler(CommandHandler('command1', register_user))
    dispatcher.add_handler(CommandHandler('command2', deregister_user))
    dispatcher.add_handler(CommandHandler('admin_options', admin_options))

    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()

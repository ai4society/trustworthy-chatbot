# SafeChat Framework


1. Install anaconda from https://www.anaconda.com/download
2. To create a virtual environment, run the command ‘conda create –name <env_name> python==3.8’
3. To activate the environment, run ‘conda activate <env_name>’
4. Run ‘git clone https://github.com/ai4society/trustworthy-chatbot.git’ to clone our SafeChat repository.
5. Go to the project directory. Run ‘pip install –r requirements.txt’ to install all the required packages.
6. Create a new ‘Chat.csv’ file in the ‘data/input/’ directory with your desired FAQs or use the existing one. Your CSV should have a column called 'Question' and another one called 'Answer'.
7. Run the ’code/extract_intent.py’, ‘code/paraphraser.py’, and ‘code/configure_rasa.py’, files in the same order to create your chatbot.
8. Go to the generated 'Chatbot/' directory and run 'rasa train' to train the chatbot. To talk to the trained chatbot run the ‘rasa shell’ command. Also, run ‘rasa run actions’ in another instance of the terminal (a custom action was created in 'actions.py' to store the conversation.).


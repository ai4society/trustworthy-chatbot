# SafeChat Framework


1. Install anaconda from https://www.anaconda.com/download
2. To create a virtual environment, run the command ‘conda create –name <env_name> python==3.7’
3. To activate the environment, run ‘conda activate <env_name>’
4. Run ‘git clone https://github.com/ai4society/trustworthy-chatbot.git’ to clone our SafeChat repository.
5. Go to the project directory. Run ‘pip install –r requirements.txt’ to install all the required packages.
6. Create a new ‘Chat.csv’ file in the ‘data/input/’ directory with your desired FAQs or use the existing one. Your CSV should have a column called 'Question' and another one called 'Answer'.
7. Run ‘code/configure_rasa.py’, ’code/extract_intent.py’ and ‘code/paraphraser.py’ files in the same order to create your chatbot.
8. Go to the generated 'Chatbot' directory and talk to the trained chatbot using the ‘rasa shell’ command.


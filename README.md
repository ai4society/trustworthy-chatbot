# SafeChat: An Architecture for Building Trustworthy Collaborative Assistants

SafeChat is an architecture that aims to provide a safe and secure environment for users to interact with AI chatbots in trust-sensitive domains. It uses a combination of neural (learning-based, including generative AI) and symbolic (rule-based) methods, together called a neuro-symbolic approach, to provide known information in easy-to-use consume forms that are adapted from user interactions (provenance). The chatbots generated are scalable, quick to build and is evaluated for trust issues like fairness, robustness and appropriateness of responses.

## 🎯 Key Features
- Scalable architecture
- Safe and traceable chatbot interactions
- Data agnostic

## 📋 Prerequisites
Before you begin, ensure you have the following installed:
- [Python](https://www.python.org/)
- [Anaconda](https://www.anaconda.com/download)


## 🚀 Getting Started
1. **Clone the repository**
   ```bash
   git clone https://github.com/ai4society/trustworthy-chatbot
   cd trustworthy-chatbot
   ```
2. **Create and activate a conda virtual environment**
   ```bash
   conda create --name safechat_venv python==3.8
   conda activate safechat_venv
   ```
3. **Install required packages**
   ```bash
   pip install -r requirements.txt
   ```
4. **Provide question answer pairs for your use case**

    * Create a new `data/input/<file-name>.csv` file with your desired question answer pairs or use the existing one. Your CSV should have a column called *Question* and another one called *Answer*. Optionally, if you would like for your chatbot to give traceable responses to your user, include columns *Timestamp* with [UNIX timestamps](https://www.unixtimestamp.com/) corresponding to the date of the response and *Source* with strings which may be URLs or names of the organization which procured the response.
    * Create a new `data/input/DNA.csv` that is a single column list of questions that you would like your chatbot to avoid answering. Ensure that the heading of this column is *Questions*
5. **Process your data and configure the chatbot using the RASA Open Source framework**

    * Extract the intent for user queries: `python code/extract_intent.py` By default, this will read `data/input/Chat.csv`, however, you can specify a different csv file in the `data/input` directory with the `-f` or `--file` argument:`python code/extract_intent.py -f Election_QA.csv` 
      * Saves to `data/input/Chat_intent.csv` 
    * Paraphrase all user queries: `python code/paraphraser.py`
      * Saves to `data/input/paraphrased.json`
    * Configure directory for RASA Open Source: `python code/configure_rasa.py`
      * Saves to `Chatbot` directory. Deletes existing `Chatbot` by default, so save in different location if you would like to save the configuration.
6. **Train and converse with your chatbot**

    * Navigate to chatbot directory: `cd Chatbot` 
    * Train chatbot: `rasa train`
    * Converse with trained chatbot: `rasa shell`
    * Optionally, if you would like your chatbot to handle some business-logic for some queries, you may utilize the [RASA Actions](https://rasa.com/docs/rasa/actions/)


## 📁 Project Structure
```
.
├── code/               # SafeChat logic for generating chatbot files
├── data/               # All provided and intermediate data files
├── doc/                # Documentation and design assets
└── rasa_template/      # Template directory for RASA Open Source
```

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 🛠️ Usage Examples

The following table highlights different use cases for SafeChat:

| **Domain**           | **Description**                                           | **Details**                                                                                                                                                 |
| -------------------- | --------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Election Information | Safe chatbot behavior for election messaging              | [Disseminating Authentic Public Messages using Chatbots - A Case Study with ElectionBot-SC](https://ai4society.github.io/publications/papers_local/AAAI_25_SafeChat_Workshop.pdf) |
| Voter Participation  | Chatbots for promoting voter engagement and participation | [On Safe and Usable Chatbots for Promoting Voter Participation](https://onlinelibrary.wiley.com/doi/full/10.1002/aaai.12109)                                |
| Financial Advice     | LLMs for fairness and efficacy in decision-making         | [LLMs for Financial Advisement: A Fairness and Efficacy Study in Personal Decision Making](https://dl.acm.org/doi/fullHtml/10.1145/3604237.3626867)         |

## 📝 Citation

If you use SafeChat in your work, please cite the following publication:

```bibtex
@inproceedings{safechat-arch-github,
  title={SafeChat: An Architecture for Building Trustworthy Collaborative Assistants},
  author={Muppasani, Bharath and Lakkaraju, Kausik and Gupta, Nitin and Nagpal, Vansh and Jones, Sara Rae and Srivastava, Biplav},
  booktitle={\url{https://github.com/ai4society/trustworthy-chatbot}},
  year={2024}
}
```

## 📚 Publications

- [Disseminating Authentic Public Messages using Chatbots - A Case Study with ElectionBot-SC to Understand and Compare Chatbot Behavior for Safe Election Information in South Carolina](https://ai4society.github.io/publications/papers_local/AAAI_25_SafeChat_Workshop.pdf); Nitin Gupta, Vansh Nagpal, Bharath Muppasani, Kausik Lakkaraju, Sara Jones, Biplav Srivastava; Thirty-Ninth AAAI Conference on Artificial Intelligence (AAAI-25), Philadelphia, USA, Feb 2025

- [On Safe and Usable Chatbots for Promoting Voter Participation](https://onlinelibrary.wiley.com/doi/full/10.1002/aaai.12109); Bharath Muppasani, Vishal Pallagani, Kausik Lakkaraju, Shuge Lei, Biplav Srivastava, Brett Robertson, Andrea Hickerson, Vignesh Narayanan; AAAI AI Magazine 2023

- [LLMs for Financial Advisement: A Fairness and Efficacy Study in Personal Decision Making](https://dl.acm.org/doi/fullHtml/10.1145/3604237.3626867); Kausik Lakkaraju, Sara Rae Jones, Sai Krishna Revanth Vuruma, Vishal Pallagani, Bharath C Muppasani and Biplav Srivastava; 4th ACM International Conference on AI in Finance: ICAIF'23, New York, 2023

# SafeChat: A Framework for Building Trustworthy Collaborative Assistants

SafeChat is an architecture to create collaborative assistants, also called chatbots and digital assistants, which can serve as safe decision supports to provide reliable, authenticated, information in trust-sensitive domains. It uses a combination of neural (learning-based, including generative AI) and symbolic (rule-based) methods, together called a neuro-symbolic approach, to provide known information in easy-to-use consume forms that are adapted from user interactions (provenance). The chatbots generated are scalable, quick to build and have in-built support for evaluation of trust issues like fairness, robustness and appropriateness of responses. SafeChat is implemented over the open-source, Rasa platform, to create a tool (and hence, an executable framework) but the approach is platform-agnostic.

## 🎯 Key Features
- For **safety**
   >- **Safe design** where only responses that are grounded and traceable to an allowed source  will be answered (provenance). 
   >- Supports **do-not-respond strategy** that can deflect certain user questions which may be harmful if answered.
- For **usability**
   >- Supports automated **trust ratings** to  communicate the chatbot’s expected behavior on dimensions like abusive language and bias.
   >- Supports **automatic, extractive summarization** of long answers that can be traced back to source
- For **fast, scalable, development**
   >- Provides a **CSV-driven chatbot building workflow** that does not require deep AI expertise, making it accessible to developers with varying levels of AI knowledge and experience.
   >- **Domain agnostic**, scalable architecture. The backend can be extended with CSV-driven web integration.
   >- **Support for testing**, including control and treatment group formation and analysis of results, for randomized control trial (RCT)

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

<table>
  <tr>
    <th>Domain</th>
    <th>Description</th>
    <th>Details</th>
  </tr>
  <tr>
    <td>Election Information</td>
    <td>Safe chatbot behavior for promoting voter engagement and participation</td>
    <td>
      <ul>
        <li><a href="https://ai4society.github.io/publications/papers_local/AAAI_25_SafeChat_Workshop.pdf">Disseminating Authentic Public Messages using Chatbots - A Case Study with ElectionBot-SC</a><sup>[1]</sup></li>
        <li><a href="https://onlinelibrary.wiley.com/doi/full/10.1002/aaai.12109">On Safe and Usable Chatbots for Promoting Voter Participation</a><sup>[2]</sup></li>
      </ul>
    </td>
  </tr>
  <tr>
    <td>Financial Advice</td>
    <td>LLMs for fairness and efficacy in decision-makin</td>
    <td>
       <ul>
         <li><a href="https://dl.acm.org/doi/fullHtml/10.1145/3604237.3626867">LLMs for Financial Advisement: A Fairness and Efficacy Study in Personal Decision Making</a><sup>[3]</sup></li>
       </ul>
    </td>
  </tr>
</table>

## 📝 Citation

If you use SafeChat in your work, please cite the following publication:

```bibtex
@inproceedings{safechat-arch-github,
  title={SafeChat: A Framework for Building Trustworthy Collaborative Assistants (Github)},
  author={Muppasani, Bharath and Lakkaraju, Kausik and Gupta, Nitin and Nagpal, Vansh and Jones, Sara Rae and Srivastava, Biplav},
  booktitle={\url{https://github.com/ai4society/trustworthy-chatbot}},
  year={2024}
}
```

## 📚 Publications

1. [Disseminating Authentic Public Messages using Chatbots - A Case Study with ElectionBot-SC to Understand and Compare Chatbot Behavior for Safe Election Information in South Carolina](https://ai4society.github.io/publications/papers_local/AAAI_25_SafeChat_Workshop.pdf); Nitin Gupta, Vansh Nagpal, Bharath Muppasani, Kausik Lakkaraju, Sara Jones, Biplav Srivastava; Workshop on AI for Public Missions (AIPM) at Thirty-Ninth AAAI Conference on Artificial Intelligence (AAAI-25), Philadelphia, USA, Feb 2025

2. [On Safe and Usable Chatbots for Promoting Voter Participation](https://onlinelibrary.wiley.com/doi/full/10.1002/aaai.12109); Bharath Muppasani, Vishal Pallagani, Kausik Lakkaraju, Shuge Lei, Biplav Srivastava, Brett Robertson, Andrea Hickerson, Vignesh Narayanan; AAAI AI Magazine 2023

3. [LLMs for Financial Advisement: A Fairness and Efficacy Study in Personal Decision Making](https://dl.acm.org/doi/fullHtml/10.1145/3604237.3626867); Kausik Lakkaraju, Sara Rae Jones, Sai Krishna Revanth Vuruma, Vishal Pallagani, Bharath C Muppasani and Biplav Srivastava; 4th ACM International Conference on AI in Finance: ICAIF'23, New York, 2023

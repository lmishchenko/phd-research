## PhD Research Repository: Fake News Detection

### Overview
This repository is dedicated to enhancing the speed of detecting and labeling fake news with limited prior information, as described in the dissertation abstract. The research aims to develop a method for the rapid detection and labeling of fake news messages based on limited prior information.

### Methodology
The research utilizes a complex synergistic combination of natural language processing processes, including:

- Frequency analysis of text tokens in short informational messages.
- Improved content analysis method for fake news.
- Binary message classification using an improved Naive Bayes classifier.
- Integration of the BM25 ranking function.

The method stands out for implementing the learning process on a dynamically updated set of short informational messages from credible sources, ensuring a high accuracy ranging from 85% to 93% for binary labeling of fake news messages.

### Contributions
- The binary classification and labeling method of fake news has been improved using the Naive Bayes classifier and the BM25 ranking function.
- Adaptive selection of ranking function parameters based on experimental data obtained from frequency analysis of news from credible sources has increased the accuracy of text data classification by 14% on a dynamically updated set of short informational messages.
- The content analysis method of fake news has been enhanced based on the use of unsupervised learning schemes, allowing for the rapid formation of fake features, considering significant changes in style and content sphere based on the brief content of the message.

### Results
Experiments with the proposed technology for implementing rapid detection of fake news with limited prior information have shown promising results:

- High resilience to form a binary assessment with fake labeling for consumers with critical accessibility conditions.
- Enablement of the detection and binary labeling of fake news on devices with low performance, energy consumption, and temporary lack of access to global information networks.

### Structure
This repository consists of three subprojects:

- **API:** Contains code for the API implementation, allowing users to interact with the fake news detection system programmatically.
- **Model Train:** Includes code for training the machine learning models based on Naive Bayes, BM25, and TF-IDF algorithms for fake news detection.
- **Scrapper:** Contains code for web scraping, used to gather data from the internet for training and testing the fake news detection models.
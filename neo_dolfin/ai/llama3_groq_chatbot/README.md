# LLAMA3 70b Model Using Groq API

This branch contains the implementation of Meta's newest large language model, LLAMA3, 
This program uses the Groq API to create a simple chat assistant that responds to user input,
utilizing Meta's newest open source model, LLAMA3 70b, to generate responses.

With the help of Groq API, the time it takes for the model to generate a response is almost always **under half a second** (at the time of this implementation, 23 April 2024).

## Usage

To start testing the model using the .ipynb file in this directory,
you will have to obtain an API key from Groq. It is completely free.

 - Navigate to https://console.groq.com and create an account.

 - After creating an account, navigate to **API Keys** and create a new API key.

 - Paste your API key in the quoted section of PUT_YOUR_API_KEY_HERE.json file.

 - install Groq library: **pip install Groq**

 - Run the .ipynb file in Jupyter Lab / Notebook and you are good to go.

## Performance

Let's see what Samuel L. Jackson thinks about DolFin:

![image](https://github.com/DataBytes-Organisation/Neo_Dolfin/assets/111813260/a4119afa-8291-4550-bf0e-8e63c90936c9)


Impressive, considering it took him **less than 30ms** to think of an answer.

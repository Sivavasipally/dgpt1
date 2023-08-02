# Importing the necessary Python libraries
import os
import yaml
import openai
import gradio as gr
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.utilities import WikipediaAPIWrapper



## OPENAI API CONNECTION
## ---------------------------------------------------------------------------------------------------------------------
# Loading the API key and organization ID from file (NOT pushed to GitHub)
with open('openai-keys.yaml') as f:
    keys_yaml = yaml.safe_load(f)

# Setting the OpenAI API key as an environment variable
os.environ['OPENAI_API_KEY'] = keys_yaml['API_KEY']

# Using LangChain to connect to OpenAI
openai_llm = OpenAI()



## LANGCHAIN CONFIGURATION
## ---------------------------------------------------------------------------------------------------------------------
# Setting up the prompt template for retreiving the input customer's top 5 competitors
top_5_competitors_template = PromptTemplate(
    input_variables = ['customer_name'],
    template = 'Which 5 companies are {customer_name}\'s largest competitors? Give me a numbered list with a brief summary of the competitor\'s strategic advantage.'
)

# Setting up the prompt template for developing five business strategies for the input customer
top_5_strategies_template = PromptTemplate(
    input_variables = ['customer_name'],
    template = 'Give me five business strategies for {customer_name} to grow their business. Provide me the answer as a bulleted list with brief explanations around each strategy. Do not provide any text before the bulleted list and do not pad with newline characters.'
)

# Setting up the prompt template for generating five specific business actions around the first strategy generated from the previous prompt template
top_5_business_actions_template = PromptTemplate(
    input_variables = ['business_strategies'],
    template = 'From this list of business strategies:\n {business_strategies}\n Please develop 5 specific actions to take around the first strategy. Provide me the answer as a bulleted list with brief explanations for each action. Do not provide any text before the bulleted list and do not pad with newline characters.'
)

# Setting up the prompt template to retrieve a summary of the customer history from the Wikipedia information
customer_history_template = PromptTemplate(
    input_variables = ['wikipedia_information'],
    template = 'Please provide me a summary of the customer history from this body of Wikipedia information: {wikipedia_information}'
)

# Setting up the prompt template to re-write customer history as Jar Jar Binks from Star Wars
jar_jar_history_template = PromptTemplate(
    input_variables = ['customer_history'],
    template = 'Please re-write the following summary in the voice of Jar Jar Binks from Star Wars: {customer_history}. Do not add any newline characters at the beginning of your response.'
)

# Setting up the prompt template for generating a catchy jingle about the customer from its Wikipedia information
jingle_template = PromptTemplate(
    input_variables = ['customer_name', 'wikipedia_information'],
    template = 'Please write a catchy jingle for {customer_name}. Here is some additional information about the customer to help you write it: {wikipedia_information}. Do not show me the word "Jingle" at the beginning nor pad the beginning of your response with newline characters.'
)

# Setting up the prompt template to generate HTML code to create a simple website for displaying the customer's summary information
html_summary_template = PromptTemplate(
    input_variables = ['customer_history'],
    template = 'Please provide me HTML code to display a customer\'s historical summary. Give me only the HTML code and nothing else. Here is the historical summary for context: {customer_history}'
)

# Instantiating the LangChains for all the prompt templates defined above
top_5_competitors_chain      = LLMChain(llm = openai_llm, prompt = top_5_competitors_template, verbose = True, output_key = 'top_5_competitors')
top_5_strategies_chain       = LLMChain(llm = openai_llm, prompt = top_5_strategies_template, verbose = True, output_key = 'business_strategies')
top_5_business_actions_chain = LLMChain(llm = openai_llm, prompt = top_5_business_actions_template, verbose = True, output_key = 'business_actions')
customer_history_chain        = LLMChain(llm = openai_llm, prompt = customer_history_template, verbose = True, output_key = 'customer_history')
jar_jar_history_chain        = LLMChain(llm = openai_llm, prompt = jar_jar_history_template, verbose = True, output_key = 'jar_jar_history')
jingle_chain                 = LLMChain(llm = openai_llm, prompt = jingle_template, verbose = True, output_key = 'jingle')
html_summary_chain           = LLMChain(llm = openai_llm, prompt = html_summary_template, verbose = True, output_key = 'html_code_template')


# Instantiating an object to obtain results from the Wikipedia API
wikipedia_api = WikipediaAPIWrapper(top_k_results = 1)



def clear_results():
    '''
    Clears the results from the page

    Inputs:
        - customer_name (str): Name of the customer
        - top_5_competitors (str): A bulleted list of the top 5 competitors
        - business_strategies (str): A list of the top 5 business strategies
        - business_actions (str): A list of top 5 business actions to take against first business strategy defined
        - customer_history (str): History about the customer
        - jar_jar_history (str): History about the customer in the voice of Jar Jar Binks
        - jingle (str): A jingle written aboutt the customer
        - html_summary_code (str): Code written about the summary to be displayed in HTML

    Returns:
        - customer_name (str): Cleared out field ready for next customer
        - top_5_competitors (str): Cleared out field ready for next customer
        - business_strategies (str): Cleared out field ready for next customer
        - business_actions (str): Cleared out field ready for next customer
        - customer_history (str): Cleared out field ready for next customer
        - jar_jar_history (str): Cleared out field ready for next customer
        - jingle (str): Cleared out field ready for next customer
        - html_summary_code (str): Cleared out field ready for next customer
    '''

    # Clearing out the results for each field
    customer_name = ''
    top_5_competitors = ''
    business_strategies = ''
    business_actions = ''
    customer_history = ''
    jar_jar_history = ''
    jingle = ''
    html_summary_code = ''

    return customer_name, top_5_competitors, business_strategies, business_actions, customer_history, jar_jar_history, jingle, html_summary_code


## HELPER FUNCTIONS
## ---------------------------------------------------------------------------------------------------------------------
def generate_business_profile(customer_name_prompt):
    '''
    Generates the business profile for the inputted Fortune 500 customer

    Inputs:
        - customer_name_prompt (str): The name of the Fortune 500 customer submitted by the user

    Returns:
        - customer_name_prompt (str): The cleared out customer name ready to take in the next submission
    '''

    # Setting the name of the customer being profiled
    customer_name = customer_name_prompt

    # Retrieving information about the customer from Wikipedia
    wikipedia_information = wikipedia_api.run(f'{customer_name_prompt} (customer)')

    # Retrieving the list of top 5 competitors from OpenAI
    top_5_competitors = top_5_competitors_chain.run(customer_name_prompt)

    # Retrieving the top 5 strategies for the business from OpenAI
    business_strategies = top_5_strategies_chain.run(customer_name_prompt)

    # Retrieving the top 5 business actions per the strategies derived by OpenAI in the previous step
    business_actions = top_5_business_actions_chain.run(business_strategies)
    business_actions = f'For the first strategy listed in the previous box, here are five specific business actions to take to further that strategy:{business_actions}'

    # Retrieving a summary of the customer using the Wikipedia information
    customer_history = customer_history_chain.run(customer_name = customer_name_prompt, wikipedia_information = wikipedia_information)

    # Retrieving a re-written version of the customer history as Jar Jar Binks
    jar_jar_history = jar_jar_history_chain.run(customer_history)

    # Retrieving the jingle written by OpenAI using wikipedia information
    jingle = jingle_chain.run(customer_name = customer_name_prompt, wikipedia_information = wikipedia_information)

    # Retrieving an HTML code template to display the customer history
    html_summary_code = html_summary_chain.run(jar_jar_history)

    # Clearing out the customer name for the next run
    customer_name_prompt = ''

    return customer_name_prompt, customer_name, top_5_competitors, business_strategies, business_actions, customer_history, jar_jar_history, jingle, html_summary_code




## GRADIO UI LAYOUT & FUNCTIONALITY
## ---------------------------------------------------------------------------------------------------------------------
# Defining the building blocks that represent the form and function of the Gradio UI
with gr.Blocks(title = 'Customer Profiler', theme = 'base') as business_profiler:

    # Setting display into two columns
    with gr.Row():
        
        # Setting the display for the first column
        with gr.Column(scale = 1):

            # Displaying the header image
            #header_image = gr.Image('business_profiler.png', interactive = False, show_label = False)

            # Displaying the interactive text box to input the customer name
            customer_name_prompt = gr.Textbox(placeholder = 'Please type the name of the Customer you would like profiled.', label = 'Customer to Profile:')

            # Creating a button to clear the results
            clear_results_button = gr.Button('Clear Results')

        # Setting the display for the second column
        with gr.Column(scale = 5):

            # Displaying all the results appropriately
            customer_name = gr.Textbox(label = 'customer Name', interactive = False)
            top_5_competitors = gr.Textbox(label = 'Top 5 Competitors', interactive = False)
            business_strategies = gr.Textbox(label = 'Top 5 Business Stratgies', interactive = False)
            business_actions = gr.Textbox(label = 'Top 5 Business Actions to Support First Recommended Business Strategy', interactive = False)
            customer_history = gr.Textbox(label = 'customer History', interactive = False)
            jar_jar_history = gr.Textbox(label = 'customer History (Dictatated by Jar Jar Binks)', interactive = False)
            jingle = gr.Textbox(label = 'customer Jingle', interactive = False)
            html_summary_code = gr.Code(label = 'HTML Summary Code', language = 'html', interactive = False)

    # Defining the behavior for what occurs when the user hits "Enter" after typing a prompt
    customer_name_prompt.submit(fn = generate_business_profile,
                               inputs = [customer_name_prompt],
                               outputs = [customer_name_prompt, customer_name, top_5_competitors, business_strategies, business_actions, customer_history, jar_jar_history, jingle, html_summary_code])
    
    # Clearing out all results when the appropriate button is clicked
    clear_results_button.click(fn = clear_results, inputs = None, outputs = [customer_name, top_5_competitors, business_strategies, business_actions, customer_history, jar_jar_history, jingle, html_summary_code])
    



## SCRIPT INVOCATION
## ---------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":

    # Launching the Gradio interface
    business_profiler.launch()
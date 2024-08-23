import streamlit as st
import io
import time
import json
from openai.types.beta.threads.text_content_block import TextContentBlock
from openai.types.beta.threads.image_file_content_block import ImageFileContentBlock

from open_ai_api_calls import client, create_OpenAI_thread, create_OpenAI_message, run_OpenAI_thread, retrieve_OpenAI_run, retreive_OpenAI_messages

def extract_content(message):
    text = ''
    for content in message.content:
        if isinstance(content, TextContentBlock):
            text = content.text.value
            if content.text.annotations:
                for annotation in content.text.annotations:
                    text = text.replace(annotation.text, '')

        else:
            text = 'Oops! I am unable to process the content of this message.'
    return text

def calculate_cost(usage, session_id):
    print(usage)
    prompt_tokens = usage.prompt_tokens
    completion_tokens = usage.completion_tokens

    cost_USD = 0.15*prompt_tokens/1000000 + 0.6*completion_tokens/1000000

    # api_call_dict = {'env': st.secrets['env'], 'id': st.session_state['id'], 'page': page, 'session_id': session_id, 'prompt_tokens': prompt_tokens, 'completion_tokens': completion_tokens, 'cost_USD': cost_USD, 'model': model}
    # supabase_client.table('api_calls_open_ai_assistants').upsert(api_call_dict).execute()

    return cost_USD

def run_OpenAI_assistant(assistant_id, prompt, model='gpt-4o-mini', role='user', file_ids=[], metadata=None, thread_id=None, session_id=None, page=None):
    """
    Runs the OpenAI assistant with the given parameters.

    Args:
    - assistant_id (str): The ID of the OpenAI assistant to run.
    - prompt (str): The prompt to send to the OpenAI assistant.
    - role (str, optional): The role of the user sending the prompt. Defaults to 'user'.
    - file_ids (list, optional): A list of file IDs to send along with the prompt. Defaults to [].
    - metadata (dict, optional): A dictionary of metadata to send along with the prompt. Defaults to None.
    - thread_id (str, optional): The ID of the thread to send the prompt to. If None, a new thread will be created. Defaults to None.

    Returns:
    - list: A list containing the following elements:
      - text (str): The response text from the OpenAI assistant.
      - files (list): A list of files sent along with the response.
      - status (int): The status code of the response. 0 indicates success, while any other value indicates an error.
      - thread_id (str): The ID of the thread the prompt was sent to.
    """
    
    cost = 0
    tool_resources = {
        'file_search': {
            'vector_stores': [{'file_ids': file_ids}]
        }
    }

    if thread_id is None:
       thread_id = create_OpenAI_thread(tool_resources=tool_resources).id

    create_OpenAI_message(thread_id=thread_id, prompt=prompt, role=role, file_ids=file_ids, metadata=metadata)

    run = {'status': None}
    run = run_OpenAI_thread(thread_id=thread_id, assistant_id=assistant_id, model=model)

    run = retrieve_OpenAI_run(thread_id=thread_id, run_id=run.id)
    while run.status not in ['completed', 'failed', 'expired', 'cancelled']:
        if run.status in ['queued', 'in_progress', 'cancelling']:
            time.sleep(0.5)
            run = retrieve_OpenAI_run(thread_id=thread_id, run_id=run.id)
      
    if run.status == 'completed':
        cost = cost + calculate_cost(run.usage, session_id)
        raw_response = retreive_OpenAI_messages(thread_id=thread_id, limit=1)
        text = extract_content(message = raw_response.data[0])
        response = [text, cost, thread_id]

    if run.status in ['failed', 'expired', 'cancelled']:
        response = [run.status, cost, thread_id]

    return response
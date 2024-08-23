
import streamlit as st
from openai import OpenAI
from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential,
)

client = OpenAI()

def upload_file_OpenAI(file, purpose):
    """
    Upload a file to OpenAI.

    POST https://api.openai.com/v1/files

    This function uploads a file that can be used across various endpoints. The size of all the files uploaded by one organization can be up to 100 GB.
    The size of individual files can be a maximum of 512 MB. See the Assistants Tools guide to learn more about the types of files supported. The Fine-tuning API only supports .jsonl files.
    Please contact us if you need to increase these storage limits.

    Args:
        file (str): The File object (not file name) to be uploaded.
        purpose (str): The intended purpose of the uploaded file. Use "fine-tune" for Fine-tuning and "assistants" for Assistants and Messages. This allows us to validate the format of the uploaded file is correct for fine-tuning.

    Returns:
        The uploaded File object. The File object represents a document that has been uploaded to OpenAI. It includes the following attributes:
        - id (str): The file identifier, which can be referenced in the API endpoints.
        - bytes (int): The size of the file, in bytes.
        - created_at (int): The Unix timestamp (in seconds) for when the file was created.
        - filename (str): The name of the file.
        - object (str): The object type, which is always file.
        - purpose (str): The intended purpose of the file. Supported values are fine-tune, fine-tune-results, assistants, and assistants_output.
    """
    return client.files.create(file=file, purpose=purpose)


def create_OpenAI_assistant(model, name, description, instructions, tools, file_ids, metadata):
    """
    Creates an OpenAI assistant.

    Args:
        model (str): The model to use for the assistant.
        name (str): The name of the assistant.
        description (str): A description of the assistant.
        instructions (str): Instructions for the assistant.
        tools (list): A list of tools the assistant can use.
        file_ids (list): A list of file IDs the assistant can access.
        metadata (dict): Additional metadata for the assistant.

    Returns:
    dict: The created assistant. The dictionary includes the following keys:
        - id (str): The identifier of the assistant.
        - object (str): The object type, always "assistant".
        - created_at (int): The Unix timestamp for when the assistant was created.
        - name (str): The name of the assistant.
        - description (str): The description of the assistant.
        - model (str): ID of the model used.
        - instructions (str): The system instructions that the assistant uses.
        - tools (list): A list of tools enabled on the assistant.
        - file_ids (list): A list of file IDs attached to the assistant.
        - metadata (dict): Additional metadata for the assistant.
    """
    return client.beta.assistants.create(
        model=model,
        name=name,
        description=description,
        instructions=instructions,
        tools=tools,
        file_ids=file_ids,
        metadata=metadata
    )

def retrieve_OpenAI_assistant(assistant_id):
    """
    Retrieve the specified OpenAI assistant.

    Args:
        assistant_id (str): The ID of the assistant to retrieve.

    Returns:
    dict: The retreived assistant. The dictionary includes the following keys:
        - id (str): The identifier of the assistant.
        - object (str): The object type, always "assistant".
        - created_at (int): The Unix timestamp for when the assistant was created.
        - name (str): The name of the assistant.
        - description (str): The description of the assistant.
        - model (str): ID of the model used.
        - instructions (str): The system instructions that the assistant uses.
        - tools (list): A list of tools enabled on the assistant.
        - file_ids (list): A list of file IDs attached to the assistant.
        - metadata (dict): Additional metadata for the assistant.    
    """
    return client.beta.assistants.retrieve(assistant_id)

def create_OpenAI_thread(messages=None, tool_resources=None, metadata=None):
    """
    Create a new OpenAI thread.

    Args:
        messages (list, optional): A list of messages to be included in the thread. Each message is a dictionary that should include 'role', 'content', and 'created' fields.
        metadata (dict, optional): Additional metadata for the thread. This should be a dictionary where each key-value pair represents a metadata entry.

    Returns:
    dict: The created thread. The dictionary includes the following keys:
        - id (str): The identifier of the thread.
        - object (str): The object type, always "thread".
        - created_at (int): The Unix timestamp for when the thread was created.
        - messages (list): The list of messages in the thread. Each message is a dictionary.
        - metadata (dict): The metadata of the thread.
    """
    return client.beta.threads.create(messages=messages, tool_resources=tool_resources,  metadata=metadata)


def create_OpenAI_message(thread_id, role, prompt, file_ids=[], metadata=None):
    """
    Creates a message within a thread using OpenAI's API.

    Args:
        thread_id (str): The thread ID that this message belongs to.
        role (str): The entity that produced the message. One of 'user' or 'assistant'.
        prompt (str): The content of the message.
        file_ids (list, optional): A list of file IDs that the assistant should use. Defaults to [].
        metadata (dict, optional): Set of 16 key-value pairs that can be attached to an object. Defaults to None.

    Returns:
    dict: The message object which includes the following fields:
        - id (str): The identifier, which can be referenced in API endpoints.
        - object (str): The object type, which is always 'thread.message'.
        - created_at (int): The Unix timestamp (in seconds) for when the message was created.
        - thread_id (str): The thread ID that this message belongs to.
        - role (str): The entity that produced the message. One of 'user' or 'assistant'.
        - content (list): The content of the message in array of text and/or images.
        - assistant_id (str or None): If applicable, the ID of the assistant that authored this message.
        - run_id (str or None): If applicable, the ID of the run associated with the authoring of this message.
        - file_ids (list): A list of file IDs that the assistant should use.
        - metadata (dict): Set of 16 key-value pairs that can be attached to an object.
    """
    return client.beta.threads.messages.create(
        thread_id=thread_id,
        role=role,
        content=prompt,
        # file_ids=file_ids,
        metadata=metadata
    )

def retreive_OpenAI_messages(thread_id, limit=20, order='desc', after=None, before=None):
    """
    This function retrieves messages from a specific OpenAI thread.

    Args:
        thread_id (str): The ID of the thread to retrieve messages from.

    Returns:
    dict: The message object which includes the following fields:
        - id (str): The identifier, which can be referenced in API endpoints.
        - object (str): The object type, which is always 'thread.message'.
        - created_at (int): The Unix timestamp (in seconds) for when the message was created.
        - thread_id (str): The thread ID that this message belongs to.
        - role (str): The entity that produced the message. One of 'user' or 'assistant'.
        - content (list): The content of the message in array of text and/or images.
        - assistant_id (str or None): If applicable, the ID of the assistant that authored this message.
        - run_id (str or None): If applicable, the ID of the run associated with the authoring of this message.
        - file_ids (list): A list of file IDs that the assistant should use.
        - metadata (dict): Set of 16 key-value pairs that can be attached to an object.
    """
    return client.beta.threads.messages.list(
        thread_id=thread_id,
        limit=limit,
        order=order,
        after=after,
        before=before,
        )

def retrieve_OpenAI_message_file(thread_id, message_id, file_id):
    """
    Retrieves a message file from a specific thread and message.

    This function uses the OpenAI API to retrieve a file attached to a message in a thread.

    Args:
        thread_id (str): The ID of the thread to which the message and File belong.
        message_id (str): The ID of the message the file belongs to.
        file_id (str): The ID of the file being retrieved.

    Returns:
     dict: The message file object, which includes the following:
        - id (str): The identifier, which can be referenced in API endpoints.
        - object (str): The object type, which is always thread.message.file.
        - created_at (int): The Unix timestamp (in seconds) for when the message file was created.
        - message_id (str): The ID of the message that the File is attached to.
    """
    return client.beta.threads.messages.files.retrieve(
        thread_id=thread_id,
        message_id=message_id,
        file_id=file_id
    )

def run_OpenAI_thread(thread_id, assistant_id, model=None, instructions=None, tools=None, metadata=None, stream=False):
    """
    This function creates a new run in a specified thread using the OpenAI API.

    Parameters:
    thread_id (str): The ID of the thread.
    assistant_id (str): The ID of the assistant.
    model (str, optional): The model to be used. Defaults to None.
    instructions (str, optional): The instructions for the run. Defaults to None.
    tools (str, optional): The tools to be used. Defaults to None.
    metadata (str, optional): The metadata for the run. Defaults to None.

    Returns:
    dict: The response from the API call. The response is a dictionary representing a run object with the following keys:
        - id (str): The identifier of the run.
        - object (str): The object type, always 'thread.run'.
        - created_at (int): The Unix timestamp for when the run was created.
        - thread_id (str): The ID of the thread that was executed on as a part of this run.
        - assistant_id (str): The ID of the assistant used for execution of this run.
        - status (str): The status of the run.
        - required_action (dict or None): Details on the action required to continue the run.
        - last_error (dict or None): The last error associated with this run.
        - expires_at (int): The Unix timestamp for when the run will expire.
        - started_at (int or None): The Unix timestamp for when the run was started.
        - cancelled_at (int or None): The Unix timestamp for when the run was cancelled.
        - failed_at (int or None): The Unix timestamp for when the run failed.
        - completed_at (int or None): The Unix timestamp for when the run was completed.
        - model (str): The model that the assistant used for this run.
        - instructions (str): The instructions that the assistant used for this run.
        - tools (list): The list of tools that the assistant used for this run.
        - file_ids (list): The list of File IDs the assistant used for this run.
        - metadata (dict): Set of key-value pairs attached to the run.
    """
    return client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=assistant_id,
        model=model,
        instructions=instructions,
        tools=tools,
        metadata=metadata,
        stream=stream
    )

def submit_OpenAI_tool_output(thread_id, run_id, tool_outputs, stream=False):
    """
    This function submits tool outputs for a run using the OpenAI API.

    Parameters:
    thread_id (str): The ID of the thread.
    run_id (str): The ID of the run.
    tool_outputs (list): The list where each element is a JSON of tool outputs to be submitted.

    Returns:
    dict: The response from the API call. The response is a dictionary representing a run object with the following keys:
        - id (str): The identifier of the run.
        - object (str): The object type, always 'thread.run'.
        - created_at (int): The Unix timestamp for when the run was created.
        - thread_id (str): The ID of the thread that was executed on as a part of this run.
        - assistant_id (str): The ID of the assistant used for execution of this run.
        - status (str): The status of the run.
        - required_action (dict or None): Details on the action required to continue the run.
        - last_error (dict or None): The last error associated with this run.
        - expires_at (int): The Unix timestamp for when the run will expire.
        - started_at (int or None): The Unix timestamp for when the run was started.
        - cancelled_at (int or None): The Unix timestamp for when the run was cancelled.
        - failed_at (int or None): The Unix timestamp for when the run failed.
        - completed_at (int or None): The Unix timestamp for when the run was completed.
        - model (str): The model that the assistant used for this run.
        - instructions (str): The instructions that the assistant used for this run.
        - tools (list): The list of tools that the assistant used for this run.
        - file_ids (list): The list of File IDs the assistant used for this run.
        - metadata (dict): Set of key-value pairs attached to the run.
    """
    return client.beta.threads.runs.submit_tool_outputs(thread_id=thread_id, run_id=run_id, tool_outputs=tool_outputs, stream=stream)

def retrieve_OpenAI_run(thread_id, run_id):
    """
    Retrieve a specific run from a thread in OpenAI.

    Parameters:
    thread_id (str): The ID of the thread.
    run_id (str): The ID of the run.

    Returns:
    dict: The response from the API call. The response is a dictionary representing a run object with the following keys:
        - id (str): The identifier of the run.
        - object (str): The object type, always 'thread.run'.
        - created_at (int): The Unix timestamp for when the run was created.
        - thread_id (str): The ID of the thread that was executed on as a part of this run.
        - assistant_id (str): The ID of the assistant used for execution of this run.
        - status (str): The status of the run.
        - required_action (dict or None): Details on the action required to continue the run.
        - last_error (dict or None): The last error associated with this run.
        - expires_at (int): The Unix timestamp for when the run will expire.
        - started_at (int or None): The Unix timestamp for when the run was started.
        - cancelled_at (int or None): The Unix timestamp for when the run was cancelled.
        - failed_at (int or None): The Unix timestamp for when the run failed.
        - completed_at (int or None): The Unix timestamp for when the run was completed.
        - model (str): The model that the assistant used for this run.
        - instructions (str): The instructions that the assistant used for this run.
        - tools (list): The list of tools that the assistant used for this run.
        - file_ids (list): The list of File IDs the assistant used for this run.
        - metadata (dict): Set of key-value pairs attached to the run.
    """
    return client.beta.threads.runs.retrieve(
        thread_id=thread_id,
        run_id=run_id,
    )
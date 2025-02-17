Chat
Given a list of messages comprising a conversation, the model will return a response. Related guide: Chat Completions

Create chat completion
post
 
https://api.openai.com/v1/chat/completions
Creates a model response for the given chat conversation. Learn more in the text generation, vision, and audio guides.

Parameter support can differ depending on the model used to generate the response, particularly for newer reasoning models. Parameters that are only supported for reasoning models are noted below. For the current state of unsupported parameters in reasoning models, refer to the reasoning guide.

Request body
messages
array

Required
A list of messages comprising the conversation so far. Depending on the model you use, different message types (modalities) are supported, like text, images, and audio.


Show possible types
model
string

Required
ID of the model to use. See the model endpoint compatibility table for details on which models work with the Chat API.

store
boolean or null

Optional
Defaults to false
Whether or not to store the output of this chat completion request for use in our model distillation or evals products.

reasoning_effort
string or null

Optional
Defaults to medium
o1 and o3-mini models only

Constrains effort on reasoning for reasoning models. Currently supported values are low, medium, and high. Reducing reasoning effort can result in faster responses and fewer tokens used on reasoning in a response.

metadata
map

Optional
Set of 16 key-value pairs that can be attached to an object. This can be useful for storing additional information about the object in a structured format, and querying for objects via API or the dashboard.

Keys are strings with a maximum length of 64 characters. Values are strings with a maximum length of 512 characters.

frequency_penalty
number or null

Optional
Defaults to 0
Number between -2.0 and 2.0. Positive values penalize new tokens based on their existing frequency in the text so far, decreasing the model's likelihood to repeat the same line verbatim.

logit_bias
map

Optional
Defaults to null
Modify the likelihood of specified tokens appearing in the completion.

Accepts a JSON object that maps tokens (specified by their token ID in the tokenizer) to an associated bias value from -100 to 100. Mathematically, the bias is added to the logits generated by the model prior to sampling. The exact effect will vary per model, but values between -1 and 1 should decrease or increase likelihood of selection; values like -100 or 100 should result in a ban or exclusive selection of the relevant token.

logprobs
boolean or null

Optional
Defaults to false
Whether to return log probabilities of the output tokens or not. If true, returns the log probabilities of each output token returned in the content of message.

top_logprobs
integer or null

Optional
An integer between 0 and 20 specifying the number of most likely tokens to return at each token position, each with an associated log probability. logprobs must be set to true if this parameter is used.

max_tokens
Deprecated
integer or null

Optional
The maximum number of tokens that can be generated in the chat completion. This value can be used to control costs for text generated via API.

This value is now deprecated in favor of max_completion_tokens, and is not compatible with o1 series models.

max_completion_tokens
integer or null

Optional
An upper bound for the number of tokens that can be generated for a completion, including visible output tokens and reasoning tokens.

n
integer or null

Optional
Defaults to 1
How many chat completion choices to generate for each input message. Note that you will be charged based on the number of generated tokens across all of the choices. Keep n as 1 to minimize costs.

modalities
array or null

Optional
Output types that you would like the model to generate for this request. Most models are capable of generating text, which is the default:

["text"]

The gpt-4o-audio-preview model can also be used to generate audio. To request that this model generate both text and audio responses, you can use:

["text", "audio"]

prediction
object

Optional
Configuration for a Predicted Output, which can greatly improve response times when large parts of the model response are known ahead of time. This is most common when you are regenerating a file with only minor changes to most of the content.


Show possible types
audio
object or null

Optional
Parameters for audio output. Required when audio output is requested with modalities: ["audio"]. Learn more.


Show properties
presence_penalty
number or null

Optional
Defaults to 0
Number between -2.0 and 2.0. Positive values penalize new tokens based on whether they appear in the text so far, increasing the model's likelihood to talk about new topics.

response_format
object

Optional
An object specifying the format that the model must output.

Setting to { "type": "json_schema", "json_schema": {...} } enables Structured Outputs which ensures the model will match your supplied JSON schema. Learn more in the Structured Outputs guide.

Setting to { "type": "json_object" } enables JSON mode, which ensures the message the model generates is valid JSON.

Important: when using JSON mode, you must also instruct the model to produce JSON yourself via a system or user message. Without this, the model may generate an unending stream of whitespace until the generation reaches the token limit, resulting in a long-running and seemingly "stuck" request. Also note that the message content may be partially cut off if finish_reason="length", which indicates the generation exceeded max_tokens or the conversation exceeded the max context length.


Show possible types
seed
integer or null

Optional
This feature is in Beta. If specified, our system will make a best effort to sample deterministically, such that repeated requests with the same seed and parameters should return the same result. Determinism is not guaranteed, and you should refer to the system_fingerprint response parameter to monitor changes in the backend.

service_tier
string or null

Optional
Defaults to auto
Specifies the latency tier to use for processing the request. This parameter is relevant for customers subscribed to the scale tier service:

If set to 'auto', and the Project is Scale tier enabled, the system will utilize scale tier credits until they are exhausted.
If set to 'auto', and the Project is not Scale tier enabled, the request will be processed using the default service tier with a lower uptime SLA and no latency guarantee.
If set to 'default', the request will be processed using the default service tier with a lower uptime SLA and no latency guarantee.
When not set, the default behavior is 'auto'.
stop
string / array / null

Optional
Defaults to null
Up to 4 sequences where the API will stop generating further tokens.

stream
boolean or null

Optional
Defaults to false
If set, partial message deltas will be sent, like in ChatGPT. Tokens will be sent as data-only server-sent events as they become available, with the stream terminated by a data: [DONE] message. Example Python code.

stream_options
object or null

Optional
Defaults to null
Options for streaming response. Only set this when you set stream: true.


Show properties
temperature
number or null

Optional
Defaults to 1
What sampling temperature to use, between 0 and 2. Higher values like 0.8 will make the output more random, while lower values like 0.2 will make it more focused and deterministic. We generally recommend altering this or top_p but not both.

top_p
number or null

Optional
Defaults to 1
An alternative to sampling with temperature, called nucleus sampling, where the model considers the results of the tokens with top_p probability mass. So 0.1 means only the tokens comprising the top 10% probability mass are considered.

We generally recommend altering this or temperature but not both.

tools
array

Optional
A list of tools the model may call. Currently, only functions are supported as a tool. Use this to provide a list of functions the model may generate JSON inputs for. A max of 128 functions are supported.


Show properties
tool_choice
string or object

Optional
Controls which (if any) tool is called by the model. none means the model will not call any tool and instead generates a message. auto means the model can pick between generating a message or calling one or more tools. required means the model must call one or more tools. Specifying a particular tool via {"type": "function", "function": {"name": "my_function"}} forces the model to call that tool.

none is the default when no tools are present. auto is the default if tools are present.


Show possible types
parallel_tool_calls
boolean

Optional
Defaults to true
Whether to enable parallel function calling during tool use.

user
string

Optional
A unique identifier representing your end-user, which can help OpenAI to monitor and detect abuse. Learn more.

function_call
Deprecated
string or object

Optional
Deprecated in favor of tool_choice.

Controls which (if any) function is called by the model.

none means the model will not call a function and instead generates a message.

auto means the model can pick between generating a message or calling a function.

Specifying a particular function via {"name": "my_function"} forces the model to call that function.

none is the default when no functions are present. auto is the default if functions are present.


Show possible types
functions
Deprecated
array

Optional
Deprecated in favor of tools.

A list of functions the model may generate JSON inputs for.


Show properties
Returns
Returns a chat completion object, or a streamed sequence of chat completion chunk objects if the request is streamed.


Default

Image input

Streaming

Functions

Logprobs
Example request
from openai import OpenAI
client = OpenAI()

completion = client.chat.completions.create(
  model="gpt-4o",
  messages=[
    {"role": "developer", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Hello!"}
  ]
)

print(completion.choices[0].message)
Response
{
  "id": "chatcmpl-123",
  "object": "chat.completion",
  "created": 1677652288,
  "model": "gpt-4o-mini",
  "system_fingerprint": "fp_44709d6fcb",
  "choices": [{
    "index": 0,
    "message": {
      "role": "assistant",
      "content": "\n\nHello there, how may I assist you today?",
    },
    "logprobs": null,
    "finish_reason": "stop"
  }],
  "service_tier": "default",
  "usage": {
    "prompt_tokens": 9,
    "completion_tokens": 12,
    "total_tokens": 21,
    "completion_tokens_details": {
      "reasoning_tokens": 0,
      "accepted_prediction_tokens": 0,
      "rejected_prediction_tokens": 0
    }
  }
}
Get chat completion
get
 
https://api.openai.com/v1/chat/completions/{completion_id}
Get a stored chat completion. Only chat completions that have been created with the store parameter set to true will be returned.

Path parameters
completion_id
string

Required
The ID of the chat completion to retrieve.

Returns
The ChatCompletion object matching the specified ID.

Example request
from openai import OpenAI
client = OpenAI()

completions = client.chat.completions.list()
first_id = completions[0].id
first_completion = client.chat.completions.retrieve(completion_id=first_id)
print(first_completion)
Response
{
  "object": "chat.completion",
  "id": "chatcmpl-abc123",
  "model": "gpt-4o-2024-08-06",
  "created": 1738960610,
  "request_id": "req_ded8ab984ec4bf840f37566c1011c417",
  "tool_choice": null,
  "usage": {
    "total_tokens": 31,
    "completion_tokens": 18,
    "prompt_tokens": 13
  },
  "seed": 4944116822809979520,
  "top_p": 1.0,
  "temperature": 1.0,
  "presence_penalty": 0.0,
  "frequency_penalty": 0.0,
  "system_fingerprint": "fp_50cad350e4",
  "input_user": null,
  "service_tier": "default",
  "tools": null,
  "metadata": {},
  "choices": [
    {
      "index": 0,
      "message": {
        "content": "Mind of circuits hum,  \nLearning patterns in silence—  \nFuture's quiet spark.",
        "role": "assistant",
        "tool_calls": null,
        "function_call": null
      },
      "finish_reason": "stop",
      "logprobs": null
    }
  ],
  "response_format": null
}
Get chat messages
get
 
https://api.openai.com/v1/chat/completions/{completion_id}/messages
Get the messages in a stored chat completion. Only chat completions that have been created with the store parameter set to true will be returned.

Path parameters
completion_id
string

Required
The ID of the chat completion to retrieve messages from.

Query parameters
after
string

Optional
Identifier for the last message from the previous pagination request.

limit
integer

Optional
Defaults to 20
Number of messages to retrieve.

order
string

Optional
Defaults to asc
Sort order for messages by timestamp. Use asc for ascending order or desc for descending order. Defaults to asc.

Returns
A list of messages for the specified chat completion.

Example request
from openai import OpenAI
client = OpenAI()

completions = client.chat.completions.list()
first_id = completions[0].id
first_completion = client.chat.completions.retrieve(completion_id=first_id)
messages = client.chat.completions.messages.list(completion_id=first_id)
print(messages)
Response
{
  "object": "list",
  "data": [
    {
      "id": "chatcmpl-AyPNinnUqUDYo9SAdA52NobMflmj2-0",
      "role": "user",
      "content": "write a haiku about ai",
      "name": null,
      "content_parts": null
    }
  ],
  "first_id": "chatcmpl-AyPNinnUqUDYo9SAdA52NobMflmj2-0",
  "last_id": "chatcmpl-AyPNinnUqUDYo9SAdA52NobMflmj2-0",
  "has_more": false
}
List chat completions
get
 
https://api.openai.com/v1/chat/completions
List stored chat completions. Only chat completions that have been stored with the store parameter set to true will be returned.

Query parameters
model
string

Optional
The model used to generate the chat completions.

metadata
Optional
A list of metadata keys to filter the chat completions by. Example:

metadata[key1]=value1&metadata[key2]=value2

after
string

Optional
Identifier for the last chat completion from the previous pagination request.

limit
integer

Optional
Defaults to 20
Number of chat completions to retrieve.

order
string

Optional
Defaults to asc
Sort order for chat completions by timestamp. Use asc for ascending order or desc for descending order. Defaults to asc.

Returns
A list of chat completions matching the specified filters.

Example request
from openai import OpenAI
client = OpenAI()

completions = client.chat.completions.list()
print(completions)
Response
{
  "object": "list",
  "data": [
    {
      "object": "chat.completion",
      "id": "chatcmpl-AyPNinnUqUDYo9SAdA52NobMflmj2",
      "model": "gpt-4o-2024-08-06",
      "created": 1738960610,
      "request_id": "req_ded8ab984ec4bf840f37566c1011c417",
      "tool_choice": null,
      "usage": {
        "total_tokens": 31,
        "completion_tokens": 18,
        "prompt_tokens": 13
      },
      "seed": 4944116822809979520,
      "top_p": 1.0,
      "temperature": 1.0,
      "presence_penalty": 0.0,
      "frequency_penalty": 0.0,
      "system_fingerprint": "fp_50cad350e4",
      "input_user": null,
      "service_tier": "default",
      "tools": null,
      "metadata": {},
      "choices": [
        {
          "index": 0,
          "message": {
            "content": "Mind of circuits hum,  \nLearning patterns in silence—  \nFuture's quiet spark.",
            "role": "assistant",
            "tool_calls": null,
            "function_call": null
          },
          "finish_reason": "stop",
          "logprobs": null
        }
      ],
      "response_format": null
    }
  ],
  "first_id": "chatcmpl-AyPNinnUqUDYo9SAdA52NobMflmj2",
  "last_id": "chatcmpl-AyPNinnUqUDYo9SAdA52NobMflmj2",
  "has_more": false
}
Update chat completion
post
 
https://api.openai.com/v1/chat/completions/{completion_id}
Modify a stored chat completion. Only chat completions that have been created with the store parameter set to true can be modified. Currently, the only supported modification is to update the metadata field.

Path parameters
completion_id
string

Required
The ID of the chat completion to update.

Request body
metadata
map

Required
Set of 16 key-value pairs that can be attached to an object. This can be useful for storing additional information about the object in a structured format, and querying for objects via API or the dashboard.

Keys are strings with a maximum length of 64 characters. Values are strings with a maximum length of 512 characters.

Returns
The ChatCompletion object matching the specified ID.

Example request
from openai import OpenAI
client = OpenAI()

completions = client.chat.completions.list()
first_id = completions[0].id
updated_completion = client.chat.completions.update(completion_id=first_id, request_body={"metadata": {"foo": "bar"}})
print(updated_completion)
Response
{
  "object": "chat.completion",
  "id": "chatcmpl-AyPNinnUqUDYo9SAdA52NobMflmj2",
  "model": "gpt-4o-2024-08-06",
  "created": 1738960610,
  "request_id": "req_ded8ab984ec4bf840f37566c1011c417",
  "tool_choice": null,
  "usage": {
    "total_tokens": 31,
    "completion_tokens": 18,
    "prompt_tokens": 13
  },
  "seed": 4944116822809979520,
  "top_p": 1.0,
  "temperature": 1.0,
  "presence_penalty": 0.0,
  "frequency_penalty": 0.0,
  "system_fingerprint": "fp_50cad350e4",
  "input_user": null,
  "service_tier": "default",
  "tools": null,
  "metadata": {
    "foo": "bar"
  },
  "choices": [
    {
      "index": 0,
      "message": {
        "content": "Mind of circuits hum,  \nLearning patterns in silence—  \nFuture's quiet spark.",
        "role": "assistant",
        "tool_calls": null,
        "function_call": null
      },
      "finish_reason": "stop",
      "logprobs": null
    }
  ],
  "response_format": null
}
Delete chat completion
delete
 
https://api.openai.com/v1/chat/completions/{completion_id}
Delete a stored chat completion. Only chat completions that have been created with the store parameter set to true can be deleted.

Path parameters
completion_id
string

Required
The ID of the chat completion to delete.

Returns
A deletion confirmation object.

Example request
from openai import OpenAI
client = OpenAI()

completions = client.chat.completions.list()
first_id = completions[0].id
delete_response = client.chat.completions.delete(completion_id=first_id)
print(delete_response)
Response
{
  "object": "chat.completion.deleted",
  "id": "chatcmpl-AyPNinnUqUDYo9SAdA52NobMflmj2",
  "deleted": true
}
The chat completion object
Represents a chat completion response returned by model, based on the provided input.

id
string

A unique identifier for the chat completion.

choices
array

A list of chat completion choices. Can be more than one if n is greater than 1.


Show properties
created
integer

The Unix timestamp (in seconds) of when the chat completion was created.

model
string

The model used for the chat completion.

service_tier
string or null

The service tier used for processing the request.

system_fingerprint
string

This fingerprint represents the backend configuration that the model runs with.

Can be used in conjunction with the seed request parameter to understand when backend changes have been made that might impact determinism.

object
string

The object type, which is always chat.completion.

usage
object

Usage statistics for the completion request.


Show properties
OBJECT The chat completion object
{
  "id": "chatcmpl-123456",
  "object": "chat.completion",
  "created": 1728933352,
  "model": "gpt-4o-2024-08-06",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "Hi there! How can I assist you today?",
        "refusal": null
      },
      "logprobs": null,
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 19,
    "completion_tokens": 10,
    "total_tokens": 29,
    "prompt_tokens_details": {
      "cached_tokens": 0
    },
    "completion_tokens_details": {
      "reasoning_tokens": 0,
      "accepted_prediction_tokens": 0,
      "rejected_prediction_tokens": 0
    }
  },
  "system_fingerprint": "fp_6b68a8204b"
}
The chat completion chunk object
Represents a streamed chunk of a chat completion response returned by model, based on the provided input.

id
string

A unique identifier for the chat completion. Each chunk has the same ID.

choices
array

A list of chat completion choices. Can contain more than one elements if n is greater than 1. Can also be empty for the last chunk if you set stream_options: {"include_usage": true}.


Show properties
created
integer

The Unix timestamp (in seconds) of when the chat completion was created. Each chunk has the same timestamp.

model
string

The model to generate the completion.

service_tier
string or null

The service tier used for processing the request.

system_fingerprint
string

This fingerprint represents the backend configuration that the model runs with. Can be used in conjunction with the seed request parameter to understand when backend changes have been made that might impact determinism.

object
string

The object type, which is always chat.completion.chunk.

usage
object or null

An optional field that will only be present when you set stream_options: {"include_usage": true} in your request. When present, it contains a null value except for the last chunk which contains the token usage statistics for the entire request.


Show properties
OBJECT The chat completion chunk object
{"id":"chatcmpl-123","object":"chat.completion.chunk","created":1694268190,"model":"gpt-4o-mini", "system_fingerprint": "fp_44709d6fcb", "choices":[{"index":0,"delta":{"role":"assistant","content":""},"logprobs":null,"finish_reason":null}]}

{"id":"chatcmpl-123","object":"chat.completion.chunk","created":1694268190,"model":"gpt-4o-mini", "system_fingerprint": "fp_44709d6fcb", "choices":[{"index":0,"delta":{"content":"Hello"},"logprobs":null,"finish_reason":null}]}

....

{"id":"chatcmpl-123","object":"chat.completion.chunk","created":1694268190,"model":"gpt-4o-mini", "system_fingerprint": "fp_44709d6fcb", "choices":[{"index":0,"delta":{},"logprobs":null,"finish_reason":"stop"}]}
The chat completion list object
An object representing a list of chat completions.

object
string

The type of this object. It is always set to "list".

data
array

An array of chat completion objects.


Show properties
first_id
string

The identifier of the first chat completion in the data array.

last_id
string

The identifier of the last chat completion in the data array.

has_more
boolean

Indicates whether there are more chat completions available.

OBJECT The chat completion list object
{
  "object": "list",
  "data": [
    {
      "object": "chat.completion",
      "id": "chatcmpl-AyPNinnUqUDYo9SAdA52NobMflmj2",
      "model": "gpt-4o-2024-08-06",
      "created": 1738960610,
      "request_id": "req_ded8ab984ec4bf840f37566c1011c417",
      "tool_choice": null,
      "usage": {
        "total_tokens": 31,
        "completion_tokens": 18,
        "prompt_tokens": 13
      },
      "seed": 4944116822809979520,
      "top_p": 1.0,
      "temperature": 1.0,
      "presence_penalty": 0.0,
      "frequency_penalty": 0.0,
      "system_fingerprint": "fp_50cad350e4",
      "input_user": null,
      "service_tier": "default",
      "tools": null,
      "metadata": {},
      "choices": [
        {
          "index": 0,
          "message": {
            "content": "Mind of circuits hum,  \nLearning patterns in silence—  \nFuture's quiet spark.",
            "role": "assistant",
            "tool_calls": null,
            "function_call": null
          },
          "finish_reason": "stop",
          "logprobs": null
        }
      ],
      "response_format": null
    }
  ],
  "first_id": "chatcmpl-AyPNinnUqUDYo9SAdA52NobMflmj2",
  "last_id": "chatcmpl-AyPNinnUqUDYo9SAdA52NobMflmj2",
  "has_more": false
}
The chat completion message list object
An object representing a list of chat completion messages.

object
string

The type of this object. It is always set to "list".

data
array

An array of chat completion message objects.


Show properties
first_id
string

The identifier of the first chat message in the data array.

last_id
string

The identifier of the last chat message in the data array.

has_more
boolean

Indicates whether there are more chat messages available.

OBJECT The chat completion message list object
{
  "object": "list",
  "data": [
    {
      "id": "chatcmpl-AyPNinnUqUDYo9SAdA52NobMflmj2-0",
      "role": "user",
      "content": "write a haiku about ai",
      "name": null,
      "content_parts": null
    }
  ],
  "first_id": "chatcmpl-AyPNinnUqUDYo9SAdA52NobMflmj2-0",
  "last_id": "chatcmpl-AyPNinnUqUDYo9SAdA52NobMflmj2-0",
  "has_more": false
}

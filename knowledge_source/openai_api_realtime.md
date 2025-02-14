```markdown
# Realtime API Documentation

## Overview

**Realtime** (Beta) enables communication with a GPT-4o class model in real time using WebRTC or WebSockets. It supports both text and audio inputs and outputs, along with audio transcriptions.  
[Learn more about the Realtime API](#).

---

## Session Tokens

This endpoint generates ephemeral session tokens for use in client-side applications.

---

## Create Session

### HTTP Request

```
POST https://api.openai.com/v1/realtime/sessions
```

### Description

Creates an ephemeral API token for use in client-side applications with the Realtime API. It can be configured with the same session parameters as the `session.update` client event. The response includes a session object and a `client_secret` key, which contains a usable ephemeral API token that can be used to authenticate browser clients for the Realtime API.

---

### Request Body Parameters

- **modalities** (Optional)  
  The set of modalities the model can respond with.  
  To disable audio, set this to `["text"]`.

- **model** (string, Optional)  
  The Realtime model used for this session.

- **instructions** (string, Optional)  
  The default system instructions (i.e. system message) that will be prepended to model calls. This field guides the model on desired responses.  
  For example:  
  - "be extremely succinct"  
  - "act friendly"  
  - "here are examples of good responses"  
  - "talk quickly", "inject emotion into your voice", "laugh frequently"  

  **Note:** The server sets default instructions if this field is not provided, and these defaults are visible in the `session.created` event at the start of the session.

- **voice** (string, Optional)  
  The voice the model uses to respond.  
  **Important:** The voice cannot be changed during the session once the model has responded with audio at least once.  
  Current voice options include: `alloy`, `ash`, `ballad`, `coral`, `echo sage`, `shimmer`, and `verse`.

- **input_audio_format** (string, Optional)  
  The format of input audio. Options are: `pcm16`, `g711_ulaw`, or `g711_alaw`.  
  For `pcm16`, input audio must be:
  - 16-bit PCM
  - 24kHz sample rate
  - Single channel (mono)
  - Little-endian byte order

- **output_audio_format** (string, Optional)  
  The format of output audio. Options are: `pcm16`, `g711_ulaw`, or `g711_alaw`.  
  For `pcm16`, output audio is sampled at a rate of 24kHz.

- **input_audio_transcription** (object, Optional)  
  Configuration for input audio transcription.  
  Defaults to off and can be set to `null` to disable once enabled.  
  **Note:** Input audio transcription is not native to the model since the model consumes audio directly.  
  Transcription runs asynchronously through OpenAI Whisper transcription and should be treated as rough guidance rather than an exact representation of what the model understands.  
  The client can optionally set the language and prompt for transcription; these fields will be passed to the Whisper API.

- **turn_detection** (object, Optional)  
  Configuration for turn detection.  
  Can be set to `null` to disable.  
  **Note:** Server VAD (Voice Activity Detection) means that the model will detect the start and end of speech based on audio volume and respond at the end of user speech.

- **tools** (array, Optional)  
  Tools (functions) available to the model.

- **tool_choice** (string, Optional)  
  How the model chooses tools. Options are:
  - `auto`
  - `none`
  - `required`
  - `specify a function`

- **temperature** (number, Optional)  
  Sampling temperature for the model, limited to the range `[0.6, 1.2]`.  
  Defaults to `0.8`.

- **max_response_output_tokens** (integer or `"inf"`, Optional)  
  Maximum number of output tokens for a single assistant response, inclusive of tool calls.  
  Provide an integer between `1` and `4096` to limit output tokens, or `"inf"` for the maximum available tokens for the given model.  
  Defaults to `"inf"`.

---

### Example Request

```bash
curl -X POST https://api.openai.com/v1/realtime/sessions \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-4o-realtime-preview-2024-12-17",
    "modalities": ["audio", "text"],
    "instructions": "You are a friendly assistant."
  }'
```

---

### Response

The API responds with the created Realtime session object, including an ephemeral key.

```json
{
  "id": "sess_001",
  "object": "realtime.session",
  "model": "gpt-4o-realtime-preview-2024-12-17",
  "modalities": ["audio", "text"],
  "instructions": "You are a friendly assistant.",
  "voice": "alloy",
  "input_audio_format": "pcm16",
  "output_audio_format": "pcm16",
  "input_audio_transcription": {
      "model": "whisper-1"
  },
  "turn_detection": null,
  "tools": [],
  "tool_choice": "none",
  "temperature": 0.7,
  "max_response_output_tokens": 200,
  "client_secret": {
    "value": "ek_abc123", 
    "expires_at": 1234567890
  }
}
```

---

## Session Object Properties

- **client_secret** (object)  
  The ephemeral key returned by the API.

- **modalities** (array)  
  The set of modalities the model can respond with.  
  *Tip:* To disable audio, set this to `["text"]`.

- **instructions** (string)  
  The default system instructions (i.e., system message) that are prepended to model calls.  
  This field guides the model on desired responses and behavior.  
  *Note:* If not provided, the server defaults will be used and displayed in the `session.created` event.

- **voice** (string)  
  The voice the model uses to respond.  
  *Note:* The voice cannot be changed once the model has started responding with audio.  
  Available options include: `alloy`, `ash`, `ballad`, `coral`, `echo sage`, `shimmer`, and `verse`.

- **input_audio_format** (string)  
  The format for input audio.  
  Options: `pcm16`, `g711_ulaw`, or `g711_alaw`.

- **output_audio_format** (string)  
  The format for output audio.  
  Options: `pcm16`, `g711_ulaw`, or `g711_alaw`.

- **input_audio_transcription** (object)  
  Configuration for input audio transcription.  
  Defaults to off and can be set to `null` to disable after being enabled.  
  **Note:** Transcription is performed asynchronously through Whisper.

- **turn_detection** (object)  
  Configuration for turn detection.  
  Can be set to `null` to disable.  
  **Note:** With server VAD, the model detects the beginning and end of speech based on audio volume and responds after the user's speech ends.

- **tools** (array)  
  Tools (functions) available to the model.

- **tool_choice** (string)  
  Defines how the model selects tools. Options are:
  - `auto`
  - `none`
  - `required`
  - `specify a function`

- **temperature** (number)  
  The sampling temperature for the model, ranging from `0.6` to `1.2`.  
  Defaults to `0.8`.

- **max_response_output_tokens** (integer or `"inf"`)  
  Maximum number of output tokens for a single assistant response, inclusive of tool calls.  
  Set an integer between `1` and `4096` or `"inf"` for the maximum tokens available for the model.  
  Defaults to `"inf"`.

---

## Complete Session Object Example

```json
{
  "id": "sess_001",
  "object": "realtime.session",
  "model": "gpt-4o-realtime-preview-2024-12-17",
  "modalities": ["audio", "text"],
  "instructions": "You are a friendly assistant.",
  "voice": "alloy",
  "input_audio_format": "pcm16",
  "output_audio_format": "pcm16",
  "input_audio_transcription": {
      "model": "whisper-1"
  },
  "turn_detection": null,
  "tools": [],
  "tool_choice": "none",
  "temperature": 0.7,
  "max_response_output_tokens": 200,
  "client_secret": {
    "value": "ek_abc123", 
    "expires_at": 1234567890
  }
}
```
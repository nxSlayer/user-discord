def StartSocket(token):
  return {
      "op": 2,
      "d": {
          "token": token,
          "capabilities": 8189,
          "properties": {
              "os": "Windows",
              "browser": "Chrome",
              "device": "",
              "system_locale": "pt-BR",
              "browser_user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
              "browser_version": "114.0.0.0",
              "os_version": "10",
              "referrer": "",
              "referring_domain": "",
              "referrer_current": "",
              "referring_domain_current": "",
              "release_channel": "stable",
              "client_build_number": 208319,
              "client_event_source": None
          }
      }
  }



def ReplyMessage(channel_id, message_id, content, nonce):
    return {
      "content": content,
      "nonce": nonce,
      "tts": False,
      "message_reference": {
          "channel_id": channel_id,
          "message_id": message_id
      },
      "flags": 0
  }


def FormatEvent(event):
  samples = {"message": "MESSAGE_CREATE", "ready": "READY"}
  if samples.get(event):
    return samples[event]
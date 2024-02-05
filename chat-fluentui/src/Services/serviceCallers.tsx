import { ChatMessage } from '../Interfaces/iprompt';
import config from "../config.json";

let streamReader: ReadableStreamDefaultReader<Uint8Array>;

//const backendAPIHost = "http://localhost:5000";
const backendAPIHost = config.backendAPIHost;

export const cancelStream = (onDataReceived:any) => {
    if (streamReader) {
      streamReader.cancel().then(() => {
        onDataReceived("");
      }).catch(error => {
        console.error("Error cancelling the stream:", error);
      });
    }
}

export const getDocList = (onDataReceived:any) => {
  const postPayLoad = {
      method: "GET",
      headers: { 'Content-Type': 'application/json' }
  };

  fetch(`${backendAPIHost}/chat/doclist`, postPayLoad)
  .then(response => {
    return response.text();
  })
  .then(data => {
    onDataReceived(data);
  })
  .then(text => {
    //console.log(text); // Here you can process your text data
    // If the server sends JSON strings, you can parse them here
    // const data = JSON.parse(text);
    // Process the data...
  })
  .catch(error => {
    console.error("Stream failed:", error);
    onDataReceived("Error occurred while sending message.");
    return {
      "api": "getDocList",
      "method": "GET",
      "status": "error",
      "chatHistory": null,
      "message": error.toString() + "\n\n Please check if bot api is running."
    };
  });
}

export const getGreetings = (onDataReceived:any) => {
    const postPayLoad = {
        method: "GET",
        headers: { 'Content-Type': 'application/json' }
    };

    fetch(`${backendAPIHost}/chat/greeting`, postPayLoad)
    .then(response => {
      return response.text();
    })
    .then(data => {
      onDataReceived(data);
    })
    .then(text => {
      //console.log(text); // Here you can process your text data
      // If the server sends JSON strings, you can parse them here
      // const data = JSON.parse(text);
      // Process the data...
    })
    .catch(error => {
      console.error("Stream failed:", error);
      onDataReceived("Error occurred while sending message.");
      return {
        "api": "getGreetings",
        "method": "GET",
        "status": "error",
        "chatHistory": null,
        "message": error.toString() + "\n\n Please check if bot api is running."
      };
    });
}

export const sendMessage = (userQuery: string, chatMessage: ChatMessage, onDataReceived:any, queryCategory?: string) => {

    if (userQuery === '') {
        return;
    }

    const apiRequest = {"userMessage": userQuery, 
                        "queue_name": chatMessage?.queue_name, 
                        "query_category": queryCategory,
                        "use_streaming": chatMessage?.use_streaming}

    const postPayLoad = {
        method: "POST",
        //headers: { 'Content-Type': 'application/json', 'Authorization': bearer },
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(apiRequest)
    };


    fetch(`${backendAPIHost}/chat/conversation`, postPayLoad)
    .then(response => {
      return response.text();
      
    })
    .then(data => {
      onDataReceived(data);
    })
    .then(text => {
      //console.log(text); // Here you can process your text data
      // If the server sends JSON strings, you can parse them here
      // const data = JSON.parse(text);
      // Process the data...
    })
    .catch(error => {
      console.error("Stream failed:", error);
      onDataReceived("Error occurred while sending message.");
      return {
        "api": "send_chat",
        "method": "POST",
        "status": "error",
        "chatHistory": null,
        "message": error.toString() + "\n\n Please check if bot api is running."
      };
    });
}


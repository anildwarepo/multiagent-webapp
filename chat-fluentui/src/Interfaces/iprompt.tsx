
export interface AIChartComponentProps {
    ChartData: ChartDataProps;
}
  
export interface ChartDataProps {
    data: any[];
    layout: any;
    dataAnalysis: any;
}
export interface Chat {
    userType: string;
    userMessage: string;
    chartData?: ChartDataProps;
}

export interface ChatMessage {
    message: string;
    connection_id: string;
    queue_name: string;
    connection_status: string;
    use_streaming: boolean;
}

export interface ChatAPIRequest {

        gptPrompt: GptPrompt;
        maxTokens: number;
        topKSearchResults: number;
        numChunk: number;
        temperature: number;
        includeChatHistory: boolean;
        useSearchEngine: boolean;
        useVectorCache: boolean;
        chatHistoryCount: number;
        chatHistory:string,
        userInfo : UserInfo
}


export interface UserInfo {
    name: string; 
    email: string; 
    tenantId: string;
}

export interface GptPrompt {
    
    systemMessage : Prompt;
    question : Prompt;    
}

export interface Prompt {

    role: string;
    content: string;
}


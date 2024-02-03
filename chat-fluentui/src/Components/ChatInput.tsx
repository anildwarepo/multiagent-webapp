import {
    useId,
    Label,
    Textarea,
    TextareaProps,
    Divider
} from "@fluentui/react-components";
import { DefaultPalette } from '@fluentui/react/lib/Styling';
import { Stack } from "@fluentui/react";
import * as Styles from "./styles";
import { useRef, useState, useEffect } from 'react';
import { ChatMessage, Chat } from '../Interfaces/iprompt';
import { sendMessage, cancelStream, getGreetings } from '../Services/serviceCallers';
import ReactMarkdown from 'react-markdown';
import AIChartComponent from "./AIChartComponent";
import { Person24Filled, Bot24Filled, Send24Filled, Send24Regular, RecordStop24Filled, RecordStop24Regular } from '@fluentui/react-icons';
import { Text } from '@fluentui/react';
import SkeletonComponent from "./SkeletonComponent";

interface ChatInputComponentProps extends Partial<TextareaProps> {
    faq: string;
    queryCategory: string;
    setFAQ?: (query: string, queryCategory: string) => void;
}

const ChatInputComponent: React.FC<ChatInputComponentProps>  = ({faq, queryCategory, ...props}) => {
    //function ChatInputComponent(props: Partial<TextareaProps>) {
    const textareaId = useId("textarea");
    const [userQuery, setUserQuery] = useState('');
    const [isSending, setIsSending] = useState(false);
    const [chatHistory, setChatHistory] = useState<Chat[]>([]);
    const divRef = useRef<null | HTMLDivElement>(null);
    const textareaRef = useRef<HTMLTextAreaElement>(null);
    const [chatMessage] = useState<ChatMessage | null>(null);
    const [isHovered, setIsHovered] = useState(false);
    const handleMouseEnter = () => setIsHovered(true);
    const handleMouseLeave = () => setIsHovered(false);


    useEffect(() => {
        setUserQuery(faq ?? '');
        updateChatHistory(faq, chatMessage as ChatMessage, queryCategory)
    }, [faq]); 

    useEffect(() => {
        divRef.current?.scrollIntoView({ inline: 'nearest', block: 'start', behavior: 'smooth' });
    }, [chatHistory]);

    useEffect(() => {
        const botItem = { userType: "system", userMessage: "" };
        let userItems = [...chatHistory, botItem];
        setChatHistory(userItems);
        setIsSending(true);
        getGreetings(handleMessage);
        setIsSending(false);
    }, []); // Empty dependency array means this runs once on mount

    
    const cancelResponse = () => {
        setIsSending(false);
        cancelStream(handleMessage);
        textareaRef.current?.focus();
    }
    const handleUserQueryChange = (e: any) => {
        console.log("handleUserQueryChange: " + e.target.value);
        setUserQuery(e.target.value);
    }

    const handleUserQuery = (e: any) => {
        if (e.key === 'Enter') {
            console.log("Enter pressed - " + userQuery)
            e.preventDefault();
            updateChatHistory(userQuery, chatMessage as ChatMessage)
            //setUserQuery('');            
        }
        if (e.type === 'click') {
            console.log("button clicked - " + userQuery)
            updateChatHistory(userQuery, chatMessage as ChatMessage)
        }
    }

    const autoResize = (e: any) => {
        e.target.style.height = 'inherit';
        e.target.style.height = `${e.target.scrollHeight}px`;
    };


    const handleMessage = (newData: any) => {
        setIsSending(false);
        if (newData.includes("CONV_END") || newData.includes("TERMINATE") || newData.includes("```json") || newData.includes("```")) {
            newData = newData.replace("CONV_END", "");
            newData = newData.replace("TERMINATE", "");
            newData = newData.replace("```json", "");
            newData = newData.replace("```", "");

            try {
                const plotdata = JSON.parse(newData);

                setChatHistory(prevChatHistory => {
                    const updatedChatHistory = [...prevChatHistory];
                    const lastChat = updatedChatHistory[updatedChatHistory.length - 1];
                    lastChat.chartData = plotdata;
                    return updatedChatHistory;
                })
            } catch (error) {
                console.info("response is not json");
                setChatHistory(prevChatHistory => {
                    const updatedChatHistory = [...prevChatHistory];
                    const lastChat = updatedChatHistory[updatedChatHistory.length - 1];
                    lastChat.userMessage = lastChat.userMessage + newData;
                    return updatedChatHistory;
                })
            }
        }

    }



    const updateChatHistory = (userQuery: string, chatMessage: ChatMessage, queryCategory?: string) => {
        if (userQuery === "" || isSending) { return; }
        const userItem = { userType: "user", userMessage: userQuery };
        const botItem = { userType: "system", userMessage: "" };
        let userItems = [...chatHistory, userItem, botItem];
        setChatHistory(userItems);
        setIsSending(true);
        sendMessage(userQuery, chatMessage as ChatMessage, handleMessage, queryCategory);
        setUserQuery('');
    }

    return (
        <div >

            <Stack className={Styles.scrollableContainerStyle} >
                {
                    chatHistory.map((chat, index) => (
                        <Stack key={index}  >
                            <Stack horizontal className={Styles.alignCenter}>
                                <div style={{ marginRight: '10px' }} >
                                    {
                                        chat.userType === 'user' ? <Person24Filled primaryFill="#c239b3" />
                                            : <Bot24Filled primaryFill="#eaa300" />
                                    }
                                </div>
                                <div >
                                    {
                                        chat.userType === 'user' ? <h4>You</h4> : <h4>Autogen</h4>
                                    }
                                </div>
                            </Stack>
                            {
                                isSending && index === chatHistory.length - 1 && chat.userType === 'system' ? <SkeletonComponent /> : <></>
                            }
                            <div ref={divRef} className={chat.userType === 'user' ? Styles.chatItemMessageUserStyles : Styles.chatItemMessageBotStyles}>
                                {
                                    <Text style={{ color: DefaultPalette.neutralLight}} variant="mediumPlus">
                                        {
                                        chat.userType === 'user' ? <p>{chat.userMessage}</p>
                                        : <ReactMarkdown>{chat.userMessage}</ReactMarkdown>
                                        }
                                    </Text>
                                }
                                {
                                    chat.userType === 'system' && chat.chartData ? (
                                        <>
                                            <AIChartComponent ChartData={chat.chartData} />
                                            <Text style={{ color: DefaultPalette.neutralLight }} variant="mediumPlus"><ReactMarkdown>{chat.chartData.dataAnalysis}</ReactMarkdown></Text>
                                        </>
                                    ) : (
                                        <></>
                                    )
                                }
                                <Divider appearance="default" style={{ width: '90%', textAlign: 'center' }} />
                            </div>
                        </Stack>
                    ))
                }
            </Stack>
            <div >
                <Label htmlFor={textareaId}></Label>
                <Stack horizontal className={Styles.chatAreaStackStyle}>
                    <Textarea id={textareaId} {...props}
                        style={{ width: '95%', border: 'none' }}
                        disabled={isSending}
                        value={userQuery}
                        onChange={handleUserQueryChange}
                        onKeyDown={handleUserQuery}
                        onInput={autoResize}
                        ref={textareaRef}
                        maxLength={500}
                        placeholder="Type your query here or select a question from the FAQs..."
                    />
                    {isSending && (
                        <div onClick={cancelResponse}
                            className={Styles.sendButtonStyle}
                            onMouseEnter={handleMouseEnter}
                            onMouseLeave={handleMouseLeave}
                        >
                            {isHovered ? <RecordStop24Regular /> : <RecordStop24Filled />}
                        </div>
                    )}

                    {!isSending && (
                        <div onClick={handleUserQuery}
                            className={Styles.sendButtonStyle}
                            onMouseEnter={handleMouseEnter}
                            onMouseLeave={handleMouseLeave}
                        >
                            {isHovered ? <Send24Regular /> : <Send24Filled />}
                        </div>
                    )}
                </Stack>
            </div>
        </div>
    );
};


export default ChatInputComponent;
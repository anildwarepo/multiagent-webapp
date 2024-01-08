import { DefaultPalette } from '@fluentui/react/lib/Styling';
import { mergeStyles} from '@fluentui/react/lib/Styling';
import * as Styles from './styles';
import ChatInputComponent from './ChatInput';
import FAQComponent from './FAQComponent';
import { useState } from 'react';

function MainComponent() {
    
    const [faq, setFAQ] = useState('');

    // Callback function to update userQuery
    const updateUserQuery = (query: string) => {
        setFAQ(query);
    };
    
    return (
        <div style={{ display: 'flex', width: '100vw', height: '100vh' }}>
            <div style={{ width: '20%', height: '100%', backgroundColor: DefaultPalette.neutralDark}}>
                <div className={mergeStyles(Styles.leftParentContainerStyles)}>
                    <div className={mergeStyles(Styles.leftContainerStyles)}>
                        <FAQComponent onPanelClick={updateUserQuery}/>
                    </div>
                </div>
                
            </div>
            <div style={{ width: '80%', height: '100%', backgroundColor: '#424242' }}>
                <div className={mergeStyles(Styles.rightParentContainerStyles)}>
                    <div className={mergeStyles(Styles.rightContainerStyles)}>
                        <ChatInputComponent faq={faq} setFAQ={setFAQ}/>
                    </div>
                </div>
            </div>
        </div>
    )
}

export default MainComponent;
import * as React from "react";
import {
    Accordion,
    AccordionHeader,
    AccordionItem,
    AccordionPanel,
    Divider,
    Label,
} from "@fluentui/react-components";
import { Text } from "@fluentui/react";
import * as Styles from "./styles";

interface FAQComponentProps {
    onPanelClick: (query: string) => void;
}

const FAQComponent: React.FC<FAQComponentProps> = ({ onPanelClick, ...props }) => {

    const handlePanelClick = (e: any) => {
        onPanelClick(e);
        //onPanelClick(e.target.textContent || e.target.innerText); // Update this string as needed
    };

    const options = [
        { key: 'q11', text: 'What are the different product divisions in Microsoft?', 'category': 'Company Info' },
        { key: 'q12', text: 'What industries does Autodesk operate in?', 'category': 'Company Info' },
        { key: 'q13', text: 'what was revenue for autodesk in the last quarter?', 'category': 'Company Info' },
        { key: 'q14', text: 'what are autodesk plans to grow revenue using AI?', 'category': 'Company Info' },
        { key: 'q15', text: 'Show me the YTD gain of 10 largest technology companies as of today.', 'category': 'Data Analysis' },  
        { key: 'q1', text: 'how to train NLP model using aml sdk v2. explain in 10 steps.', 'category': 'Product Guide' },
        { key: 'q2', text: 'Show me daily revenue trends per region', 'category': 'Data Analysis' },
        { key: 'q3', text: 'Is that true that top 20% customers generate 80% revenue? What is their percentage of revenue contribution?', 'category': 'Data Analysis' },
        { key: 'q4', text: 'Which products have most seasonality in sales quantity?', 'category': 'Data Analysis' },
        { key: 'q5', text: 'Which customers are most likely to churn who use our products?', 'category': 'Data Analysis' },
        { key: 'q6', text: 'What is the impact of discount on sales? What is optimal discount rate?', 'category': 'Data Analysis' },
        { key: 'q7', text: 'Predict monthly revenue for next 6 months.', 'category': 'Data Analysis' },
        { key: 'q8', text: 'Pick top 20 customers generated most revenue and for each customer show 3 products that they purchased most', 'category': 'Data Analysis'},
        { key: 'q9', text: 'which type of telco customer has the highest churn rate?. Generate customer email to address churn rate.' , 'category': 'Data Analysis'},
        { key: 'q10', text: 'How to configure networking using SDWAN?' , 'category': 'Product Guide'}             

    ];

    const groupedOptions = options.reduce((acc, option) => {
        acc[option.category] = acc[option.category] || [];
        acc[option.category].push(option);
        return acc;
    }, {} as Record<string, typeof options>);

    
    return (

       <div>
            <Label size='large' weight="semibold" >
                <span style={{color: '#d13438'}}>FAQs</span>
            </Label>
            <Accordion multiple>
            {Object.entries(groupedOptions).map(([category, questions], idx) => (
               
             
                <AccordionItem key={idx} value={category}>
                <AccordionHeader>
                        <Text className={Styles.faqStyle} variant="mediumPlus">{category}</Text>
                    </AccordionHeader>
                        {questions.map((question) => (
                            <AccordionPanel key={question.key}>
                                <div className={Styles.faqItemsStyle} onClick={() => handlePanelClick(question.text)}>
                                    {question.text}
                                </div>
                            </AccordionPanel>
                        ))}
                        <Divider />
                </AccordionItem>
                
            ))}

            </Accordion>        
           
        </div>
    )
}

export default FAQComponent;
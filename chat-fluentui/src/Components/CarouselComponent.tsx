import * as React from 'react';
import { initializeIcons } from '@fluentui/font-icons-mdl2';
import { IconButton } from '@fluentui/react/lib/Button';
import { mergeStyles } from '@fluentui/react/lib/Styling';


initializeIcons();

const carouselContainer = mergeStyles({
    position: 'relative',
    width: '100%',
    height: 'auto',
    marginBottom: '7%',
    display: 'flex', // Use Flexbox to layout children in a row
    alignItems: 'center', // Vertically center the children
    justifyContent: 'center', // Horizontally center the children
  });
  
  const buttonStyles = mergeStyles({
    position: 'absolute',
    top: '50%',
    transform: 'translateY(-50%)',
  });

  const carouselContent = mergeStyles({
    width: '80%',
    display: 'flex', // Use Flexbox to layout children in a row
    alignItems: 'center', // Vertically center the children
    justifyContent: 'center', // Horizontally center the children
  });
  
  const leftButtonStyles = mergeStyles(buttonStyles, {
    left: '0',
  });
  
  const rightButtonStyles = mergeStyles(buttonStyles, {
    right: '0',
  });
  

interface CarouselProps {
    //content: { key: string; text: string }[];
    userQuery: string;
    onUpdateQuery: (newQuery: string) => void
}

const Carousel: React.FC<CarouselProps> = ({ userQuery, onUpdateQuery }) => {
    const [currentIndex, setCurrentIndex] = React.useState(0);

    const options = [
        { key: 'q11', text: 'What are the different product divisions in Microsoft?' },
        { key: 'q12', text: 'What industries does Autodesk operate in?' },
        { key: 'q13', text: 'what was revenue for autodesk in the last quarter?' },
        { key: 'q14', text: 'what are autodesk plans to grow revenue using AI?' },
        { key: 'q15', text: 'Show me the YTD gain of 10 largest technology companies as of today.' },  
        { key: 'q1', text: 'how to train NLP model using aml sdk v2. explain in 10 steps.' },
        { key: 'q2', text: 'Show me daily revenue trends per region' },
        { key: 'q3', text: 'Is that true that top 20% customers generate 80% revenue? What is their percentage of revenue contribution?' },
        { key: 'q4', text: 'Which products have most seasonality in sales quantity?' },
        { key: 'q5', text: 'Which customers are most likely to churn who use our products?' },
        { key: 'q6', text: 'What is the impact of discount on sales? What is optimal discount rate?' },
        { key: 'q7', text: 'Predict monthly revenue for next 6 months.' },
        { key: 'q8', text: 'Pick top 20 customers generated most revenue and for each customer show 3 products that they purchased most'},
        { key: 'q9', text: 'which type of telco customer has the highest churn rate?. Generate customer email to address churn rate.' },
        { key: 'q10', text: 'How to configure networking using SDWAN?' }             

    ];

    React.useEffect (() => {
        // Call the callback function with the new text
        onUpdateQuery(options[currentIndex].text);
    }, [currentIndex]);

    const goToPrevious = () => {
      const newIndex = currentIndex === 0 ? options.length - 1 : currentIndex - 1;
      setCurrentIndex(newIndex);
    };
  
    const goToNext = () => {
      const newIndex = currentIndex === options.length - 1 ? 0 : currentIndex + 1;
      setCurrentIndex(newIndex);
    };


  
    return (
      <div className={carouselContainer}>
        <IconButton iconProps={{ iconName: 'ChevronLeft' }} onClick={goToPrevious} className={leftButtonStyles} />
        <div className={carouselContent}> <span>{options[currentIndex].text}</span> </div>
        <IconButton iconProps={{ iconName: 'ChevronRight' }} onClick={goToNext} className={rightButtonStyles}/>
      </div>
    );
};

export default Carousel;

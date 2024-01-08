import { IStyle } from '@fluentui/react/lib/Styling';
import { shorthands, tokens, makeStyles} from "@fluentui/react-components";
import { mergeStyles } from '@fluentui/react/lib/Styling';

// Parent container style
export const parentContainerStyles: IStyle = {
  height: '100vh', // Full height of the viewport
  width: '100vw', // Full width of the viewport
  display: 'flex', // Use Flexbox
  flexDirection: 'column', // Arrange children vertically
  justifyContent: 'flex-end', 
  alignItems: 'center', // Center vertically
};

// Your existing container style
export const containerStyles: IStyle = {
  height: 'auto', // Or any specific height
  width: '60%', // Half of the viewport width or any specific width
  //backgroundColor: DefaultPalette.themePrimary,
  marginBottom: tokens.spacingHorizontalL,
  // Other styling as needed
};

export const rightParentContainerStyles: IStyle = {
  height: '100%', // Full height of the viewport
  width: '100%', // Full width of the viewport
  display: 'flex', // Use Flexbox
  flexDirection: 'column', // Arrange children vertically
  justifyContent: 'flex-end', 
  alignItems: 'center', // Center vertically
};

// Your existing container style
export const rightContainerStyles: IStyle = {
  height: 'auto', // Or any specific height
  width: '90%', // Half of the viewport width or any specific width
  //backgroundColor: DefaultPalette.themePrimary,
  marginBottom: tokens.spacingHorizontalL,
  // Other styling as needed
};


export const leftParentContainerStyles: IStyle = {
  height: '100%', // Full height of the viewport
  width: '98%', // Full width of the viewport
  display: 'flex', // Use Flexbox
  flexDirection: 'column', // Arrange children vertically
  justifyContent: 'flex-center', 
  alignItems: 'center', // Center vertically
};

// Your existing container style
export const leftContainerStyles: IStyle = {
  height: '100%', // Or any specific height
  width: '90%', // Half of the viewport width or any specific width
  //backgroundColor: DefaultPalette.themePrimary,
  marginBottom: tokens.spacingHorizontalL,
  overflowY: 'auto',
  // Custom scrollbar styles
  '::-webkit-scrollbar': {
    width: '2px',
    height: '10px',
  },
  '::-webkit-scrollbar-track': {
    //background: DefaultPalette.blackTranslucent40,
  },
  '::-webkit-scrollbar-thumb': {
    background: '#888',
    borderRadius: '10px',
  },
  '::-webkit-scrollbar-thumb:hover': {
    background: '#555',
  },

};

export const chatAreaStackStyle = mergeStyles({
  
  width: '95%', 
  //border : '1px solid' , 
  //borderColor : DefaultPalette.blackTranslucent40 , 
  borderRadius : '8px', 
  alignItems: 'center'
  
})


export const faqStyle = mergeStyles({
  color: '#479ef5',
  ':hover': {
    cursor: 'pointer',
   
    
  },
})


export const faqItemsStyle = mergeStyles({
  marginBottom: '5px',
  ':hover': {
    cursor: 'pointer',
    color: '#f7630c',
  },
})

export const sendButtonStyle = mergeStyles({  
  marginLeft: '10px',  
})

export const useSkeletonStyles = makeStyles({
  invertedWrapper: {
    backgroundColor: tokens.colorNeutralBackground1,
  },
  firstRow: {
    alignItems: "center",
    display: "grid",
    paddingBottom: "10px",
    position: "relative",
    ...shorthands.gap("10px"),
    gridTemplateColumns: "min-content 80%",
  },
  secondThirdRow: {
    alignItems: "center",
    display: "grid",
    paddingBottom: "10px",
    position: "relative",
    ...shorthands.gap("10px"),
    gridTemplateColumns: "min-content 20% 20% 15% 15%",
  },
});

export const scrollableContainerStyle = mergeStyles({
  flex: 1,
  display: 'flex',
  marginTop: '0px',
  marginBottom: '20px',
  marginLeft: '20px',
  marginRight: '20px',
  gap: '5px',
  width: '95%', // Take up full width of parent
  height: '100%', // Take up full height of parent
  maxHeight: '80vh',
  overflowY: 'auto',
    
  // Custom scrollbar styles
  '::-webkit-scrollbar': {
    width: '2px',
    height: '10px',
  },
  '::-webkit-scrollbar-track': {
    //background: DefaultPalette.blackTranslucent40,
  },
  '::-webkit-scrollbar-thumb': {
    background: '#888',
    borderRadius: '10px',
  },
  '::-webkit-scrollbar-thumb:hover': {
    background: '#555',
  },
});


export const scrollableFAQStyle = mergeStyles({
  flex: 1,
  display: 'flex',
  marginTop: '20px',
  marginBottom: '20px',
  marginLeft: '2px',
  marginRight: '2px',
  gap: '5px',
  width: '20%', // Take up full width of parent
  height: '100%', // Take up full height of parent
  overflowY: 'auto',
    
  // Custom scrollbar styles
  '::-webkit-scrollbar': {
    width: '2px',
    height: '10px',
  },
  '::-webkit-scrollbar-track': {
    //background: DefaultPalette.blackTranslucent40,
  },
  '::-webkit-scrollbar-thumb': {
    background: '#888',
    borderRadius: '10px',
  },
  '::-webkit-scrollbar-thumb:hover': {
    background: '#555',
  },
});

export const chatItemRightStyles = mergeStyles({
  alignSelf: 'flex-end',
  flexDirection: 'row-reverse',
  marginTop: '0px',
  marginBottom: '0px',
  marginRight: '10px',
  width: '100%',
});

export const chatItemLeftStyles = mergeStyles({
  alignSelf: 'flex-start',
  flexDirection: 'row',
  marginRight: '10px',
});

export const messageItemLeftStyles = mergeStyles({
  display: 'flex',
  flexDirection: 'row',
  justifyContent: 'space-between',
  alignItems: 'center',
  padding: 0,
  margin: 0,
  borderRadius: 0,
  backgroundColor: 'transparent',
});

export const messageItemRightStyles = mergeStyles({
  display: 'flex',
  flexDirection: 'row-reverse',
  justifyContent: 'space-between',
  alignItems: 'center',
  padding: 0,
  margin: 0,
  borderRadius: 0,
  backgroundColor: 'transparent',
});

export const chatItemMessageUserStyles = mergeStyles({
  //width: '100%',
  textAlign: 'left',
  borderRadius: 0,

});

export const chatItemMessageBotStyles = mergeStyles({
  //width: '100%',
  textAlign: 'left',
  borderRadius: 0,
  padding: 0,
});

export const alignCenter = mergeStyles({
  alignItems: 'center',

});

export * from './styles';

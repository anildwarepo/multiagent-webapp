import * as React from 'react';
import { getTheme, mergeStyleSets } from '@fluentui/react/lib/Styling';
import ReactMarkdown from 'react-markdown';
import { ScrollablePane, IScrollablePaneStyles } from '@fluentui/react/lib/ScrollablePane';
import { Sticky, StickyPositionType } from '@fluentui/react/lib/Sticky';

export interface IScrollablePaneExampleItem {
  color: string;
  text: string;
  index: number;
}
const theme = getTheme();
const classNames = mergeStyleSets({
  wrapper: {
    height: '80vh',
    position: 'relative',
    maxHeight: 'inherit',
    
  },
  pane: {
    maxWidth: 400,
    border: '0px solid ' + theme.palette.neutralLight,
  },
  sticky: {
    color: theme.palette.neutralLight,
    padding: '5px 20px 5px 10px',
    fontSize: '13px',
    borderTop: '0px solid ' + theme.palette.orangeLight,
    borderBottom: '1px solid ' + theme.palette.orangeLight,
  },
  textContent: {
    padding: '15px 10px',
    contentEditable: 'true',
  },
});
const systemMessage = `You are a document expert. You will be provided with a document to analyze. 
You need to classify and extract information from the document. Provide complete response.
Use markdown formatting to format your response that can be rendered on HTML page.
Reply \`TERMINATE\` in the end when everything is done.
  
You need to classify the documents into the following type and subtypes:
type: financial, legal, technical, HR, other.
confidentiality: High - If it contains people names or company secrets, General - for forms, policies and letters.
subtypes: HR_email, HR_policies, HR_letter, HR_forms, HR_emails.
Your response in the below format:
**Confidentiality:** \`Confidentiality of the document\` \n
**Document Classification:** \`true\`  \n
**Document Type:** \`type of document\`  \n
**Document Subtype:** \`document sub type\` \n  
**Document Content:** \`provide short and complete content of the document under 10 words\` `;

const scrollablePaneStyles: Partial<IScrollablePaneStyles> = { root: classNames.pane };
const colors = ['#5c5c5c', '#dadada', '#d0d0d0', '#c8c8c8', '#a6a6a6', '#c7e0f4', '#71afe5', '#eff6fc', '#deecf9'];
const items = Array.from({ length: 1 }).map((item, index) => ({
  color: colors.splice(Math.floor(Math.random() * colors.length), 1)[0],
  text: systemMessage,
  index,
}));
const createContentArea = (item: IScrollablePaneExampleItem) => (
  <div
    key={item.index}
    style={{
      backgroundColor: '#5c5c5c',
    }}
  >
    <Sticky stickyPosition={StickyPositionType.Both}>
      <div role="heading" aria-level={1} className={classNames.sticky}>
        System Message
      </div>
    </Sticky>
    <div className={classNames.textContent}>
      <ReactMarkdown>{item.text}</ReactMarkdown>
      </div>
  </div>
);
const contentAreas = items.map(createContentArea);
export const SystemSettingsComponent: React.FunctionComponent = () => (
  <div className={classNames.wrapper}>
    <ScrollablePane
      scrollContainerFocus={true}
      scrollContainerAriaLabel="Sticky component example"
      styles={scrollablePaneStyles}
    >
      {contentAreas}
    </ScrollablePane>
  </div>
);
export default SystemSettingsComponent;
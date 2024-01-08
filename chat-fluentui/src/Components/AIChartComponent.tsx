import Plot from 'react-plotly.js';
import {AIChartComponentProps} from '../Interfaces/iprompt';


const AIChartComponent: React.FC<AIChartComponentProps>  = ({ChartData}) => {
    
   
    //const [newdata, setData] = useState(ChartData);
    const chart = <Plot
        //data={JSON.parse(data1)}
        data={ChartData.data}
        layout={ChartData.layout}
        //layout={{ width: 500, height: 240, title: 'A Fancy Plot' }}
    />
    return chart
}

export default AIChartComponent;

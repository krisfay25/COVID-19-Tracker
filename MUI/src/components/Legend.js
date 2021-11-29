import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import LegendItem from "./LegendItem";

const Legend = ({itemList}) => {
    const legendList = [
        new LegendItem(
            "100,000+",
            "#990000",
            (cases) => cases >= 100000
        ),
        new LegendItem(
            "75,000-99,999",
            "#cc0000",
            (cases) => cases >= 75000 && cases <= 99999
        ),
        new LegendItem(
            "50,000-74,999",
            "#ff0000",
            (cases) => cases >= 50000 && cases <= 74999
        ),
        new LegendItem(
            "25,000-49,999",
            "#ff4d4d",
            (cases) => cases >= 25000 && cases <= 49999
        ),
        new LegendItem(
            "0-24,999",
            "#ffffff",
            (cases) => true
        ),
    ]
    return(
        <div style={{
            display: "flex",
            alignItems: "stretch",
            position: "absolute",
            bottom: 5,
            left: 5,
            fontWeight: "bold",
        }}>
        <List>
            {legendList.map((item)=>(
                <ListItem key={item.title} style={{
                    backgroundColor: item.color,
                }}>
                <div style={{
                    backgroundColor: item.color,
                }}>
                {item.title}
                </div>
                </ListItem>
            ))}
        </List>
        </div>
    )
}
export default Legend;

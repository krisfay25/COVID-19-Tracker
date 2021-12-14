import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import LegendItem from "./LegendItem";
import ListSubheader from '@mui/material/ListSubheader';

const Legend = ({ dataType }) => {
    const legendList = [
        new LegendItem(
            dataType === "cases" ? "16,000+" :
                dataType === "vaccinations" ? "60,000-62,499" :
                    "400+",
            "#FF0000",
            (cases) => cases >= 100000
        ),
        new LegendItem(
            dataType === "cases" ? "12,000-15,999" :
                dataType === "vaccinations" ? "62,500-64,999" :
                    "300-399",
            "#FF5700",
            (cases) => cases >= 75000 && cases <= 99999
        ),
        new LegendItem(
            dataType === "cases" ? "8,000-11,999" :
                dataType === "vaccinations" ? "65,000-67,499" :
                    "200-299",
            "#FFE400",
            (cases) => cases >= 50000 && cases <= 74999
        ),
        new LegendItem(
            dataType === "cases" ? "4,000-7,999" :
                dataType === "vaccinations" ? "67,500-69,999" :
                    "100-199",
            "#6AFF00",
            (cases) => cases >= 25000 && cases <= 49999
        ),
        new LegendItem(
            dataType === "cases" ? "0-3,999" :
                dataType === "vaccinations" ? "70,000+" :
                    "0-99",
            "#00FF00",
            (cases) => cases >= 0
        ),
        new LegendItem(
            "No Data",
            "#ffffff",
            (cases) => true
        ),
    ]
    return (
        <div style={{
            display: "flex",
            alignItems: "stretch",
            position: "absolute",
            top: 5,
            right: 5,
            fontWeight: "bold",
            maxWidth: 150,
        }}>
            <List
                subheader={
                    <ListSubheader component="div" id="nested-list-subheader">
                        {dataType === "cases" ? "Case Rate" :
                            dataType === "vaccinations" ? "Vaccination Rate" :
                                "Death Rate"}
                    </ListSubheader>
                }
            >
                {legendList.map((item) => (
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

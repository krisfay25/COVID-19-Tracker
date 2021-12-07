import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import LegendItem from "./LegendItem";
import ListSubheader from '@mui/material/ListSubheader';

const Legend = ({ dataType }) => {
    const legendList = [
        new LegendItem(
            dataType == "cases" ? "100,000+" :
                dataType == "vaccinations" ? "6,000+" :
                    "3,000+",
            "#FF0000",
            (cases) => cases >= 100000
        ),
        new LegendItem(
            dataType == "cases" ? "75,000-99,999" :
                dataType == "vaccinations" ? "4,500-5,999" :
                    "2,250-2,999",
            "#FF5700",
            (cases) => cases >= 75000 && cases <= 99999
        ),
        new LegendItem(
            dataType == "cases" ? "50,000-74,999" :
                dataType == "vaccinations" ? "3,000-4,499" :
                    "1,500-2,249",
            "#FFE400",
            (cases) => cases >= 50000 && cases <= 74999
        ),
        new LegendItem(
            dataType == "cases" ? "25,000-49,999" :
                dataType == "vaccinations" ? "1,500-2,999" :
                    "750-1,499",
            "#6AFF00",
            (cases) => cases >= 25000 && cases <= 49999
        ),
        new LegendItem(
            dataType == "cases" ? "0-24,999" :
                dataType == "vaccinations" ? "0-1,499" :
                    "0-749",
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
                        {dataType == "cases" ? "Case Rate" :
                            dataType == "vaccinations" ? "Vaccination Rate" :
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

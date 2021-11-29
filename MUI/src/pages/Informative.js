import React, {useState, useEffect} from 'react'
import TemporaryDrawer from '../components/TemporaryDrawer';
import TotalsTable from '../components/TotalsTable';
import MonthlyData from '../components/MonthlyData';

import Select from '@mui/material/Select';
import MenuItem from '@mui/material/MenuItem';
import Box from '@mui/material/Box';
import List from '@mui/material/List';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemText from '@mui/material/ListItemText';
import ExpandLess from '@mui/icons-material/ExpandLess';
import ExpandMore from '@mui/icons-material/ExpandMore';
import Collapse from '@mui/material/Collapse';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';

export const Informative = () => {
    const [loading, setLoading] = useState(false);
    const [main, setMain] = useState([]);
    const [monthly, setMonthly] = useState({});
    // Fips codes for counties we currently support
    const [counties] = useState([44001, 44003, 44005, 44007, 44009]);
    const [currentCounty, setCurrentCounty] = React.useState(44001);

    // Years that we support
    const [years] = useState([2020, 2021]);
    const [currentYear, setCurrentYear] = useState(2021);
    function updateCurrentYear(event) {
        setCurrentYear(event.target.value);
    }

    useEffect(() => {
        // Load county data
        Promise.all(counties.map(fips =>
            fetch(`http://localhost:5000/county/${fips}`)
                .then(response => response.json())
        )).then(data => {
            // Replace state id with state name and add id
            var id_val = 0;

            for (let county of data) {
                if (county.state_id === 44) {
                    county.state = 'Rhode Island';
                    county.id = id_val++;
                }
            }
            setMain(data);
            setLoading(true);
        });
    }, [counties]);

    // When county is changed, load monthly data for that county
    useEffect(() => {
        if (!(currentCounty in monthly)) {
            fetch(`http://localhost:5000/county/${currentCounty}/monthly`)
                .then(response => response.json())
                .then(data => {
                    // Add ids and month names, then add data to variable
                    const months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
                    setMonthly({
                        ...monthly,
                        [currentCounty]: data.map((entry, counter) => {
                            entry.id = counter;
                            entry.month = months[entry.infection_month-1];
                            return entry;
                        })
                    });
                });
        }
    }, [currentCounty, monthly]);

    return (
        <Box sx={{ px:5, py:3 }}>
            <TemporaryDrawer/>
            <h1>Rhode Island</h1> 
            {!loading ? <div>Loading....</div> : <div>
            <h2>Total Data</h2>
            <TotalsTable data={main} />
            </div>}
            <h2>Monthly Data</h2>
            <Select value={currentYear} onChange={updateCurrentYear}>
                {years.map(year => <MenuItem key={year} value={year}>{year}</MenuItem>)}
            </Select>
            <Card>
                <CardContent>
                    <List>
                        {main.map(county => (<div key={county.fips}>
                            <ListItemButton onClick={() => setCurrentCounty(county.fips)}>
                                <ListItemText primary={county.county_name} />
                                {currentCounty===county.fips ? <ExpandLess /> : <ExpandMore />}
                            </ListItemButton>

                            <Collapse in={currentCounty===county.fips} timeout="auto" unmountOnExit>
                                {county.fips in monthly
                                    ? <MonthlyData data={monthly[county.fips].filter(entry => entry.infection_year===currentYear)}/>
                                    : <p>Loading...</p>
                                }
                            </Collapse>
                        </div>))}
                    </List>
                </CardContent>
            </Card>
        </Box>
    )
}

export default Informative;

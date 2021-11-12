import React, {useState, useEffect} from 'react'
import TemporaryDrawer from '../components/TemporaryDrawer';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';

export const Informative = () => {
    const [loading, setLoading] = useState(false);
    const [main, setMain] = useState([]);
    // Fips codes for counties we currently support
    const [counties] = useState([44001, 44003, 44005, 44009]);

    // The columns of the table and what property in the data they correspond to
    const columns = [
        { name: 'Fips', property: 'fips' },
        { name: 'State', property: 'state' },
        { name: 'County', property: 'county_name' },
        { name: 'Total Cases', property: 'total_cases' },
        { name: 'Total Deaths', property: 'total_deaths' },
        { name: 'Total Hospitalizations', property: 'total_hospital' },
        { name: 'Total Vaccinations', property: 'total_vaccinated' },
        { name: 'Last Updated', property: 'last_updated_timestamp' }
    ];

    useEffect(() => {
        // Load county data
        Promise.all(counties.map(fips =>
            fetch(`http://localhost:5000/county/${fips}`)
                .then(response => response.json())
        )).then(data => {
            // Replace state id with state name
            for (let county of data) {
                if (county.state_id === 44) {
                    county.state = 'Rhode Island';
                }
            }
            setMain(data);
            setLoading(true);
        });
    }, [counties]);

    return (
        <div>
            {!loading ? <div>Loading....</div> : <div>
            <TemporaryDrawer/>
            <TableContainer component={Paper}>
                <Table sx={{ minWidth: 650 }} aria-label="simple table">
                    <TableHead>
                        <TableRow>
                            {columns.map(column => (
                                <TableCell align="right" key={column.name}>{column.name}</TableCell>
                            ))}
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {main.map(county => (
                            <TableRow
                            key={`${county.fips}`}
                            sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
                            >
                                {columns.map(column => (
                                    <TableCell align="right" key={column.name}>{county[column.property]}</TableCell>
                                ))}

                            </TableRow>
                        ))}
                    </TableBody>
                </Table>
            </TableContainer>
            </div>}
        </div>
    )
}

export default Informative;

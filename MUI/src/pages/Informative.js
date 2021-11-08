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
    const [main] = useState([]);

    useEffect(() => {
            //fips 44001
            fetch('http://localhost:5000/county/44001', {
                headers : { 
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                }
            }).then(response=>response.json())
            .then(data => {
                main[0] = {data};
            });
    
            //fips 44003
            fetch('http://localhost:5000/county/44003', {
                headers : { 
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                }
            }).then(response=>response.json())
            .then(data => {
                main[1] = {data};
            });
    
            //fips 44005
            fetch('http://localhost:5000/county/44005', {
                headers : { 
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                }
            }).then(response=>response.json())
            .then(data => {
                main[2] = {data}
            });
    
            //fips 44007
            fetch('http://localhost:5000/county/44007', {
                headers : { 
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                }
            }).then(response=>response.json())
            .then(data => {
                main[3] = {data}
            });
    
            //fips 44009
            fetch('http://localhost:5000/county/44009', {
                headers : { 
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                }
            }).then(response=>response.json())
            .then(data => {
                main[4] = {data}
                setLoading(true);
            });
    },[main])

    console.log(main)
    return (
        <div>
            {!loading ? <div>Loading....</div> : <div>
            <TemporaryDrawer/>
            <TableContainer component={Paper}>
                <Table sx={{ minWidth: 650 }} aria-label="simple table">
                    <TableHead>
                        <TableRow>
                            <TableCell>Fips</TableCell>
                            <TableCell align="right">State</TableCell>
                            <TableCell align="right">County&nbsp;</TableCell>
                            <TableCell align="right">Total Cases&nbsp;</TableCell>
                            <TableCell align="right">Total Deaths&nbsp;</TableCell>
                            <TableCell align="right">Total Hospitalizations&nbsp;</TableCell>
                            <TableCell align="right">Total Vaccinations&nbsp;</TableCell>
                            <TableCell align="right">Last Updated&nbsp;</TableCell>
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {main.map(county => (
                            <TableRow
                            key={county.data.fips}
                            sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
                            >
                                <TableCell>
                                    {county.data.fips}
                                </TableCell>
                                <TableCell align="right">{county.data.state_id === 44 ? <>Rhode Island</> : county.data.state_id}</TableCell>
                                <TableCell align="right">{county.data.county_name}</TableCell>
                                <TableCell align="right">{county.data.total_cases}</TableCell>
                                <TableCell align="right">{county.data.total_deaths}</TableCell>
                                <TableCell align="right">{county.data.total_hospital}</TableCell>
                                <TableCell align="right">{county.data.total_vaccinated}</TableCell>
                                <TableCell align="right">{county.data.last_updated_timestamp}</TableCell>
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


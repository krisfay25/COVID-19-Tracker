import {DataGrid, GridRowsProp, GridColDef, GridToolbar} from '@mui/x-data-grid';
import { Toolbar } from '@mui/material';

export const TotalsTable = ({data}) => {

    const rows: GridRowsProp = data;

    const columns: GridColDef[] = [
        { headerName: 'Fips', field: 'fips' },
        { headerName: 'State', field: 'state' },
        { headerName: 'County', field: 'county_name' },
        { headerName: 'Total Cases', field: 'total_cases' },
        { headerName: 'Total Deaths', field: 'total_deaths' },
        { headerName: 'Total Hospitalizations', field: 'total_hospital' },
        { headerName: 'Total Vaccinations', field: 'total_vaccinated' },
        { headerName: 'Last Updated', field: 'last_updated_timestamp' }
    ];

    return(
        <div style={{ height: 300, width: '100%' }}>
            <DataGrid rows={rows} columns={columns} components={{Toolbar: GridToolbar,}} />
        </div>
    )
}

export default TotalsTable;
import {DataGrid, GridRowsProp, GridColDef, GridToolbar} from '@mui/x-data-grid';

export const TotalsTable = ({data}) => {

    const rows: GridRowsProp = data;

    const columns: GridColDef[] = [
        { headerName: 'Fips', field: 'fips', width: 160 },
        { headerName: 'State', field: 'state', width: 160 },
        { headerName: 'County', field: 'county_name', width: 160 },
        { headerName: 'Total Cases', field: 'total_cases', width: 160 },
        { headerName: 'Total Deaths', field: 'total_deaths', width: 160 },
        { headerName: 'Total Hospitalizations', field: 'total_hospital', width: 170 },
        { headerName: 'Total Vaccinations', field: 'total_vaccinated', width: 160 },
        { headerName: 'Case Rate', field: 'case_rate_per_100k', width: 160 },
        { headerName: 'Death Rate', field: 'death_rate_per_100k', width: 160 },
        { headerName: 'Hospitalization Rate', field: 'hospital_rate_per_100k', width: 160 },
        { headerName: 'Vaccination Rate', field: 'vaccinated_rate_per_100k', width: 160 },
        { headerName: 'Last Updated', field: 'last_updated_timestamp', width: 160 }
    ];

    return(
        <div style={{ height: 400, width: '100%' }}>
            <DataGrid rows={rows} columns={columns} components={{Toolbar: GridToolbar,}} />
        </div>
    )
}

export default TotalsTable;
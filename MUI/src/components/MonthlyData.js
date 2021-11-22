import {DataGrid, GridToolbar} from '@mui/x-data-grid';

export const MonthlyData = ({data}) => {
  const rows = data;

  // Headers
  const columns = [
    { headerName: 'Month', field: 'month', width: 160 },
    { headerName: 'Cases', field: 'num_cases', width: 160 },
    { headerName: 'Deaths', field: 'num_deaths', width: 160 },
    { headerName: 'Hospitalizations', field: 'num_hospit', width: 160 },
    { headerName: 'Vaccinations', field: 'num_vaxxed', width: 160 },
    { headerName: 'Case Rate', field: 'rate_cases', width: 160 },
    { headerName: 'Death Rate', field: 'rate_deaths', width: 160 },
    { headerName: 'Hospitalization Rate', field: 'rate_hospit', width: 160 },
    { headerName: 'Vaccination Rate', field: 'rate_vaxxed', width: 160 }
  ]

  return (
    <div style={{ height: 500, width: '100%' }}>
      <DataGrid rows={rows} columns={columns} components={{Toolbar: GridToolbar}} />
    </div>
  )
}

export default MonthlyData;
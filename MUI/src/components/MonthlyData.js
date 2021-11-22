import {DataGrid, GridToolbar} from '@mui/x-data-grid';

export const MonthlyData = ({data}) => {
  const rows = data;

  // Headers
  const columns = [
    { headerName: 'Month', field: 'month' },
    { headerName: 'Cases', field: 'num_cases' },
    { headerName: 'Deaths', field: 'num_deaths' },
    { headerName: 'Hospitalizations', field: 'num_hospit' },
    { headerName: 'Vaccinations', field: 'num_vaxxed' },
    { headerName: 'Case Rate', field: 'rate_cases' },
    { headerName: 'Death Rate', field: 'rate_deahts' },
    { headerName: 'Hospitalization Rate', field: 'rate_hospit' },
    { headerName: 'Vaccination Rate', field: 'rate_vaxxed' }
  ]

  return (
    <div style={{ height: 500, width: '100%' }}>
      <DataGrid rows={rows} columns={columns} components={{Toolbar: GridToolbar}} />
    </div>
  )
}

export default MonthlyData;
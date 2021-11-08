import React , {useState} from 'react';
import Switch from '@mui/material/Switch';

export const MapSwitch = ({ }) => {
    const [checked,setChecked] = useState(true);

    const handleChange = (event) => {
        setChecked(event.target.checked);
    }

    return(        
        <Switch
            checked={checked}
        onChange={handleChange}
        inputProps={{ 'aria-label': 'Map Switch' }}
        />
    )
}
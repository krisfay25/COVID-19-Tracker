import React , {useState} from 'react';
import Switch from '@mui/material/Switch';

export const GraphSwitch = () => {
    const [checked,setChecked] = useState(true);

    const handleChange = (event) => {
        setChecked(event.target.checked);
    }

    return(
        <Switch
            checked={checked}
            onChange={handleChange}
            inputProps={{ 'aria-label': 'Graph Switch' }}
        />
    )
}